import os
from typing import Annotated, Optional

import httpx
import requests
import typer
from rich.console import Console
from rich.table import Table

from kleinkram.api_client import AuthenticatedClient
from kleinkram.error_handling import AccessDeniedException

mission = typer.Typer(
    name="mission",
    help="Mission operations",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@mission.command("tag")
def addTag(
    mission_uuid: Annotated[str, typer.Argument()],
    tagtype_uuid: Annotated[str, typer.Argument()],
    value: Annotated[str, typer.Argument()],
):
    """Tag a mission"""
    try:
        client = AuthenticatedClient()
        response = client.post(
            "/tag/addTag",
            json={"mission": mission_uuid, "tagType": tagtype_uuid, "value": value},
        )
        if response.status_code < 400:
            print("Tagged mission")
        else:
            print(response.json())
            print("Failed to tag mission")
            raise Exception("Failed to tag mission")
    except httpx.HTTPError as e:
        print(e)
        print("Failed to tag mission")
        raise e


@mission.command("list")
def list_missions(
    project: Optional[str] = typer.Option(None, help="Name of Project"),
    verbose: Optional[bool] = typer.Option(
        False, help="Outputs a table with more information"
    ),
):
    """
    List all missions with optional filter for project.
    """

    url = "/mission"
    if project:
        url += f"/filteredByProjectName/{project}"
    else:
        url += "/all"

    client = AuthenticatedClient()

    try:

        response = client.get(url)
        response.raise_for_status()

    except httpx.HTTPError:

        raise AccessDeniedException(
            f"Failed to fetch mission."
            f"Consider using the following command to list all missions: 'klein mission list --verbose'\n",
            f"{response.json()['message']} ({response.status_code})",
        )

    data = response.json()
    missions_by_project_uuid = {}
    for mission in data:
        project_uuid = mission["project"]["uuid"]
        if project_uuid not in missions_by_project_uuid:
            missions_by_project_uuid[project_uuid] = []
        missions_by_project_uuid[project_uuid].append(mission)

    if len(missions_by_project_uuid.items()) == 0:
        print(f"No missions found for project '{project}'. Does it exist?")
        return

    print("missions by Project:")
    if not verbose:
        for project_uuid, missions in missions_by_project_uuid.items():
            print(f"* {missions_by_project_uuid[project_uuid][0]['project']['name']}")
            for mission in missions:
                print(f"  - {mission['name']}")

    else:
        table = Table("UUID", "name", "project", "creator", "createdAt")
        for project_uuid, missions in missions_by_project_uuid.items():
            for mission in missions:
                table.add_row(
                    mission["uuid"],
                    mission["name"],
                    mission["project"]["name"],
                    mission["creator"]["name"],
                    mission["createdAt"],
                )
        console = Console()
        console.print(table)


@mission.command("byUUID")
def mission_by_uuid(
    uuid: Annotated[str, typer.Argument()],
    json: Optional[bool] = typer.Option(False, help="Output as JSON"),
):
    """
    Get mission name, project name, creator and table of its files given a Mission UUID

    Use the JSON flag to output the full JSON response instead.

    Can be run with API Key or with login.
    """
    url = "/mission/byUUID"
    client = AuthenticatedClient()
    response = client.get(url, params={"uuid": uuid})

    try:
        response.raise_for_status()
    except httpx.HTTPError:
        raise AccessDeniedException(
            f"Failed to fetch mission."
            f"Consider using the following command to list all missions: 'klein mission list --verbose'\n",
            f"{response.json()['message']} ({response.status_code})",
        )

    data = response.json()

    if json:
        print(data)
    else:
        print(f"mission: {data['name']}")
        print(f"Creator: {data['creator']['name']}")
        print("Project: " + data["project"]["name"])
        table = Table("Filename", "Size", "date")
        for file in data["files"]:
            table.add_row(file["filename"], f"{file['size']}", file["date"])
        console = Console()
        console.print(table)


@mission.command("download")
def download(
    mission_uuid: Annotated[str, typer.Argument()],
    local_path: Annotated[str, typer.Argument()],
):
    """

    Downloads all files of a mission to a local path.
    The local path must be an empty directory.

    """

    if not os.path.isdir(local_path):
        raise ValueError(f"Local path '{local_path}' is not a directory.")
    if not os.listdir(local_path) == []:
        raise ValueError(f"Local path '{local_path}' is not empty, but must be empty.")

    client = AuthenticatedClient()
    response = client.get("/file/downloadWithToken", params={"uuid": mission_uuid})

    try:
        response.raise_for_status()
    except httpx.HTTPError as e:
        raise AccessDeniedException(
            f"Failed to download file."
            f"Consider using the following command to list all missions: 'klein mission list --verbose'\n",
            f"{response.json()['message']} ({response.status_code})",
        )

    paths = response.json()

    print(f"Downloading files to {local_path}:")
    for path in paths:

        filename = path.split("/")[-1].split("?")[0]
        print(f" - {filename}")

        response = requests.get(path)
        with open(os.path.join(local_path, filename), "wb") as f:
            f.write(response.content)
            print(f"   Downloaded {filename}")
