import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Load schedule data
with open("schedule.json", encoding="utf-8") as f:
    data = json.load(f)

tz = ZoneInfo(data.get("timezone", "America/Los_Angeles"))

# Use FORCE_DATE if provided (manual testing), otherwise tomorrow's date in Pacific time
force = os.environ.get("FORCE_DATE", "").strip()
target = force if force else (datetime.now(tz) + timedelta(days=1)).strftime("%Y-%m-%d")
today = datetime.now(tz).strftime("%Y-%m-%d")
label = "Today's Schedule" if target == today else "Tomorrow's Schedule"

day = data["days"].get(target)
if not day:
    print(f"No schedule for {target}; nothing to send.")
    sys.exit(0)

# Skip if this date was already sent (dedup guard for backup crons)
marker_file = "last_sent.txt"
last_sent = open(marker_file, encoding="utf-8").read().strip() if os.path.exists(marker_file) else ""
if not force and last_sent == target:
    print(f"Already sent for {target}; skipping.")
    sys.exit(0)
# Build the Slack message
lines = [f"*📅 {day['title']} — {label}*", ""]
for item in day["items"]:
        loc = f" _{item['location']}_" if item.get("location") else ""
        time_str = f"*{item['time']}* " if item.get("time") else ""
        lines.append(f"• {time_str}{item['activity']}{loc}")
text = "\n".join(lines)

# Post to Slack
webhook = os.environ["SLACK_WEBHOOK_URL"]
payload = json.dumps({"text": text}).encode("utf-8")
req = urllib.request.Request(
    webhook, data=payload, headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req) as resp:
    print(f"Sent schedule for {target}. Slack responded: {resp.status}")
open(marker_file, "w", encoding="utf-8").write(target)
