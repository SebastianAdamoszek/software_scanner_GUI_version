import json
import logging
import subprocess


REGISTRY_PATHS = [
    r"HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
    r"HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
    r"HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
]


POWERSHELL_SCRIPT = rf"""
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$paths = @(
    "{REGISTRY_PATHS[0]}",
    "{REGISTRY_PATHS[1]}",
    "{REGISTRY_PATHS[2]}"
)

$items = foreach ($path in $paths) {{
    Get-ItemProperty -Path $path -ErrorAction SilentlyContinue |
        Where-Object {{ $_.DisplayName -and $_.DisplayName.Trim() -ne "" }} |
        Select-Object DisplayName, DisplayVersion, Publisher, InstallDate, InstallLocation, UninstallString
}}

$items |
    Sort-Object DisplayName, DisplayVersion, Publisher -Unique |
    ConvertTo-Json -Depth 3
"""


def scan_installed_programs(timeout=30):
    command = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        POWERSHELL_SCRIPT,
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        logging.exception("Skanowanie przekroczylo limit czasu: %s sekund.", timeout)
        return []
    except FileNotFoundError:
        logging.exception("Nie znaleziono PowerShella w systemie.")
        return []
    except OSError:
        logging.exception("Blad systemowy podczas uruchamiania skanowania.")
        return []

    if result.returncode != 0:
        logging.error("PowerShell zakonczyl prace z kodem %s.", result.returncode)
        logging.error("STDERR: %s", result.stderr.strip())
        return []

    output = (result.stdout or "").strip()
    if not output:
        logging.warning("PowerShell nie zwrocil zadnych danych.")
        if result.stderr:
            logging.warning("STDERR: %s", result.stderr.strip())
        return []

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        logging.exception("Nie udalo sie odczytac JSON z wyniku PowerShella.")
        logging.error("STDOUT: %s", output[:2000])
        return []

    if isinstance(data, dict):
        data = [data]

    programs = [normalize_program(item) for item in data if item.get("DisplayName")]
    return remove_duplicates(programs)


def normalize_program(item):
    return {
        "name": clean_text(item.get("DisplayName")),
        "version": clean_text(item.get("DisplayVersion")),
        "publisher": clean_text(item.get("Publisher")),
        "install_date": format_install_date(clean_text(item.get("InstallDate"))),
        "install_location": clean_text(item.get("InstallLocation")),
        "uninstall_string": clean_text(item.get("UninstallString")),
    }


def clean_text(value):
    if value is None:
        return ""
    return str(value).strip()


def format_install_date(date):
    if date and len(date) == 8:
        return f"{date[:4]}-{date[4:6]}-{date[6:]}"
    
    return date

def remove_duplicates(programs):
    unique = {}

    for program in programs:
        key = (
            program["name"].casefold(),
            program["version"].casefold(),
            program["publisher"].casefold(),
        )
        unique[key] = program

    return sorted(unique.values(), key=lambda item: item["name"].casefold())
