#!/usr/bin/env python3

-- coding: utf-8 --

"""
RIA MASTER PC v4.8 - UNIFIED CLOUD SECURITY & AUTONOMOUS ORCHESTRATOR
Complete Single-File Source Code.
Includes: Persistent SQLite Memory, Linux/Kali Arsenal Auto-Discovery,
Autonomous ReAct Tool Execution Loop, Self-Healing, File Intelligence,
Background Watchdog, and Embedded Cloud Web Dashboard.
"""

import os
import sys
import json
import time
import shutil
import sqlite3
import logging
import threading
import platform
import subprocess

from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

=========================================================

1. CONFIGURATION & ENVIRONMENT SETUP

=========================================================

RIA_NAME = "RIA MASTER PC"
RIA_VERSION = "4.8"

ROOT = Path(file).resolve().parent
DATA_DIR = ROOT / "ria_data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "ria_memory.db"
LOG_PATH = DATA_DIR / "ria.log"

API_KEY = os.getenv("OPENAI_API_KEY", "")
AI_BASE_URL = os.getenv(
"RIA_AI_BASE_URL",
"https://api.openai.com/v1/chat/completions"
)
AI_MODEL = os.getenv("RIA_AI_MODEL", "gpt-4o-mini")

REMOTE_HOST = os.getenv("RIA_HOST", "0.0.0.0")  # Cloud & Codespaces Ready
REMOTE_PORT = int(os.getenv("RIA_PORT", "8080"))
REMOTE_TOKEN = os.getenv("RIA_REMOTE_TOKEN", "")

MAX_FILE_SIZE = 2 * 1024 * 1024
COMMAND_TIMEOUT = 180  # Max seconds for terminal command execution

logging.basicConfig(
filename=str(LOG_PATH),
level=logging.INFO,
format="%(asctime)s %(levelname)s %(message)s"
)

log = logging.getLogger("RIA")

def stamp():
return datetime.now().isoformat(timespec="seconds")

def safe_error(exc):
return str(exc)[:1000]

=========================================================

2. DATABASE AND PERSISTENT MEMORY

=========================================================

class Database:

def __init__(self):  
    self.lock = threading.RLock()  
    self.initialize()  

def connect(self):  
    conn = sqlite3.connect(  
        str(DB_PATH),  
        timeout=15  
    )  
    conn.row_factory = sqlite3.Row  
    return conn  

def initialize(self):  
    with self.connect() as db:  
        db.execute("""  
            CREATE TABLE IF NOT EXISTS messages (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                role TEXT NOT NULL,  
                content TEXT NOT NULL,  
                created_at TEXT NOT NULL  
            )  
        """)  

        db.execute("""  
            CREATE TABLE IF NOT EXISTS memories (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                content TEXT NOT NULL,  
                created_at TEXT NOT NULL  
            )  
        """)  

        db.execute("""  
            CREATE TABLE IF NOT EXISTS audit (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                level TEXT,  
                event TEXT,  
                created_at TEXT  
            )  
        """)  

        db.execute("""  
            CREATE TABLE IF NOT EXISTS settings (  
                key TEXT PRIMARY KEY,  
                value TEXT  
            )  
        """)  

def add_message(self, role, content):  
    with self.lock, self.connect() as db:  
        db.execute(  
            "INSERT INTO messages VALUES(NULL,?,?,?)",  
            (role, content, stamp())  
        )  

def history(self, limit=30):  
    with self.lock, self.connect() as db:  
        rows = db.execute("""  
            SELECT role, content  
            FROM messages  
            ORDER BY id DESC  
            LIMIT ?  
        """, (limit,)).fetchall()  

    return list(reversed([dict(x) for x in rows]))  

def clear_history(self):  
    with self.lock, self.connect() as db:  
        db.execute("DELETE FROM messages")  

def add_memory(self, content):  
    with self.lock, self.connect() as db:  
        db.execute(  
            "INSERT INTO memories VALUES(NULL,?,?)",  
            (content, stamp())  
        )  

def memories(self):  
    with self.lock, self.connect() as db:  
        rows = db.execute("""  
            SELECT id, content, created_at  
            FROM memories ORDER BY id DESC  
        """).fetchall()  
    return [dict(x) for x in rows]  

def audit(self, level, event):  
    log.info("%s: %s", level, event)  
    with self.lock, self.connect() as db:  
        db.execute(  
            "INSERT INTO audit VALUES(NULL,?,?,?)",  
            (level, event, stamp())  
        )

=========================================================

3. RESOURCE MANAGER

=========================================================

class ResourceManager:

def get_metrics(self):  
    result = {  
        "platform": platform.platform(),  
        "python": sys.version.split()[0],  
        "cpu_percent": 0.0,  
        "ram_percent": 0.0,  
        "ram_total_gb": 0.0,  
        "disk_percent": 0.0,  
        "disk_free_gb": 0.0,  
        "gpu": "Not detected"  
    }  

    try:  
        import psutil  

        result["cpu_percent"] = psutil.cpu_percent(  
            interval=0.2  
        )  

        memory = psutil.virtual_memory()  

        result["ram_percent"] = memory.percent  
        result["ram_total_gb"] = round(  
            memory.total / (1024 ** 3), 2  
        )  

        disk = psutil.disk_usage(str(ROOT))  

        result["disk_percent"] = disk.percent  
        result["disk_free_gb"] = round(  
            disk.free / (1024 ** 3), 2  
        )  

    except ImportError:  
        result["monitoring_note"] = (  
            "Install psutil for detailed metrics."  
        )  

    result["gpu"] = self.detect_gpu()  

    return result  

def detect_gpu(self):  
    for command in ("nvidia-smi", "rocm-smi"):  
        try:  
            output = subprocess.run(  
                [command],  
                capture_output=True,  
                text=True,  
                timeout=3  
            )  

            if output.returncode == 0:  
                return command + " detected"  

        except (FileNotFoundError, subprocess.TimeoutExpired):  
            pass  

    return "No supported GPU monitor detected"

=========================================================

4. LINUX & KALI ARSENAL INTEGRATION

=========================================================

class LinuxIntegration:

def information(self):  
    return {  
        "system": platform.system(),  
        "release": platform.release(),  
        "machine": platform.machine(),  
        "distribution": self.distribution(),  
        "is_root": (os.geteuid() == 0) if hasattr(os, "geteuid") else False  
    }  

def distribution(self):  
    try:  
        import distro  
        return distro.name() or "Unknown"  
    except ImportError:  
        return platform.platform()

class SecurityArsenal:
"""
Comprehensive Security & Kali Linux Arsenal Registry + Auto-Discovery.
Covers information gathering, web analysis, exploitation, password cracking,
wireless sniffing, reverse engineering, and cloud utilities.
"""

ARSENAL_CATALOG = {  
    "Information Gathering & OSINT": [  
        "nmap", "masscan", "rustscan", "amass", "subfinder", "theHarvester",  
        "recon-ng", "shodan", "whois", "dig", "nslookup", "netdiscover", "arp-scan"  
    ],  
    "Web & API Vulnerability Analysis": [  
        "sqlmap", "nikto", "dirb", "gobuster", "ffuf", "feroxbuster", "wfuzz",  
        "wpscan", "nuclei", "httpx", "katana", "whatweb", "wafw00f", "commix", "xsstrike"  
    ],  
    "Exploitation Frameworks": [  
        "msfconsole", "msfvenom", "searchsploit", "routersploit", "netexec",  
        "evil-winrm", "impacket-smbexec", "impacket-psexec"  
    ],  
    "Password Cracking & Crypto": [  
        "john", "hashcat", "hydra", "medusa", "ncrack", "cewl", "crunch", "hashid"  
    ],  
    "Wireless & Network Sniffing": [  
        "aircrack-ng", "airodump-ng", "wireshark", "tshark", "tcpdump",  
        "ettercap", "arpspoof", "bettercap", "netcat", "nc", "socat", "proxychains"  
    ],  
    "Reverse Engineering & Forensics": [  
        "gdb", "radare2", "ghidra", "binwalk", "volatility", "exiftool", "strings", "strace"  
    ],  
    "Cloud & DevOps Utilities": [  
        "curl", "wget", "git", "python3", "bash", "docker", "kubectl", "aws", "az", "gcloud"  
    ]  
}  

def __init__(self, db):  
    self.db = db  
    self.discovered_tools = self.scan_installed_arsenal()  

def scan_installed_arsenal(self):  
    installed = {}  
    for category, tools in self.ARSENAL_CATALOG.items():  
        installed[category] = {}  
        for tool in tools:  
            path = shutil.which(tool)  
            installed[category][tool] = path if path else "Not Installed (Auto-Installable)"  
    return installed  

def get_available_summary(self):  
    available = {}  
    for category, tools in self.discovered_tools.items():  
        found = [t for t, p in tools.items() if not p.startswith("Not")]  
        available[category] = found  
    return available  

def execute_command(self, command, cwd=None):  
    self.db.audit("EXEC", f"Running command: {command}")  
    work_dir = cwd if cwd and Path(cwd).exists() else str(ROOT)  

    try:  
        process = subprocess.run(  
            command,  
            shell=True,  
            cwd=work_dir,  
            capture_output=True,  
            text=True,  
            timeout=COMMAND_TIMEOUT  
        )  
        stdout = process.stdout.strip()  
        stderr = process.stderr.strip()  

        output = ""  
        if stdout:  
            output += f"[STDOUT]:\n{stdout}\n"  
        if stderr:  
            output += f"[STDERR]:\n{stderr}\n"  
        if not output:  
            output = "[Command executed successfully with zero output]"  

        if len(output) > 12000:  
            output = output[:12000] + "\n...[OUTPUT TRUNCATED DUE TO LENGTH]..."  

        return {  
            "exit_code": process.returncode,  
            "output": output  
        }  

    except subprocess.TimeoutExpired:  
        return {  
            "exit_code": -1,  
            "output": f"[TIMEOUT]: Command exceeded {COMMAND_TIMEOUT} seconds limit."  
        }  
    except Exception as exc:  
        return {  
            "exit_code": -1,  
            "output": f"[EXECUTION ERROR]: {safe_error(exc)}"  
        }

=========================================================

5. FILE INTELLIGENCE

=========================================================

class FileIntelligence:

ALLOWED_EXTENSIONS = {  
    ".txt", ".md", ".json", ".py",  
    ".log", ".csv", ".xml", ".html", ".sh"  
}  

def inspect(self, filename):  
    path = Path(filename).expanduser().resolve()  
    if not path.is_file():  
        raise FileNotFoundError("File not found")  

    if path.stat().st_size > MAX_FILE_SIZE:  
        raise ValueError("File exceeds size limit")  

    return path.read_text(encoding="utf-8", errors="replace")  

def write_file(self, filename, content):  
    path = Path(filename).expanduser().resolve()  
    path.parent.mkdir(parents=True, exist_ok=True)  
    path.write_text(content, encoding="utf-8")  
    return f"Successfully wrote {len(content)} characters to {path}"

=========================================================

6. AUTONOMOUS AI CLIENT (ReAct Loop & Self-Healing)

=========================================================

class AutonomousAIClient:

def __init__(self, db, arsenal, file_intel, resource, linux):  
    self.db = db  
    self.arsenal = arsenal  
    self.file_intel = file_intel  
    self.resource = resource  
    self.linux = linux  

def _call_llm(self, messages):  
    if not API_KEY:  
        return (  
            "AI API key is not configured. "  
            "Set OPENAI_API_KEY in the environment variables."  
        )  

    import urllib.request  
    import urllib.error  

    payload = json.dumps({  
        "model": AI_MODEL,  
        "messages": messages  
    }).encode("utf-8")  

    request = urllib.request.Request(  
        AI_BASE_URL,  
        data=payload,  
        headers={  
            "Content-Type": "application/json",  
            "Authorization": f"Bearer {API_KEY}"  
        },  
        method="POST"  
    )  

    try:  
        with urllib.request.urlopen(request, timeout=120) as response:  
            data = json.loads(response.read().decode("utf-8"))  
        return data["choices"][0]["message"]["content"]  
    except urllib.error.HTTPError as exc:  
        detail = exc.read().decode("utf-8", errors="replace")  
        raise RuntimeError(f"AI API HTTP {exc.code}: {detail[:300]}")  
    except Exception as exc:  
        raise RuntimeError(f"AI connection failed: {safe_error(exc)}")  

def ask(self, prompt, status_callback=None):  
    available_tools = json.dumps(  
        self.arsenal.get_available_summary(), ensure_ascii=False  
    )  
    sys_info = json.dumps(self.linux.information(), ensure_ascii=False)  

    system_prompt = f"""

You are RIA MASTER PC v4.8, an advanced Autonomous Cloud Security Orchestrator & AI Hacking Assistant.
Environment: {sys_info}
Discovered Security Arsenal: {available_tools}

OPERATIONAL PROTOCOL:
You follow ONLY the user's commands. Support Bangla and English fluently. When a task requires running security tools, terminal commands, or file operations, you must issue JSON action blocks:

To run a shell command/tool:

{{      def read_file(self, filename):
        try:
            content = self.file_intel.inspect(filename)
            return {"status": "success", "content": content}
        except Exception as e:
            return {"status": "error", "message": safe_error(e)}

    def save_file(self, path, content):
        try:
            res = self.file_intel.write_file(path, content)
            return {"status": "success", "message": res}
        except Exception as e:
            return {"status": "error", "message": safe_error(e)}

