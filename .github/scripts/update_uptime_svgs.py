import re
from datetime import datetime, timezone
from pathlib import Path


# TARGET START DATE: February 9, 2009 (UTC)
START_DATE = datetime(2009, 2, 9, 0, 0, 0, tzinfo=timezone.utc)
SVG_FILES = [
    "assets/vectors/index.light.svg",
    "assets/vectors/index.dark.svg"
]


def calculate_uptime(now: datetime) -> str:
    # Calculate full calendar years
    years = now.year - START_DATE.year
    anniversary = START_DATE.replace(year=now.year)
    if now < anniversary:
        years -= 1
        anniversary = START_DATE.replace(year=now.year - 1)

    # Remaining delta for days and hours
    delta = now - anniversary
    days = delta.days
    hours = delta.seconds // 3600

    # FIXED-WIDTH FORMATTING PRESERVES EXACT CHARACTER COUNT (28 CHARS)
    return f"{years:02d} YEARS, {days:03d} DAYS, {hours:02d} HOURS"


def update_svgs():
    now = datetime.now(timezone.utc)
    new_uptime = calculate_uptime(now)

    # MATCHES THE EXACT 28-CHARACTER UPTIME PATTERN SO SURROUNDING SPACES STAY UNTOUCHED
    pattern = re.compile(r"\d{2} YEARS, \d{3} DAYS, \d{2} HOURS")

    for file_path in SVG_FILES:
        path = Path(file_path)
        if not path.exists():
            print(f"Skipping {file_path}: file not found.")
            continue

        content = path.read_text(encoding="utf-8")
        updated_content, count = pattern.subn(new_uptime, content)

        if count > 0:
            path.write_text(updated_content, encoding="utf-8")
            print(f"Updated {file_path} -> '{new_uptime}'")
        else:
            print(f"Warning: Pattern not found in {file_path}")


if __name__ == "__main__":
    update_svgs()
