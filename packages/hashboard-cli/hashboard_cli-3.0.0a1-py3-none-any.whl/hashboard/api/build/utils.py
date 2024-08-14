import sys
import time
from typing import List, Literal, Union
import click
from hashboard.api import (
    build_details_uri,
    fetch_build,
    fetch_build_status,
)
from hashboard.session import get_current_session
from hashboard.utils.cli import echo_list


def echo_async_build_creation(
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

    click.echo("")


def poll_for_build_status(build_id):
    s = get_current_session()

    spinner = _spinning_cursor()
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


def _spinning_cursor():
    while True:
        for cursor in "|/-\\":
            yield cursor


def echo_async_build_results(
    build_results: dict,
    deploy=False,
    query_name: Literal["fetchBuild", "applyBuild"] = "fetchBuild",
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
    created_build_id = created_build_results["id"]

    if query_name == "applyBuild":
        click.echo(f"More details: {build_details_uri(created_build_id)}")
        click.echo()

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

    if query_name != "applyBuild":
        click.echo("Run `hb build apply` to persist these changes.")


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


def _echo_build_errors_and_exit(errors: List[str]):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    click.echo("❗ Errors encountered when creating your build")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    if not errors:
        errors = ["Something went wrong, please contact Hashboard for support."]
    echo_list(errors, color="red")
    click.echo("")
    click.secho("Build failed.", fg="red")
    click.get_current_context().exit(1)


def _echo_build_warnings(warnings: List[str]):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="yellow")
    click.echo(" ⚠️  Warnings encountered when creating your build")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="yellow")
    if not warnings:
        warnings = ["Warning message missing, please contact Hashboard for support."]
    echo_list(warnings, color="yellow")
    click.echo("")


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
        echo_list(
            [
                click.style("Model - ", fg="bright_black")
                + click.style(r["model"]["name"], fg="white")
                for r in model_bundles
            ]
        )
        echo_list(
            [
                click.style("Metric - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in metrics
            ]
        )
        echo_list(
            [
                click.style("View - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in saved_views
            ]
        )
        echo_list(
            [
                click.style("Dashboard - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in dashboards
            ]
        )
        echo_list(
            [
                click.style("Report schedule - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in report_schedules
            ]
        )
        echo_list(
            [
                click.style("Color Palette - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in color_palettes
            ]
        )
        echo_list(
            [
                click.style("Homepage Launchpad", fg="bright_black")
                for _ in homepage_launchpads
            ]
        )
        click.echo()
