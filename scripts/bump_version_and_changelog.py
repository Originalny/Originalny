import os
import pathlib
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT / "VERSION"
CHANGELOG_FILE = ROOT / "CHANGELOG.md"


def read_version():
    text = VERSION_FILE.read_text(encoding="utf-8").strip()
    major, minor, patch = map(int, text.split("."))
    return major, minor, patch


def write_version(major: int, minor: int, patch: int) -> str:
    new_version = f"{major}.{minor}.{patch}"
    VERSION_FILE.write_text(new_version + "\n", encoding="utf-8")
    return new_version


def calculate_new_version(branch_name: str):
    major, minor, patch = read_version()

    branch_lower = branch_name.lower()
    if branch_lower.startswith("feature/"):
        minor += 1
        patch = 0
        change_type = "minor"
    elif branch_lower.startswith("hotfix/"):
        patch += 1
        change_type = "patch"
    else:
        # по умолчанию считаем patch
        patch += 1
        change_type = "patch"

    new_version = write_version(major, minor, patch)
    old_version = f"{major}.{minor}.{patch - 1}" if change_type == "patch" else f"{major}.{minor - 1}.0"

    return old_version, new_version, change_type


def update_changelog(new_version: str, branch_name: str, pr_number: str, author: str, summary: str):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    if CHANGELOG_FILE.exists():
        old_body = CHANGELOG_FILE.read_text(encoding="utf-8")
        # убираем первую строку "# Changelog\n\n"
        if old_body.startswith("# Changelog"):
            _, rest = old_body.split("\n", 1)
        else:
            rest = old_body
    else:
        rest = ""

    header = "# Changelog\n\n"
    new_entry = (
        f"## {new_version} — {now}\n"
        f"- Branch: `{branch_name}`\n"
        f"- PR: #{pr_number}\n"
        f"- Author: {author}\n"
        f"- Changes: {summary}\n\n"
    )

    CHANGELOG_FILE.write_text(header + new_entry + rest, encoding="utf-8")


def main():
    branch_name = os.environ.get("BRANCH_NAME", "unknown")
    pr_number = os.environ.get("PR_NUMBER", "0")
    author = os.environ.get("AUTHOR", "unknown")
    summary = os.environ.get("SUMMARY", "no description")

    old_version, new_version, change_type = calculate_new_version(branch_name)
    update_changelog(new_version, branch_name, pr_number, author, summary)

    # выводим данные, чтобы workflow мог их забрать как output
    print(f"OLD_VERSION={old_version}")
    print(f"NEW_VERSION={new_version}")
    print(f"CHANGE_TYPE={change_type}")


if __name__ == "__main__":
    main()
