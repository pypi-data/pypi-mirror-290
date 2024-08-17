from contextlib import suppress
from itertools import count
import logging
import os
import sys
from pathlib import Path, PurePath, PurePosixPath
import time
from hashboard.api.datasource.datasource_cli import datasource
import string
import subprocess
from typing import Dict, Optional, List
from uuid import UUID, uuid3
from prettytable import PrettyTable

import click
from hashboard.dbt_run_results_parser import parse_dbt_run_results
from hashboard.session import get_current_session
from ruamel.yaml import YAML

from hashboard.api.analytics.cli_with_tracking import (
    CommandWithTracking,
    GroupWithTracking,
    set_raw_command,
)
from hashboard.utils.env import env_with_fallback

from hashboard import VERSION
from hashboard.api import (
    apply_preview_build,
    build_details_uri,
    clear_model_cache,
    create_build_from_git_revision,
    create_build_from_local_files,
    fetch_build,
    fetch_build_status,
    login,
    get_datasources,
    get_tables,
    pull_resource,
    remove_from_data_ops_mutation,
)
from hashboard.api.access_keys.existing_user import create_access_key
from hashboard.constants import (
    DEFAULT_CREDENTIALS_FILEPATH,
    HASHBOARD_BASE_URI,
    HASHBOARD_DEBUG,
)
from hashboard.credentials import get_credentials
from hashboard.filesystem import local_resources
from hashboard.utils.cli import cli_error_boundary, getenv_bool
from hashboard.utils.grn import GRN_TYPE_KEY_MODEL, GRNComponents, parse_grn
from hashboard.utils.resource import Resource


# Turning this on will result in secrets getting logged to stdout.
HASHBOARD_VERBOSE_DEBUG_UNSAFE = getenv_bool("HASHBOARD_VERBOSE_DEBUG_UNSAFE")


MAX_COLUMN_REGEX_LENGTH = 30
MAX_COLUMN_FILTER_CHARS = 1000


def main():
    root_command_with_path, *rest = sys.argv
    root_command = root_command_with_path.split("/")[-1]
    raw_command = " ".join([root_command, *rest])
    set_raw_command(raw_command)
    with cli_error_boundary(debug=HASHBOARD_DEBUG):
        if not _check_version():
            logging.warning(
                "There is a newer version of the Hashboard CLI available on PyPI. Upgrade your hashboard-cli package for the latest features.\n"
            )

        cli()


git_revision_option = click.option(
    "--git-revision",
    type=str,
    required=False,
    help="""
    If specified, Hashboard will pull configuration files from your configured git repository at the provided commit,
    instead of using local files.
    """,
)
git_path_option = click.option(
    "--git-path",
    type=str,
    required=False,
    help="""
    A path within your git repo that will be used as the top-level directory for the Build.
    Only applicable when also using the `--git-revision` flag.
    """,
)
dbt_manifest_option = click.option(
    "--dbt-manifest",
    "dbt_manifest_path",
    required=False,
    help="Path to dbt manifest JSON file (if using Hashboard dbt integration).",
    type=click.Path(exists=True, readable=True, file_okay=True, dir_okay=False),
)
run_dbt_parse_option = click.option(
    "--dbt",
    "run_dbt_parse",
    required=False,
    help="If specified, runs `dbt parse` and uses the resulting manifest.",
    is_flag=True,
    default=False,
)
dbt_model_filter_option = click.option(
    "--dbt-models",
    "dbt_model_filter",
    required=False,
    help="A comma separated list of dbt models to include in the build. Will be ignored if neither --dbt nor --dbt-manifest flags are set. If not provided, all dbt models will be built.",
    type=click.STRING,
)
dbt_parse_flags_argument = click.argument(
    "DBT_FLAGS",
    type=click.STRING,
    nargs=-1,
)
local_path_argument = click.argument("filepath", type=click.STRING, default=".")
allow_dangerous_empty_build_option = click.option(
    "--allow-dangerous-empty-build",
    "allow_dangerous_empty_build",
    is_flag=True,
    default=False,
    help="Allow builds with no config files. WARNING: this will allow a build to delete all of your resources, including non-dataops resources that depend on your dataops resources!",
)
partial_option = click.option(
    "--partial",
    "partial",
    is_flag=True,
    default=False,
    help="Build a subset of resources",
)


@click.group(cls=GroupWithTracking, context_settings=dict(max_content_width=130))
@click.version_option(version=VERSION, prog_name="Hashboard CLI")
@click.option(
    "--credentials-filepath",
    type=str,
    help="Path to your Hashboard access key credentials. You can also control this by setting a HASHBOARD_CREDENTIALS_FILEPATH environment variable.",
)
@click.pass_context
def cli(ctx: click.Context, credentials_filepath: str):
    """A command-line interface for interacting with Hashboard."""
    if HASHBOARD_DEBUG or HASHBOARD_VERBOSE_DEBUG_UNSAFE:
        _enable_http_logging()
    ctx.ensure_object(dict)
    if credentials_filepath is None:
        credentials_filepath = env_with_fallback(
            "HASHBOARD_CREDENTIALS_FILEPATH",
            "GLEAN_CREDENTIALS_FILEPATH",
            DEFAULT_CREDENTIALS_FILEPATH,
        )
    ctx.obj["credentials_filepath"] = os.path.expanduser(credentials_filepath)


@cli.command(cls=CommandWithTracking)
@click.pass_context
def signup(ctx: click.Context):
    """Sign up for a new Hashboard account."""
    click.echo(
        f"👋 Welcome! Follow this link to get started with Hashboard and create a new project: {HASHBOARD_BASE_URI}/getAccess"
    )
    click.echo(
        "After creating your project, we recommend you to run `hb token` to create an access key."
    )


@cli.command(cls=CommandWithTracking)
@click.option(
    "--project-id",
    type=str,
    required=False,
    help="If specified, creates an access key for this project ID. Required if your Hashboard user is a member of multiple projects.",
)
@click.pass_context
def token(ctx: click.Context, project_id: Optional[str]):
    """Log into a Hashboard account and create a new access key.

    If `--credentials-filepath` is passed, will save the access key in that location.
    """
    create_access_key(ctx.obj["credentials_filepath"], project_id)


@cli.command(
    "preview",
    cls=CommandWithTracking,
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@git_revision_option
@git_path_option
@dbt_manifest_option
@local_path_argument
@run_dbt_parse_option
@dbt_model_filter_option
@dbt_parse_flags_argument
@allow_dangerous_empty_build_option
@partial_option
@click.pass_context
def preview_async(
    ctx,
    git_revision,
    git_path,
    dbt_manifest_path,
    filepath,
    run_dbt_parse,
    dbt_model_filter,
    dbt_flags,
    allow_dangerous_empty_build,
    partial,
):
    """Validates resource configurations and generates a preview link."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    dbt_manifest_path, dbt_inclusion_list = _handle_dbt_args(
        dbt_manifest_path, run_dbt_parse, dbt_flags, dbt_model_filter, partial
    )

    click.echo("🏗️  Creating preview build...")
    build_results = _create_build_using_options(
        ctx,
        filepath,
        git_revision=git_revision,
        git_path=git_path,
        deploy=False,
        dbt_manifest_path=dbt_manifest_path,
        dbt_inclusion_list=dbt_inclusion_list,
        allow_dangerous_empty_build=allow_dangerous_empty_build,
        partial=partial,
    )
    _echo_async_build_creation(build_results, False)

    build_id = build_results["data"]["createAsyncBuild"]
    build_results = _poll_for_build_status(build_id)

    _echo_async_build_results(build_results)


# TODO: Update to follow a build -> apply pattern
@cli.command(
    "deploy",
    cls=CommandWithTracking,
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@allow_dangerous_empty_build_option
@git_revision_option
@git_path_option
@dbt_manifest_option
@run_dbt_parse_option
@local_path_argument
@dbt_parse_flags_argument
@dbt_model_filter_option
@partial_option
@click.option(
    "--preview / --no-preview",
    default=True,
    help="Whether to generate a Preview Build before deploying.",
)
@click.pass_context
def deploy_async(
    ctx: click.Context,
    git_revision: Optional[str],
    git_path: Optional[str],
    dbt_manifest_path: Optional[PurePath],
    run_dbt_parse: bool,
    dbt_model_filter: str,
    filepath: str,
    preview: bool,
    dbt_flags,
    allow_dangerous_empty_build: bool,
    partial: bool,
):
    """Validates and deploys resource configurations to your project."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    dbt_manifest_path, dbt_inclusion_list = _handle_dbt_args(
        dbt_manifest_path, run_dbt_parse, dbt_flags, dbt_model_filter, partial
    )

    if not preview:
        click.echo("🚀 Creating deploy build...")
        build_results = _create_build_using_options(
            ctx,
            filepath,
            git_revision=git_revision,
            git_path=git_path,
            deploy=True,
            dbt_manifest_path=dbt_manifest_path,
            dbt_inclusion_list=dbt_inclusion_list,
            allow_dangerous_empty_build=allow_dangerous_empty_build,
            partial=partial,
        )
        _echo_async_build_creation(build_results, True)
        build_id = build_results["data"]["createAsyncBuild"]
        build_results = _poll_for_build_status(build_id)
        _echo_async_build_results(build_results, deploy=True)
    else:
        click.echo("🏗️  Creating preview build...")
        build_results = _create_build_using_options(
            ctx,
            filepath,
            git_revision=git_revision,
            git_path=git_path,
            deploy=False,
            dbt_manifest_path=dbt_manifest_path,
            dbt_inclusion_list=dbt_inclusion_list,
            allow_dangerous_empty_build=allow_dangerous_empty_build,
            partial=partial,
        )
        _echo_async_build_creation(build_results, False)
        build_id = build_results["data"]["createAsyncBuild"]
        build_results = _poll_for_build_status(build_id)
        _echo_async_build_results(build_results)
        if not click.confirm("Continue with deploy?"):
            ctx.exit(1)
        deploy_results = _create_build_using_options(
            ctx,
            filepath,
            git_revision=git_revision,
            git_path=git_path,
            deploy=True,
            dbt_manifest_path=dbt_manifest_path,
            dbt_inclusion_list=dbt_inclusion_list,
            allow_dangerous_empty_build=allow_dangerous_empty_build,
            partial=partial,
        )
        _echo_async_build_creation(deploy_results, True)
        deploy_id = deploy_results["data"]["createAsyncBuild"]
        deploy_completed = _poll_for_build_status(deploy_id)
        _echo_async_build_results(deploy_completed, deploy=True)

    click.echo("")
    click.echo(click.style("✅ Deploy complete.", fg="bright_green"))


def spinning_cursor():
    while True:
        for cursor in "|/-\\":
            yield cursor


def _poll_for_build_status(build_id):
    s = get_current_session()

    spinner = spinning_cursor()
    is_running = False
    for i in range(3000):  # arbitrary upper limit
        click.echo("\r" + next(spinner), nl=False)
        if not i % 10:
            click.echo("\b ", nl=False)
            sys.stdout.flush()
            partial_build = fetch_build_status(s, build_id)
            if ("errors" in partial_build and partial_build["errors"]) or partial_build[
                "data"
            ]["fetchBuild"]["status"] in ["completed", "applied"]:
                build = fetch_build(s, build_id)
                return build
            elif (
                partial_build["data"]["fetchBuild"]["status"] == "building"
                and not is_running
            ):
                click.echo("\bBuilding resources... ")
                is_running = True
        time.sleep(0.5)
    click.echo("Error fetching build, max attempt.", fg="red")
    click.get_current_context().exit(1)


@cli.command(cls=CommandWithTracking)
@click.argument("database")
@click.pass_context
def tables(ctx, database):
    """Specify a database connection name or id and see its available tables."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    s = get_current_session()
    project_id = login(s, ctx.obj["credentials"])

    datasource_list = get_datasources(s, project_id)
    name_lookup = {d[0]: d[2] for d in datasource_list}

    if database in name_lookup.keys():
        datasource_id = name_lookup[database]
    elif database in name_lookup.values():
        datasource_id = database
    else:
        _echo_datasource_not_found(database, datasource_list)
        ctx.exit(1)

    tables = get_tables(s, datasource_id)
    table_names = list(tables.keys())
    _echo_tables(table_names, database)


@cli.group(cls=GroupWithTracking)
@click.pass_context
def cache(ctx):
    """Hashboard stores the results of queries in a cache so that users don't have
    to access the database again."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    pass


@cache.command("clear", cls=CommandWithTracking)
@click.argument("resource_grn")
@click.pass_context
def cache_clear(ctx, resource_grn):
    """Clears the cache for the associated resource."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    s = get_current_session()
    login(s, ctx.obj["credentials"])

    grn = parse_grn(resource_grn)
    if not grn.gluid:
        click.echo("GRN must specify an id when clearing cache.")
        ctx.exit(1)
    if grn.resource_type != GRN_TYPE_KEY_MODEL:
        click.echo("Cache can only be cleared for models.")
        ctx.exit(1)

    clear_model_cache(s, grn.gluid)
    click.echo(f"Successfully cleared cache for {resource_grn}.")


@cli.command(cls=CommandWithTracking)
@click.argument("grn", required=False, type=str)
@click.option(
    "--all",
    is_flag=True,
    default=False,
    help="Pull all project resources, including those not managed by DataOps.",
)
@click.pass_context
def pull(
    ctx: click.Context,
    grn: str,
    all: bool = False,
):
    """Pull the latest DataOps resource configuration from Hashboard into the working directory.

    GRN is the Hashboard resource name of the target resource. If the resource has DataOps dependencies, they will also be
    retrieved. If no GRN is specified, all resources for the project are pulled.
    """
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])

    s = get_current_session()
    project_id = login(s, ctx.obj["credentials"])

    resource_type = None
    resource_id = None
    resource_alias = None

    # map the GRN resource type abbreviation to the full name
    RESOURCE_TYPE_FROM_ABBREV = {
        "dsb": "dashboard",
        "sv": "savedExploration",
        "m": "model",
        "palette": "colorPalette",
        "launchpad": "homepageLaunchpad",
        "mtr": "metric",
    }
    if grn:
        grn_components = parse_grn(grn)

        try:
            resource_type = RESOURCE_TYPE_FROM_ABBREV[grn_components.resource_type]
        except:
            raise click.ClickException(
                "Hashboard pull currently only supports models, saved views, dashboards, and color palettes"
            )
        resource_id = grn_components.gluid
        resource_alias = grn_components.alias

        # pulling a grn means we ignore the normal dataops-only filter
        all = True

    SUPPORTED_TYPES = [
        "dashboard",
        "saved_view",
        "saved_exploration",
        "model",
        "color_palette",
        "homepage_launchpad",
        "metric",
    ]
    local_by_path = {
        k: v for k, v in local_resources(Path(".")).items() if v.type in SUPPORTED_TYPES
    }
    click.echo(
        f"🔎 Found {len(local_by_path)} Hashboard resources in working directory."
    )

    def get_grn(path: PurePosixPath, resource: Resource) -> GRNComponents:
        RESOURCE_TYPE_TO_ABBREV = {
            "model": "m",
            "saved_view": "sv",
            "saved_exploration": "sv",
            "dashboard": "dsb",
            "color_palette": "palette",
            "homepage_launchpad": "launchpad",
            "metric": "mtr",
        }
        if resource.grn is not None:
            return resource.grn

        elif resource.type == "saved_view" or resource.type == "saved_exploration":
            # terrible special case logic for saved views to maintain backwards compatibility,
            # since saved view IDs include a hash of the model ID

            model_ref: str = resource.raw["model"]
            model_grn = None
            try:
                # resolve model references by file paths to their project-local path
                model_path = (
                    Path(path.parent / model_ref).resolve().relative_to(Path.cwd())
                )
                if model_path.exists():
                    model = local_by_path[PurePosixPath(model_path)]
                    assert model is not None
                    model_grn = get_grn(PurePosixPath(model_path), model)
            except OSError:  # python 3.7, Path.exists can throw if the path is invalid
                pass
            except ValueError:
                pass

            # if model is not a local path, it must be a GRN
            if not model_grn:
                model_grn = parse_grn(model_ref)

            model_id = model_grn.gluid
            assert model_id is not None

            default_namespace = UUID("{00000000-0000-0000-0000-000000000000}")
            initial_id = GRNComponents.generate("sv", project_id, path).gluid
            assert initial_id is not None
            sv_id = str(uuid3(default_namespace, model_id + initial_id))

            return GRNComponents("sv", sv_id)

        else:
            return GRNComponents.generate(
                RESOURCE_TYPE_TO_ABBREV[resource.type], project_id, path
            )

    # Can't use a map here because we actually _do_ want to compare GRNs that hash to different values!
    # In particular, if they have the same type/alias but different guid (because local hasn't received a guid),
    # they should be considered equal.
    local_by_grn = list(
        (get_grn(path, resource), path, resource)
        for (path, resource) in local_by_path.items()
    )
    local_grns = list(local_grn for (local_grn, _, _) in local_by_grn)

    result = pull_resource(
        s,
        project_id,
        resource_type,
        resource_id,
        resource_alias,
        dataops_only=(not all),
    )

    remote: list[Resource] = result["configs"]
    if len(remote) == 0 and not all:
        click.echo(
            "No DataOps-managed resources were found. To pull all resources in the project, use `hb pull --all`."
        )
        return

    touched_files = []  # either created or modified
    num_updated = 0
    for resource in remote:
        assert resource.grn is not None
        yaml = YAML(pure=True)
        with suppress(ValueError):
            index = local_grns.index(resource.grn)
            # we've matched the resource to a local file
            (_, path, local_resource) = local_by_grn[index]
            if local_resource.raw == resource.raw:
                continue
            # the resource has changed!
            num_updated += 1
            touched_files.append(Path(path))
            with open(Path(path), "w") as f:
                yaml.dump(resource.raw, f)

            continue

        # not present locally, so we need to make a new file
        name = "".join(
            filter(
                lambda x: x in string.ascii_letters or x in string.digits,
                resource.raw.get("name", "untitled").lower().replace(" ", "_"),
            )
        )
        name = resource.grn.resource_type + "_" + name
        for i in count(0):
            if i > 0:
                path = Path(f"{name}_{i}.yml")
            else:
                path = Path(f"{name}.yml")
            if path.exists():
                continue

            touched_files.append(path)
            with open(path, "w") as f:
                yaml.dump(resource.raw, f)

            break

    click.echo()
    if touched_files:
        click.echo(f"{len(touched_files)} files were created or modified:")
        _echo_list(list(sorted([str(p) for p in touched_files])))
        click.echo()
        if num_updated < len(local_by_path):
            click.echo(f"{len(local_by_path) - num_updated} files were not modified.")
    else:
        click.echo("No files were updated.")

    if result.get("errors"):
        _echo_pull_errors_and_exit(result["errors"])

    click.echo("✅ Project pulled successfully")


@cli.command("remove-from-data-ops", cls=CommandWithTracking)
@click.argument("resource_grns", nargs=-1)
@click.pass_context
def remove_from_data_ops(ctx, resource_grns):
    """Removes a Hashboard resource from DataOps management."""

    if len(resource_grns) == 0:
        raise click.UsageError("At least one GRN is required.")

    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])
    s = get_current_session()
    project_id = login(s, ctx.obj["credentials"])

    click.echo(f"Removing resources from DataOps management...")
    result = remove_from_data_ops_mutation(s, project_id, resource_grns)
    if result:
        click.echo(f"Resources removed from DataOps successfully.")
    else:
        click.echo(
            f"An unknown error occurred, please try again or contact support for assistance."
        )


def _handle_dbt_args(
    dbt_manifest_path: str,
    run_dbt_parse: bool,
    dbt_flags,
    dbt_model_filter: str,
    partial: bool,
):
    """Convenience wrapper for running `dbt parse` before `hb preview` or `hb deploy`.
    Must be run from your Hashboard project directory.

    Flags passed in after the hb subcommand will be passed onwards to dbt.
    """
    inclusion_list = (
        dbt_model_filter.split(",")
        if (dbt_manifest_path or run_dbt_parse) and dbt_model_filter
        else None
    )
    if not run_dbt_parse:
        # no --dbt flag
        if dbt_manifest_path is not None:
            # user specified --dbt-manifest explicitly
            click.echo(f"✅ Using manifest file at {dbt_manifest_path}\n")

        return dbt_manifest_path, inclusion_list

    if dbt_manifest_path is not None:
        click.echo()
        click.echo(
            "🚨 `--dbt-manifest` is redundant when running with `--dbt` and will be ignored."
        )
        click.echo()
    click.echo("🐇 Running `dbt parse` to generate a manifest file.")

    click.echo()

    dbt_flags = list(dbt_flags) or []
    # find the dbt target dir (some manual flags parsing)
    target_dir = Path("target")
    with suppress(ValueError, IndexError):
        flag_index = dbt_flags.index("--target-dir")
        target_dir = Path(dbt_flags[flag_index + 1])
    with suppress(StopIteration):
        flag_index = next(
            n for n, f in enumerate(dbt_flags) if f.startswith("--target-dir=")
        )
        if flag_index is not None:
            target_dir = Path(dbt_flags[flag_index][len("--target-dir=") :])

    dbt_command = (f"dbt parse " + " ".join(dbt_flags)).strip()
    click.echo(f"$ {dbt_command}")
    click.echo("--- dbt output ---")

    ret_code = subprocess.Popen(dbt_command.split(" ")).wait()
    click.echo("--- end of dbt output ---")
    if ret_code != 0:
        raise click.ClickException(f"dbt returned nonzero exit code ({ret_code})")

    manifest_path = target_dir / "manifest.json"
    if not manifest_path.is_file():
        raise click.ClickException(
            "⚠️ manifest file does not exist after `dbt parse` ran successfully."
        )

    # If there is no explicit inclusion list and this is a partial build parse run results and use that for the inclusion list
    run_results_path = target_dir / "run_results.json"
    if partial and not inclusion_list and run_results_path.is_file():
        try:
            with open(Path(run_results_path), "r") as f:
                run_results = f.read()
        except Exception as e:
            raise click.ClickException(f"Could not read dbt manifest file: {e}")

        inclusion_list = parse_dbt_run_results(run_results)

    click.echo()
    click.echo(f"✅ Using manifest file at {manifest_path}\n")
    return manifest_path, inclusion_list


cli.add_command(datasource)


def _create_build_using_options(
    ctx: click.Context,
    filepath: str,
    dbt_manifest_path: Optional[PurePath] = None,
    dbt_inclusion_list: Optional[List[str]] = None,
    git_revision: Optional[str] = None,
    git_path: Optional[str] = None,
    deploy: bool = False,
    allow_dangerous_empty_build: bool = False,
    partial: bool = False,
):
    s = get_current_session()
    project_id = login(s, ctx.obj["credentials"])
    if git_revision:
        if not Path(filepath).is_dir():
            raise click.ClickException(
                "When deploying a Git revision, the filepath argument must point to a single directory."
            )
        return create_build_from_git_revision(
            s,
            project_id,
            git_revision,
            git_path,
            deploy,
            allow_dangerous_empty_build=allow_dangerous_empty_build,
            dbt_manifest_path=dbt_manifest_path,
            dbt_inclusion_list=dbt_inclusion_list,
        )
    else:
        return create_build_from_local_files(
            s,
            project_id,
            filepath,
            deploy,
            allow_dangerous_empty_build=allow_dangerous_empty_build,
            dbt_manifest_path=dbt_manifest_path,
            dbt_inclusion_list=dbt_inclusion_list,
            partial=partial,
        )


def _deploy_preview_build(preview_build_id: str):
    s = get_current_session()
    return apply_preview_build(s, preview_build_id)


def _echo_tables(table_names: list, datasource: str) -> None:
    click.secho(f"📂 Available Tables From {datasource}", fg="bright_green")
    _echo_list(table_names)


def _echo_table_not_found(table: str, tables: dict, datasource: str) -> None:
    """If table is not found in the available tables, output warning and display available tables."""
    click.echo("")
    click.secho(f"❗{table} was not found in {datasource}'s tables.", fg="red")
    click.echo("")
    _echo_tables(list(tables.keys()), datasource)
    click.echo("")


def _echo_datasources(datasources: list) -> None:
    click.secho("🗒  Available data connections ", fg="bright_green")
    columns = ["Data connection name", "Data connection type", "ID"]
    table = PrettyTable(columns)
    for col in columns:
        table.align[col] = "l"
    for ds in datasources:
        table.add_row(ds)
    click.echo(table)


def _echo_datasource_not_found(datasource: str, datasources: list) -> None:
    """If datasource not found, output warning and available datasources."""
    click.echo("")
    click.secho(f"❗{datasource} was not found in your database connections.", fg="red")
    click.echo("")
    _echo_datasources(datasources)
    click.echo("")
    click.echo(
        "You can add another database connection in your Settings tab on hashboard.com."
    )
    click.echo("")


def _echo_async_build_creation(
    build_results: dict, deploy: bool, query_name="createAsyncBuild"
):
    """Outputs user-friendly build results."""
    if "errors" in build_results and build_results["errors"]:
        _echo_build_errors_and_exit(
            [
                e["extensions"]["userMessage"]
                for e in build_results["errors"]
                if "extensions" in e and "userMessage" in e["extensions"]
            ]
        )
    created_build_id = build_results["data"][query_name]

    click.echo(
        click.style("\n📦 Build ", fg="white")
        + click.style(created_build_id, bold=True)
        + click.style(" queued, waiting to start", fg="white")
    )
    click.echo(f"Follow build in web app: {build_details_uri(created_build_id)}")
    click.echo("")


def _get_empty_status_groups():
    return {
        "modelBundles": [],
        "metrics": [],
        "savedViews": [],
        "dashboards": [],
        "colorPalettes": [],
        "homepageLaunchpads": [],
        "reportSchedules": [],
    }


def _convert_to_resource_update_list(resource_changes: dict):
    result = {
        "added": _get_empty_status_groups(),
        "changed": _get_empty_status_groups(),
        "deleted": _get_empty_status_groups(),
        "unchanged": _get_empty_status_groups(),
    }
    action_to_status = {
        "create": "added",
        "update": "changed",
        "delete": "deleted",
        "unchanged": "unchanged",
    }
    type_to_status_group = {
        "modelBundle": "modelBundles",
        "savedView": "savedViews",
        "dashboard-v2": "dashboards",
        "projectMetric": "metrics",
        "colorPalette": "colorPalettes",
        "homepageLaunchpad": "homepageLaunchpads",
        "reportSchedule": "reportSchedules",
    }
    for rc in resource_changes.values():
        rcType = rc["newContent"]["value"]["type"]
        content = rc["newContent"]["value"]
        if rcType == "reportSchedule":
            report_id = content.get("id")
            content["name"] = content.get("subject", f"Report schedule {report_id}")
        result[action_to_status[rc["action"]]][
            type_to_status_group[rc["newContent"]["value"]["type"]]
        ].append(rc["newContent"]["value"])

    return result


def _echo_async_build_results(
    build_results: dict, deploy=False, query_name="fetchBuild"
):
    """Outputs user-friendly build results."""
    if "errors" in build_results and build_results["errors"]:
        _echo_build_errors_and_exit(
            [
                e["extensions"]["userMessage"]
                for e in build_results["errors"]
                if "extensions" in e and "userMessage" in e["extensions"]
            ]
        )

    click.echo()

    created_build_results = build_results["data"][query_name]

    if created_build_results["errors"]:
        _echo_build_errors_and_exit(created_build_results["errors"])

    click.echo(
        click.style("📦 Build ", fg="bright_green")
        + click.style(created_build_results["id"], bold=True)
        + click.style(" completed successfully.", fg="bright_green")
    )

    click.echo()

    _echo_build_resources(
        _convert_to_resource_update_list(
            created_build_results["changeSet"]["resourceChanges"]
        ),
        deploy,
    )

    if created_build_results["warnings"]:
        _echo_build_warnings(created_build_results["warnings"])

    click.echo("")


def _echo_pull_errors_and_exit(errors: List[str]):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    click.echo("❗ Errors encountered when pulling resources")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    click.secho(
        "Resources that failed to export were not written to local files.",
        fg="red",
    )
    click.echo("")
    if not errors:
        errors = ["Something went wrong, please contact Hashboard for support."]
    _echo_list(errors, color="red")
    click.echo("")
    click.get_current_context().exit(1)


def _echo_build_errors_and_exit(errors: List[str]):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    click.echo("❗ Errors encountered when creating your build")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    if not errors:
        errors = ["Something went wrong, please contact Hashboard for support."]
    _echo_list(errors, color="red")
    click.echo("")
    click.secho("Build failed.", fg="red")
    click.get_current_context().exit(1)


def _echo_datasource_creation_errors_and_exit(errors: List[str]):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――–––", fg="red")
    click.echo("❗ Errors encountered when creating your datasource")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――–––", fg="red")
    if not errors:
        errors = ["Something went wrong, please contact Hashboard for support."]
    _echo_list(errors, color="red")
    click.echo("")
    click.secho("Datasource creation failed.", fg="red")
    click.get_current_context().exit(1)


def _echo_build_warnings(warnings: List[str]):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="yellow")
    click.echo(" ⚠️  Warnings encountered when creating your build")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="yellow")
    if not warnings:
        warnings = ["Warning message missing, please contact Hashboard for support."]
    _echo_list(warnings, color="yellow")
    click.echo("")


def _echo_list(items: List[str], color="white"):
    for item in items:
        lines = item.split("\n")
        click.echo(click.style("*", fg=color) + "  " + lines[0])
        for line in lines[1:]:
            click.echo("   " + line)


def _echo_resources_with_status(resources: dict, status: str, title: str):
    model_bundles = resources[status]["modelBundles"]
    metrics = resources[status]["metrics"]
    saved_views = resources[status]["savedViews"]
    dashboards = resources[status]["dashboards"]
    color_palettes = resources[status]["colorPalettes"]
    homepage_launchpads = resources[status]["homepageLaunchpads"]
    report_schedules = resources[status].get("reportSchedules", [])

    combinedResources = (
        model_bundles
        + metrics
        + saved_views
        + dashboards
        + color_palettes
        + homepage_launchpads
        + report_schedules
    )

    if combinedResources:
        click.echo(title)
        _echo_list(
            [
                click.style("Model - ", fg="bright_black")
                + click.style(r["model"]["name"], fg="white")
                for r in model_bundles
            ]
        )
        _echo_list(
            [
                click.style("Metric - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in metrics
            ]
        )
        _echo_list(
            [
                click.style("View - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in saved_views
            ]
        )
        _echo_list(
            [
                click.style("Dashboard - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in dashboards
            ]
        )
        _echo_list(
            [
                click.style("Report schedule - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in report_schedules
            ]
        )
        _echo_list(
            [
                click.style("Color Palette - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in color_palettes
            ]
        )
        _echo_list(
            [
                click.style("Homepage Launchpad", fg="bright_black")
                for _ in homepage_launchpads
            ]
        )
        click.echo()


def _echo_build_resources(resources: dict, deploy: bool):
    added = click.style("Added:" if deploy else "Will add:", bold=True, fg="green")
    _echo_resources_with_status(resources, "added", added)

    updated = click.style(
        "Updated:" if deploy else "Will update:", bold=True, fg="cyan"
    )
    _echo_resources_with_status(resources, "changed", updated)

    deleted = click.style("Deleted:" if deploy else "Will delete:", bold=True, fg="red")
    _echo_resources_with_status(resources, "deleted", deleted)

    not_modified = click.style("Unchanged:", bold=True)
    _echo_resources_with_status(resources, "unchanged", not_modified)


def _enable_http_logging():
    # From: https://docs.python-requests.org/en/master/api/#api-changes
    from http.client import HTTPConnection

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    if HASHBOARD_VERBOSE_DEBUG_UNSAFE:
        HTTPConnection.debuglevel = 1


def _check_version():
    from pathlib import Path
    import time, requests
    import semver

    ttl = 24 * 60 * 60
    hb_path = Path.home() / ".hashboard"
    version_path = hb_path / ".cache" / "version"

    try:
        old_umask = os.umask(0)
        os.makedirs(hb_path, exist_ok=True, mode=0o700)
        os.umask(old_umask)

        os.makedirs(version_path.parent, exist_ok=True)
    except:
        # Could be a permissions issue, or hard drive full, or weird cosmic bit flip...
        # Just assume we're up-to-date.
        return True

    try:
        prev_mtime = os.path.getmtime(version_path)
    except Exception:
        prev_mtime = None

    if prev_mtime is None or time.time() - prev_mtime > ttl:
        # delete stale cache
        try:
            version_path.unlink()  # missing_ok not available in Python 3.7
        except:
            pass

    try:
        with open(version_path, "r") as f:
            return semver.compare(VERSION, f.readline().strip()) >= 0
    except:
        pass

    # cache was stale or did not exist; fetch from pypi
    try:
        with open(version_path, "w+") as f:
            PACKAGE_JSON_URL = "https://pypi.org/pypi/hashboard-cli/json"
            resp = requests.get(PACKAGE_JSON_URL, timeout=1)
            data = resp.json()
            latest_version = _get_latest_public_version(data["releases"])
            f.write(latest_version)
            return semver.compare(VERSION, latest_version) >= 0
    except Exception as e:
        logging.warning("Unable to check the latest version of the CLI.", e)
        # Unable to pull version information currently, just return true
        return True


def _get_latest_public_version(releases: Dict[str, Dict]) -> str:
    from semver import Version

    max_version = Version.parse("0.0.1")
    for release_version_str, release in releases.items():
        try:
            release_version = Version.parse(release_version_str)
        except ValueError:
            # if a version string isn't valid, then skip it
            continue
        if [item for item in release if item.get("yanked", False)]:
            # if any distributions in this release are yanked, skip it
            continue

        if release_version.compare(max_version) >= 0:
            max_version = release_version

    return str(max_version)
