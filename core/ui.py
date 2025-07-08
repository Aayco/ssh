from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from rich.prompt import Prompt
from rich.console import Console

from core.database import DatabaseManager
from core.client import SSHClient

class VPSUI:
    def __init__(self):
        self.console = Console()
        self.session = PromptSession()
        self.completer = WordCompleter(
            ["connect", "run", "upload", "download", "profiles", "history", "exit"],
            ignore_case=True,
        )
        self.db = DatabaseManager()
        self.ssh = SSHClient()
        self.active_profile_id = None

    async def Launch(self):
        await self.db.Init()
        self.console.print("[bold cyan]🧠 VPS Shell Ready — Type 'connect' or 'profiles' to start[/]")

        while True:
            try:
                cmd = await self.session.prompt_async("🛠️ Command> ", completer=self.completer)
                cmd = cmd.strip().lower()

                if cmd == "connect":
                    await self.HandleConnect()
                elif cmd == "run":
                    await self.HandleRun()
                elif cmd == "upload":
                    await self.HandleUpload()
                elif cmd == "download":
                    await self.HandleDownload()
                elif cmd == "profiles":
                    await self.ListProfiles()
                elif cmd == "history":
                    await self.ShowHistory()
                elif cmd == "exit":
                    await self.ssh.Close()
                    self.console.print("[yellow]👋 Exiting...[/]")
                    break
                else:
                    self.console.print("[red]❓ Unknown command[/]")

            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[red]👋 Exiting shell...[/]")
                break

    async def HandleConnect(self):
        name = Prompt.ask("💾 Save profile name")
        host = Prompt.ask("🌐 Host")
        user = Prompt.ask("👤 Username")
        auth_type = Prompt.ask("🔐 Auth method", choices=["password", "key"], default="password")

        password = None
        key_path = None
        if auth_type == "password":
            password = Prompt.ask("🔒 Password", password=True)
        else:
            key_path = Prompt.ask("🔑 SSH key path")

        await self.ssh.Connect(host, user, password, key_path)

        await self.db.SaveProfile(name, host, user, password, key_path)
        profile = await self.db.GetProfileByName(name)
        if profile:
            self.active_profile_id = profile[0]
            self.console.print(f"[green]✔ Active profile: {name} (ID {self.active_profile_id})[/]")

    async def HandleRun(self):
        if not self.ssh.conn:
            self.console.print("[red]❌ Not connected[/]")
            return
        command = Prompt.ask("📥 Command to run")
        await self.ssh.RunCommand(command)
        if self.active_profile_id:
            await self.db.SaveHistory(self.active_profile_id, command)

    async def HandleUpload(self):
        if not self.ssh.conn:
            self.console.print("[red]❌ Not connected[/]")
            return
        local = Prompt.ask("📂 Local file path")
        remote = Prompt.ask("🗂️ Remote path")
        await self.ssh.UploadFile(local, remote)

    async def HandleDownload(self):
        if not self.ssh.conn:
            self.console.print("[red]❌ Not connected[/]")
            return
        remote = Prompt.ask("🗂️ Remote file path")
        local = Prompt.ask("📂 Local destination")
        await self.ssh.DownloadFile(remote, local)

    async def ListProfiles(self):
        profiles = await self.db.GetProfiles()
        if not profiles:
            self.console.print("[yellow]⚠ No saved profiles[/]")
            return
        self.console.print("[bold green]🗂️ Saved Profiles:[/]")
        for pid, name, host, user in profiles:
            self.console.print(f"[cyan]{name}[/] ({host}, {user}) [dim](ID {pid})[/]")

    async def ShowHistory(self):
        if not self.active_profile_id:
            self.console.print("[yellow]⚠ Connect to a profile first[/]")
            return
        history = await self.db.GetHistory(self.active_profile_id)
        if not history:
            self.console.print("[dim]No history found for this profile.[/]")
            return
        self.console.print("[bold magenta]📜 Command History:[/]")
        for command, timestamp in history:
            self.console.print(f"[dim]{timestamp}[/] → [white]{command}[/]")
