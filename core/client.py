import asyncssh
from rich.console import Console
from typing import Optional

class SSHClient:
    def __init__(self):
        self.conn: Optional[asyncssh.SSHClientConnection] = None
        self.sftp = None
        self.console = Console()

    async def Connect(self, host: str, user: str, password: Optional[str] = None, key_path: Optional[str] = None):
        try:
            if key_path:
                self.conn = await asyncssh.connect(host, username=user, client_keys=[key_path])
            else:
                self.conn = await asyncssh.connect(host, username=user, password=password)
            self.sftp = await self.conn.start_sftp_client()
            self.console.print(f"[green]✅ Connected to {host} as {user}[/]")
        except Exception as e:
            self.console.print(f"[red]❌ SSH connection failed: {e}[/]")
            raise

    async def RunCommand(self, command: str) -> str:
        if not self.conn:
            raise RuntimeError("SSH not connected")
        try:
            result = await self.conn.run(command)
            if result.stdout:
                self.console.print(f"[blue]{result.stdout.rstrip()}[/]")
            if result.stderr:
                self.console.print(f"[red]{result.stderr.rstrip()}[/]")
            return result.stdout
        except Exception as e:
            self.console.print(f"[red]❌ Command failed: {e}[/]")
            return ""

    async def UploadFile(self, local_path: str, remote_path: str):
        if not self.sftp:
            raise RuntimeError("SFTP not connected")
        await self.sftp.put(local_path, remote_path)
        self.console.print(f"[green]📤 Uploaded {local_path} → {remote_path}[/]")

    async def DownloadFile(self, remote_path: str, local_path: str):
        if not self.sftp:
            raise RuntimeError("SFTP not connected")
        await self.sftp.get(remote_path, local_path)
        self.console.print(f"[green]📥 Downloaded {remote_path} → {local_path}[/]")

    async def Close(self):
        if self.conn:
            self.conn.close()
            await self.conn.wait_closed()
            self.console.print("[yellow]🔒 SSH session closed[/]")
