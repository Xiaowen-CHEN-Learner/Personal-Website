"""Finish Xavier's GitHub profile using his own authenticated GitHub CLI.

Default: preview only, with no authentication or network needed.
Use --apply to create the profile repository, update public profile fields,
and add repository descriptions/topics. No renames, deletions, visibility
changes, email publication, credential handling, or pin/photo changes.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

OWNER = "Xiaowen-CHEN-Learner"
PROFILE = {
    "name": "Xavier Chen (Xiaowen)",
    "bio": "Fordham MS Finance & Research Assistant | Python, investment research & AI workflows | Former FP&A | Building practical finance tools.",
    "company": "Fordham University",
    "location": "New York, NY",
    "blog": "https://www.linkedin.com/in/xiaowen-chen/",
}
REPOS = {
    "Learn-Finance-Though-Games": (
        "Interactive browser-based finance lessons on market events, behavioral biases, and probability.",
        ["finance", "financial-education", "javascript", "interactive-learning"]),
    "Quantitative-investing_Quantamental-approach": (
        "Exploratory Python notebooks for VIX-based index strategies and market-sentiment research.",
        ["python", "jupyter-notebook", "quantitative-finance", "backtesting"]),
    "Equity-research": (
        "Independent equity and industry research informed by accounting, FP&A, and financial analysis.",
        ["equity-research", "financial-analysis", "investment-research"]),
    "AI-Projects---Price-Catalysts": (
        "Notebook experiments combining market-price visualizations with event context.",
        ["python", "data-visualization", "financial-markets"]),
    "From-prompt-to-AI-system": (
        "Reusable Markdown research instructions and worked examples for AI-assisted portfolio review.",
        ["prompt-engineering", "ai-workflows", "investment-research", "markdown"]),
    "FMR-A---Structuring-a-1-Million-Portfolio-Gold-Silver-and-Gold-Mining-Equities": (
        "Academic precious-metals portfolio research with Python performance, correlation, and regression notebooks.",
        ["python", "portfolio-analysis", "precious-metals", "jupyter-notebook"]),
    "Headhunt_FixedIncome": (
        "Fixed-income research workspace with a tested offline bond-pricing example and dated research inputs.",
        ["python", "fixed-income", "credit-research", "yield-curve"]),
    "Personal-Website": (
        "Static portfolio site for Xavier Chen's finance research, analytical projects, and educational tools.",
        ["portfolio", "personal-website", "html", "finance"]),
}


def gh(*args: str, payload: dict | None = None) -> str:
    command = ["gh", *args]
    stdin = None
    if payload is not None:
        command += ["--input", "-"]
        stdin = json.dumps(payload)
    result = subprocess.run(command, input=stdin, text=True, encoding="utf-8",
                            capture_output=True, check=False, timeout=90)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "GitHub CLI command failed")
    return result.stdout


def api(endpoint: str, method: str = "GET", payload: dict | None = None):
    text = gh("api", "--hostname", "github.com", "--method", method,
              endpoint, payload=payload)
    return json.loads(text) if text.strip() else None


def optional_get(endpoint: str):
    try:
        return api(endpoint)
    except RuntimeError as exc:
        if "HTTP 404" in str(exc):
            return None
        raise


def check_owner(user: dict) -> None:
    if user.get("login", "").casefold() != OWNER.casefold():
        raise RuntimeError(f"Stop: authenticate to github.com as {OWNER} before applying.")


def merged_topics(existing: list[str], desired: list[str]) -> list[str]:
    result = sorted(set(existing) | set(desired))
    if len(result) > 20:
        raise ValueError("Topic limit exceeded; existing topics will not be removed automatically.")
    if any(not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", item) for item in result):
        raise ValueError("Invalid topic; no changes made to this repository.")
    return result


def preview() -> None:
    print("PREVIEW ONLY — no GitHub changes or network requests")
    print(json.dumps(PROFILE, indent=2))
    print(f"Create/update public profile README: {OWNER}/{OWNER}")
    for name, (description, topics) in REPOS.items():
        print(f"\n{name}\n  {description}\n  Topics to add: {', '.join(topics)}")
    print("\nPreserved: repository names, visibility, code, existing topics, email and photo.")
    print("Pins and photo still require GitHub's profile interface.")


def apply(replace_readme: bool = False) -> None:
    if shutil.which("gh") is None:
        raise RuntimeError("Install GitHub CLI, then run gh auth login --hostname github.com --web --scopes write:user")
    user = api("user")
    check_owner(user)
    profile_path = f"repos/{OWNER}/{OWNER}"
    profile_repo = optional_get(profile_path)
    if profile_repo and profile_repo.get("private"):
        raise RuntimeError("Existing profile repository is private; its visibility will not be changed automatically.")
    source = api(f"repos/{OWNER}/Personal-Website/contents/docs/PROFILE_README.md")
    if source.get("encoding") != "base64":
        raise RuntimeError("Unexpected profile README encoding.")
    desired_readme = base64.b64decode(source["content"]).decode("utf-8")
    old_readme = optional_get(f"{profile_path}/contents/README.md") if profile_repo else None
    old_text = base64.b64decode(old_readme["content"]).decode("utf-8") if old_readme else ""
    placeholders = {"", f"# {OWNER}", f"# {OWNER}\n"}
    if old_text.strip() != desired_readme.strip() and old_text.strip() not in placeholders and not replace_readme:
        raise RuntimeError("Existing custom profile README found. Review it, then use --replace-profile-readme to replace with a local backup.")

    # Preflight reads and backups happen before any writes.
    states = {}
    for name, (_, topics) in REPOS.items():
        repo = api(f"repos/{OWNER}/{name}")
        if repo.get("archived"):
            raise RuntimeError(f"{name} is archived; stop rather than alter its status.")
        merged_topics(repo.get("topics", []), topics)
        states[name] = {k: repo.get(k) for k in ("description", "topics", "homepage", "id")}
    backup_dir = Path.home() / ".xavier-github-setup"
    backup_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    backup = backup_dir / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json")
    snapshot = {"profile": {k: user.get(k) for k in PROFILE}, "repositories": states,
                "profile_repository_existed": bool(profile_repo), "profile_readme": old_text}
    with backup.open("x", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=2)
    print(f"Backup of public fields and README: {backup}")

    if not profile_repo:
        api("user/repos", "POST", {"name": OWNER, "private": False, "auto_init": True,
                                  "description": "Xavier Chen | Finance research, Python analytics and AI workflows"})
        old_readme = api(f"{profile_path}/contents/README.md")
    if old_text.strip() != desired_readme.strip():
        body = {"message": "docs: activate professional GitHub profile README",
                "content": base64.b64encode(desired_readme.encode("utf-8")).decode("ascii")}
        if old_readme:
            body["sha"] = old_readme["sha"]
        api(f"{profile_path}/contents/README.md", "PUT", body)
    verified = api(f"{profile_path}/contents/README.md")
    if base64.b64decode(verified["content"]).decode("utf-8") != desired_readme:
        raise RuntimeError("Profile README verification failed.")
    print("Verified: public profile README")

    api("user", "PATCH", PROFILE)
    current = api("user")
    if any(current.get(key) != value for key, value in PROFILE.items()):
        raise RuntimeError("Public profile field verification failed.")
    print("Verified: name, bio, company, location and LinkedIn")
    for name, (description, topics) in REPOS.items():
        endpoint = f"repos/{OWNER}/{name}"
        # Re-read topics immediately before merging, preserving additions since preflight.
        current_topics = api(endpoint).get("topics", [])
        api(endpoint, "PATCH", {"description": description})
        api(f"{endpoint}/topics", "PUT", {"names": merged_topics(current_topics, topics)})
        current = api(endpoint)
        if current.get("description") != description or not set(topics) <= set(current.get("topics", [])):
            raise RuntimeError(f"Metadata verification failed for {name}.")
        print(f"Verified: description and topics for {name}")
    print("Finished. Set your six pins and review your photo in GitHub's profile interface.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="make and verify the listed GitHub changes")
    parser.add_argument("--replace-profile-readme", action="store_true", help="allow replacing a custom README after backing it up locally")
    args = parser.parse_args()
    if not args.apply:
        preview()
        return 0
    try:
        apply(args.replace_profile_readme)
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"STOPPED: {exc}\nEarlier verified changes may remain. Review the local backup before rerunning.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
