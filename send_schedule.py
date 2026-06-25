import json
import os
import sys
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

# Load schedule data
with open("schedule.json", encoding="utf-8") as f:
    data = json.load(f)

tz = ZoneInfo(data.get("timezone", "America/Los_Angeles"))

# Use FORCE_DATE if provided (manual testing), otherwise today's date in Pacific time
force = os.environ.get("FORCE_DATE", "").strip()
target = force if force else datetime.now(tz).strftime("%Y-%m-%d")

day = data["days"].get(target)
if not day:
    print(f"No schedule for {target}; nothing to send.")
    sys.exit(0)

# Build the Slack message
lines = [f"*📅 {day['title']} — Today's Schedule*", ""]
for item in day["items"]:
    loc = f"   _{item['location']}_" if item.get("location") else ""
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
