# 🔐 VPS Remote SSH Manager — by [Aayco](https://t.me/Aayco)

A powerful, fully asynchronous SSH management tool for VPS and Linux servers. Built with ❤️ by Aayco using modern Python libraries.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)  
![License](https://img.shields.io/badge/License-MIT-green.svg)  
![SQLite](https://img.shields.io/badge/SQLite-persistent-orange.svg)  
![Async](https://img.shields.io/badge/AsyncSSH-fast%20and%20secure-lightgrey.svg)  
![Rich UI](https://img.shields.io/badge/Rich-Beautiful%20Output-purple.svg)

---

## ✨ Features

🧠 **Interactive Terminal Shell** with autocomplete and history  
💾 **Persistent Profiles** saved in local `SQLite` using `aiosqlite`  
🔐 **SSH Login via Password or Key** with `asyncssh`  
🖥️ **Run Commands**, view output in color-coded format  
📤 **Upload Files** from local to remote  
📥 **Download Files** from remote to local  
🎨 **Beautiful CLI** with `Rich` and `Prompt Toolkit`  
🧱 **Modular & Class-Based** clean Python code  
🐍 **Fully async / non-blocking** with `asyncio`

---

## 📂 Project Structure

```bash
ssh/
├── tool.py               # Main CLI entry (Typer)
├── core/
│   ├── database.py       # DatabaseManager (aiosqlite)
│   ├── client.py         # SSHClient (asyncssh)
│   └── ui.py             # VPSUI interactive shell
├── data/
│   └── profiles.db       # Auto-created SQLite DB
├── README.md             # This file 📘
└── requirements.txt      # All dependencies 📦
```


---

## ⚙️ Installation

```sh
git clone https://github.com/Aayco/ssh.git
cd ssh
pip install -r requirements.txt
```


---

## 🚀Usage

```usage
🧠 Interactive Shell

python tool.py shell

Features:

Browse and reuse profiles

View history

Upload / download

Auto-saves profiles
```



---

## ⚡ Run Quick CLI Commands

**Run a command:**

```sh
python tool.py cli --host 1.2.3.4 --user root --password mypass --cmd "ls -la"
```

**Upload a file:**

```sh
python tool.py cli --host 1.2.3.4 --user root --password mypass --upload ./myfile.py --to /root/myfile.py
```

**Download a file:**

```sh
python tool.py cli --host 1.2.3.4 --user root --password mypass --download /root/app.log --to ./log.txt
```


---

## 🗂️ Profiles & History

```history
Every connection is saved as a profile with:

Hostname

Username

Password/SSH key (optional)

Timestamped command history


You can view them in the shell:

Command> profiles
Command> history

You can upload or download or run codes in shell:

Command> download
Command> upload
Command> run
```


---

## 📬 Contact Me

👤 Author: Amiru Mohammed

🌐 GitHub: [ssh](https://github.com/Aayco/ssh)

✈️ Telegram: [Aayco](https://t.me/Aayco) | [Aayco](https://t.me/Unlowly)


---

## 📄 License

MIT License — Use freely, give credit. Contributions welcome!

> Made with Python 🐍, Rich 🎨, and AsyncSSH 🔐 by Aayco
