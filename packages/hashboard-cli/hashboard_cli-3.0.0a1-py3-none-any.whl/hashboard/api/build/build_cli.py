import click
from pathlib import Path, PurePath
import subprocess
import time
from typing import List, Optional

from hashboard.api import (
    apply_preview_build,
    create_build_from_git_revision,
    create_build_from_local_files,
    login,
)
from hashboard.api.analytics.cli_with_tracking import (
    CommandWithTracking,
    GroupWithTracking,
)
from hashboard.api.build.utils import (
    echo_async_build_creation,
    echo_async_build_results,
    poll_for_build_status,
)
from hashboard.credentials import get_credentials
from hashboard.dbt_run_results_parser import parse_dbt_run_results
from hashboard.session import get_current_session
from hashboard.utils.hbproject import (
    DBT_ROOT_KEY,
    DEFAULT_BUILD_ID_KEY,
    MAX_DEFAULT_BUILD_SECS,
    read_hashboard_project_value,
)
from hashboard.utils.session_state import (
    delete_session_state_value,
    read_session_state_value,
    write_session_state_value,
)

class GroupWithDefaultCommand(GroupWithTracking):
    def __init__(self, *args, **kwargs):
        self.default_command = kwargs.pop('default_command', None)
        super().__init__(*args, **kwargs)

    def parse_args(self, ctx, args):
        # If no arguments are given, invoke the default subcommand
        if not args and self.default_command:
            args.insert(0, self.default_command)
        # If the first argument is not a known subcommand, prepend the default subcommand
        elif args and args[0] not in self.commands and self.default_command:
            args.insert(0, self.default_command)
        super().parse_args(ctx, args)


@click.group(cls=GroupWithDefaultCommand, default_command='create')
@click.pass_context
def build(ctx):
    """Commands for managing Hashboard builds\u2024 By default, creates a new build."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(preview_async)

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
run_dbt_parse_option = click.option(
    "--dbt",
    "run_dbt_parse",
    required=False,
    help="If specified, runs `dbt parse` in the current directory and uses the resulting artifacts to build associated Hashboard models if using Hashboard dbt integration.",
    is_flag=True,
    default=False,
)
dbt_artifacts_option = click.option(
    "--dbt-artifacts",
    "dbt_artifacts_path",
    required=False,
    help="Path to folder containing dbt manifest and dbt run results JSON files, used to build associated Hashboard models if using Hashboard dbt integration.",
    type=click.Path(exists=True, readable=True, file_okay=False, dir_okay=True),
)
dbt_model_filter_option = click.option(
    "--dbt-models",
    "dbt_model_filter",
    required=False,
    help="A comma separated list of dbt models to include in the build. Will be ignored if neither --dbt nor --dbt-manifest flags are set. If not provided, all dbt models will be built.",
    type=click.STRING,
)
allow_dangerous_empty_build_option = click.option(
    "--allow-dangerous-empty-build",
    "allow_dangerous_empty_build",
    is_flag=True,
    default=False,
    help="Allow builds with no config files. WARNING: this will allow a build to delete all of your resources, including non-dataops resources that depend on your dataops resources!",
)
apply_immediate_option = click.option(
    "--apply-immediately",
    "apply_immediate",
    is_flag=True,
    default=False,
    help="Applies build immediately after creation",
)
full_rebuild_option = click.option(
    "--full-rebuild",
    "full_rebuild",
    is_flag=True,
    default=False,
    help="Rebuilds all code-controlled resources, deleting any code-controlled resources that are no longer included in your build.",
)
local_path_argument = click.argument("filepaths", type=click.STRING, nargs=-1)


@build.command(
    "create",
    cls=CommandWithTracking,
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@git_revision_option
@git_path_option
@dbt_artifacts_option
@local_path_argument
@run_dbt_parse_option
@dbt_model_filter_option
@allow_dangerous_empty_build_option
@full_rebuild_option
@apply_immediate_option
@click.pass_context
def preview_async(
    ctx,
    git_revision,
    git_path,
    dbt_artifacts_path,
    filepaths,
    run_dbt_parse,
    dbt_model_filter,
    allow_dangerous_empty_build,
    full_rebuild,
    apply_immediate,
):
    """Creates and validates a new build. This is the default command if you just run `hb build`."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])

    is_partial = not full_rebuild

    dbt_manifest_path, dbt_inclusion_list = _handle_dbt_args(
        dbt_artifacts_path, run_dbt_parse, dbt_model_filter, is_partial
    )

    # Since click doesn't support defaults for unlimited args we manually set the default
    # filepath argument
    paths_as_list = list(filepaths) if filepaths else ["."]

    click.echo("🏗️  Creating build...")
    build_results = _create_build_using_options(
        ctx,
        paths_as_list,
        git_revision=git_revision,
        git_path=git_path,
        deploy=apply_immediate,
        dbt_manifest_path=dbt_manifest_path,
        dbt_inclusion_list=dbt_inclusion_list,
        allow_dangerous_empty_build=allow_dangerous_empty_build,
        partial=is_partial,
    )
    echo_async_build_creation(build_results, apply_immediate)

    build_id = build_results["data"]["createAsyncBuild"]
    build_results = poll_for_build_status(build_id)

    if not apply_immediate:
        write_session_state_value(
            DEFAULT_BUILD_ID_KEY, f"{build_id},{int(time.time())}"
        )
    echo_async_build_results(build_results, deploy=apply_immediate)


@build.command(
    "apply",
    cls=CommandWithTracking,
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.argument("build_id", type=click.STRING, required=False)
@click.pass_context
def apply(ctx: click.Context, build_id: Optional[str]):
    """Applies the changes from a build to your project. If no build_id is provided, this command will apply the most recently created build in your session, if one exists."""
    ctx.obj["credentials"] = get_credentials(ctx.obj["credentials_filepath"])

    if build_id is None:
        default_build_id = None
        try:
            default_build_id, timestamp = read_session_state_value(
                DEFAULT_BUILD_ID_KEY
            ).split(",")
            if time.time() - int(timestamp) > MAX_DEFAULT_BUILD_SECS:
                default_build_id = None
        except:
            pass

        if default_build_id is None:
            raise click.ClickException(
                "Could not find most recent build to apply, please explicitly specify a build id to apply to the project."
            )
        click.echo("No build id specified, applying most recent build.")
        build_id = default_build_id

    deploy_results = _apply_preview_build(ctx, build_id)
    echo_async_build_results(deploy_results, deploy=True, query_name="applyBuild")
    delete_session_state_value(DEFAULT_BUILD_ID_KEY)
    click.echo("")
    click.echo(click.style("✅ Build applied successfully.", fg="bright_green"))


def _create_build_using_options(
    ctx: click.Context,
    filepaths: List[str],
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
        if not len(filepaths) == 1 and Path(filepaths[0]).is_dir():
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
            filepaths,
            deploy,
            allow_dangerous_empty_build=allow_dangerous_empty_build,
            dbt_manifest_path=dbt_manifest_path,
            dbt_inclusion_list=dbt_inclusion_list,
            partial=partial,
        )


def _apply_preview_build(ctx: click.Context, preview_build_id: str):
    s = get_current_session()
    login(s, ctx.obj["credentials"])
    return apply_preview_build(s, preview_build_id)


def _handle_dbt_args(
    dbt_artifacts_path: str,
    run_dbt_parse: bool,
    dbt_model_filter: str,
    partial: bool,
):
    """Convenience wrapper for running `dbt parse` before `hb preview` or `hb deploy`.
    Must be run from your Hashboard project directory.

    Flags passed in after the hb subcommand will be passed onwards to dbt.
    """

    # Exit early if neither option is provided
    if not run_dbt_parse and dbt_artifacts_path is None:
        return None, None

    # Raise warning if multiple options are provided
    if run_dbt_parse and dbt_artifacts_path is not None:
        click.echo()
        click.echo(
            "🚨 `--dbt-artifacts` is redundant when running with `--dbt` and will be ignored."
        )
        click.echo()

    inclusion_list = (
        dbt_model_filter.split(",")
        if (dbt_artifacts_path or run_dbt_parse) and dbt_model_filter
        else None
    )

    dbt_root = read_hashboard_project_value(DBT_ROOT_KEY)
    target_dir = Path(dbt_root) / "target" if dbt_root else Path("target")

    if run_dbt_parse:
        # Will always run in current directory
        click.echo("🐇 Running `dbt parse` to generate a manifest file.")

        click.echo()

        dbt_command = f"dbt parse"
        click.echo(f"$ {dbt_command}")
        click.echo("--- dbt output ---")

        ret_code = subprocess.Popen(dbt_command.split(" "), cwd=dbt_root).wait()
        click.echo("--- end of dbt output ---")

        if ret_code != 0:
            raise click.ClickException(f"dbt returned nonzero exit code ({ret_code})")
    elif dbt_artifacts_path is not None:
        # user specified --dbt-manifest explicitly
        target_dir = dbt_artifacts_path

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
    click.echo(f"✅ Using dbt artifacts at {target_dir}\n")
    return manifest_path, inclusion_list
