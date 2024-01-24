from argparse import Namespace
from asyncio import TaskGroup

from rich.console import Console
from rich.text import Text

from hacktegic._internal.base_command import BaseCommand
from hacktegic._internal.config import ConfigManager
from hacktegic._internal.credentials import Credentials
from hacktegic.cloud.api_clients.networks import NetworksAPIClient

class NetworksUpdateCommand(BaseCommand):
    async def run(tg: TaskGroup, args: Namespace) -> None:
        creds = Credentials()
        config_manager = ConfigManager()
        await creds.load()
        await config_manager.load()

        client = NetworksAPIClient(creds, config_manager)

        console = Console()

        network = {}
        if hasattr(args, "address") and args.address:
            network["address"] = args.address
        if hasattr(args, "description"):
            network["description"] = args.description

        result = await client.update(args.network_id, network)

        if result:
            text = Text("Network successfully updated!")
            text.stylize("green")
        else:
            text = Text("Something went wrong!")
            text.stylize("bold red")
        console.print(text)