import asyncio
import typer
from rich.console import Console
from rich.prompt import Prompt

from core.database import DatabaseManager
from core.client import SSHClient
from core.ui import VPSUI

app = typer.Typer()
console = Console()

@app.command()
def Shell():
    """Launch interactive VPS terminal shell."""
    ui = VPSUI()
    asyncio.run(ui.Launch())

@app.command()
def CLI(
    host: str = typer.Option(..., prompt="🌐 Host"),
    user: str = typer.Option(..., prompt="👤 Username"),
    password: str = typer.Option(None, prompt="🔒 Password (leave empty for SSH key)", hide_input=True),
    key: str = typer.Option(None, help="SSH private key path (if using SSH key login)"),
    cmd: str = typer.Option(None, help="Command to run on the server"),
    upload: str = typer.Option(None, help="Local file to upload"),
    to: str = typer.Option(None, help="Remote path (for upload/download)"),
    download: str = typer.Option(None, help="Remote file to download"),
):
    """Run a command or upload/download a file over SSH."""
    async def Run():
        db = DatabaseManager()
        await db.Init()

        ssh = SSHClient()
        await ssh.Connect(host, user, password if password else None, key)

        profile_name = f"{user}@{host}"
        await db.SaveProfile(profile_name, host, user, password, key)
        profile = await db.GetProfileByName(profile_name)
        profile_id = profile[0] if profile else None

        if cmd:
            await ssh.RunCommand(cmd)
            if profile_id:
                await db.SaveHistory(profile_id, cmd)

        if upload and to:
            await ssh.UploadFile(upload, to)

        if download and to:
            await ssh.DownloadFile(download, to)

        await ssh.Close()

    asyncio.run(Run())

if __name__ == "__main__":
    app()
