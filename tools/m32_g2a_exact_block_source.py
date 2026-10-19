"""Validate a G2-A exact PowerShell review candidate as TEXT, not execution."""
from pathlib import Path
import re

DOC = Path(__file__).resolve().parents[1] / "docs/qualification/M3_2_G2A_EXACT_BLOCK_REVIEW.md"
FENCE = re.compile(r"(?ms)^\x60{3}powershell[ \t]*\r?\n(.*?)^\x60{3}[ \t]*$")
REQUIRED = (
    "& {", "$ErrorActionPreference = 'Stop'", "[Environment]::SystemDirectory",
    "'whoami.exe'", "/groups /fo csv /nh", "ConvertFrom-Csv -Header",
    "'^S-1-16-[0-9]+$'", "'S-1-16-8192'",
    "Get-Process -ErrorAction Stop", "'Fabulaxiom','ollama','msedgewebview2'",
    "throw 'RELATED_OR_AMBIGUOUS_PROCESS'", "catch {",
    "G2A_LOCAL_METADATA: PASS", "G2A_LOCAL_METADATA: STOP",
    "PROCESS_WRITER_ABSENCE: NOT_PROVEN", "PUBLIC_GITHUB_CHECK: NOT_ASSESSED_BY_THIS_BLOCK",
    "G2B_G2C_G2D_G3_G6: NOT_AUTHORIZED", "TAURI_RUNTIME: NOT_TESTED",
)
BANNED = re.compile(r"(?i)\b(?:Read-Host|Add-Type|Invoke-Expression|Invoke-Command|"
    r"Invoke-RestMethod|Invoke-WebRequest|Start-Process|Stop-Process|Get-Content|"
    r"Set-Content|Get-Acl|Get-FileHash|Copy-Item|Move-Item|Remove-Item|New-Item|"
    r"Start-Transcript|Out-File|Tee-Object|git|sqlite3|tauri|pwsh\.exe|"
    r"powershell\.exe|Start-Job|Set-ExecutionPolicy|Register-ScheduledTask)\b")

class CandidateStop(ValueError):
    pass

def extract(markdown):
    matches = FENCE.findall(markdown)
    if len(matches) != 1:
        raise CandidateStop("STOP: must contain one exact code block")
    return matches[0]

def check(script):
    if not script.startswith("& {\n") or not script.rstrip().endswith("\n}"):
        raise CandidateStop("STOP: script wrapper changed")
    if len(script) > 3800 or any(marker not in script for marker in REQUIRED):
        raise CandidateStop("STOP: source boundary anchor missing")
    if BANNED.search(script) or re.search(r"(?m)[12]?>>?", script):
        raise CandidateStop("STOP: unsafe command or file redirection")
    if script.count("/groups /fo csv /nh") != 1 or \
       script.count("Get-Process -ErrorAction Stop") != 1:
        raise CandidateStop("STOP: duplicated token or process read")
    if script.count("Write-Output 'G2A_LOCAL_METADATA: STOP'") != 1:
        raise CandidateStop("STOP: missing STOP output")
    return {"candidate": "SYNTAX_REVIEW_ONLY", "operator_execution": "NOT_AUTHORIZED"}

def check_repository():
    return check(extract(DOC.read_text(encoding="utf-8")))
