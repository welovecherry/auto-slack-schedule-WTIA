<a id="top"></a>

# auto-slack-schedule-WTIA

**English** | [🇰🇷 한국어로 보기](#korean)

---

## Why this exists

WTIA program runs for about two months. Every day, the daily schedule lived inside a PowerPoint, posted in a Slack channel. To find out what was happening today, each of the ~30 people had to open Slack, go to the channel, open the PowerPoint, and look for today's date. Small, but you do it every single morning.

This bot removes that chore for the whole group. Every morning it posts **today's schedule** — times, activities, and locations — as simple text, straight into the Slack channel. No clicking into a file. You just read the channel.

---

## What it does

- Runs **every morning, around 7:00 AM (Pacific time)**, on its own.
- Looks up **today's date** in a schedule file.
- Posts that day's plan to a Slack channel.
- If there is no class that day, it posts nothing.

Nobody has to press a button. It keeps running while your computer is off.

---

## How it works

The whole thing is four small pieces working together:

```
   GitHub timer (cron)          A short Python script         Your Slack channel
   "It's 7 AM. Go!"     ─────►  - what day is it today? ─────► today's schedule
                                - find that day's plan         shows up as text
   (runs in GitHub's cloud,     - send it to Slack
    not on your computer)
```

In plain words: GitHub has a built-in alarm clock (called **cron**). At the set time it wakes up, borrows a tiny computer in GitHub's cloud for a few seconds, runs the script, and shuts it down. The script checks today's date, finds the matching schedule, and sends it to Slack through a **webhook** (a private link that lets you post a message into a channel).

---

## Files in this repo

| File | Type | What it's for |
|------|------|----------------|
| `schedule.json` | Data | The actual schedule — every day, its times, activities, and places. **This is the only file you normally edit.** |
| `send_schedule.py` | Python code | The worker. Finds today's plan and sends it to Slack. |
| `.github/workflows/daily-slack.yml` | Settings | Tells GitHub *when* to run and *what* to run. |

```
auto-slack-schedule-WTIA/
├── README.md
├── schedule.json                      ← edit this to change the schedule
├── send_schedule.py
└── .github/
    └── workflows/
        └── daily-slack.yml            ← edit this to change the send time
```

A key idea: the **data** (`schedule.json`) is kept apart from the **code** (`send_schedule.py`). When the schedule changes, you only touch the data file. You never need to read or change the code.

---

## Setup (one time)

If you ever rebuild this from scratch:

1. **Make a Slack webhook.** Go to https://api.slack.com/apps → *Create New App* → *From scratch*. Turn on **Incoming Webhooks**, click *Add New Webhook to Workspace*, pick your channel, and copy the URL. Keep it private — anyone with this URL can post to your channel.
2. **Make a private GitHub repo.**
3. **Add the three files** above. The `.yml` file must sit inside `.github/workflows/`.
4. **Add the webhook as a secret.** In the repo: *Settings → Secrets and variables → Actions → New repository secret*. Name it exactly `SLACK_WEBHOOK_URL` and paste the URL as the value.
5. **Test it.** Go to the *Actions* tab → *Daily Slack Schedule* → *Run workflow*. Check that the message shows up in Slack.

After that, it runs by itself every day.

---

## How to change the schedule

Open `schedule.json` on GitHub, click the pencil (Edit), and add or change a day. Each day looks like this:

```json
"2026-06-24": {
  "title": "Wednesday, June 24",
  "items": [
    { "time": "10:00 – 11:00", "activity": "Problem Discovery / Empathy Mapping", "location": "Fluke Hall" }
  ]
}
```

- The date key must be `YYYY-MM-DD`.
- `time` and `location` are optional. If you leave out `time`, the line shows with no time.
- A date that is **not** in the file sends **nothing** that day.

Click *Commit changes* and you're done.

**Test one day without waiting for the morning:** *Actions → Run workflow*, and type a date (like `2026-06-24`) in the box.

---

## How to change the send time (cron)

The time lives in one line of `.github/workflows/daily-slack.yml`:

```yaml
- cron: '0 14 * * *'
```

Those five fields mean:

```
0 14 * * *
│  │ │ │ └─ day of week (any)
│  │ │ └─── month (any)
│  │ └───── day of month (any)
│  └─────── hour
└────────── minute
```

**Important:** GitHub uses **UTC time only**, not local time. So you convert your local time to UTC.

- `0 14 * * *` = 14:00 UTC = **7:00 AM Pacific** (summer / PDT).
- Want 9:00 AM Pacific instead? Use `0 16 * * *`.

Change the numbers, commit, done.

A few honest notes:
- GitHub may run a few minutes (5–20) late. "Around 7 AM" is the right expectation, not "7:00 sharp."
- In fall, Pacific switches to standard time (PST), so the same UTC time lands one hour earlier. This program ends in August, so it doesn't matter here.
- If the repo gets **no activity for 60 days**, GitHub turns the schedule off. Just make any commit to wake it up again.

---
---

<a id="korean"></a>

# auto-slack-schedule-WTIA (한국어)

[⬆️ English로 보기](#top)

---

## 왜 만들었나

WTIA 프로그램은 약 두 달간 진행됩니다. 매일의 일정은 파워포인트 안에 들어 있고, 그게 슬랙 채널에 업로드 되어 있습니. 오늘 뭘 하는지 알려면 약 30명 각자가 슬랙을 열고 → 채널로 가서 → 파워포인트를 열고 → 오늘 날짜를 찾아야 했습니다. 작은 일이지만 매일 아침 반복됩니다.

이 봇은 그 번거로움을 모두를 위해 없앱니다. 매일 아침 **오늘의 일정**(시간·활동·장소)을 그냥 텍스트로 슬랙 채널에 올려줘요. 파일을 열 필요 없이, 채널만 보면 됩니다.

---

## 무엇을 하나

- 매일 아침 **오전 7시쯤(태평양 시간)** 알아서 실행됩니다.
- 일정 파일에서 **오늘 날짜**를 찾습니다.
- 그날의 일정을 슬랙 채널에 올립니다.
- 수업이 없는 날은 아무것도 올리지 않습니다.

버튼을 누를 필요가 없고, 내 컴퓨터가 꺼져 있어도 계속 돌아갑니다.

---

## 동작 원리

전체는 네 조각이 함께 일하는 구조입니다

```
   GitHub 타이머 (cron)          짧은 파이썬 스크립트          슬랙 채널
   "7시다. 실행!"        ─────►  - 오늘이 며칠?        ─────►  오늘 일정이
                                - 그날 일정 찾기                텍스트로 표시됨
   (내 컴퓨터가 아니라           - 슬랙으로 전송
    GitHub 클라우드에서 실행)
```

쉽게 말하면, GitHub에는 내장 알람시계(**cron**)가 있어요. 정해진 시각에 깨어나 GitHub 클라우드의 작은 컴퓨터를 몇 초간 빌려 스크립트를 돌리고 끕니다. 스크립트는 오늘 날짜를 확인해 맞는 일정을 찾고, **웹훅**(채널에 메시지를 넣을 수 있는 비공개 링크)을 통해 슬랙으로 보냅니다.

---

## 이 저장소의 파일

| 파일 | 종류 | 역할 |
|------|------|------|
| `schedule.json` | 데이터 | 실제 일정 — 날짜별 시간·활동·장소. **평소에 수정하는 건 이 파일 하나뿐입니다.** |
| `send_schedule.py` | 파이썬 코드 | 일꾼. 오늘 일정을 찾아 슬랙으로 보냅니다. |
| `.github/workflows/daily-slack.yml` | 설정 | GitHub에게 *언제* 무엇을 실행할지 알려줍니다. |

```
auto-slack-schedule-WTIA/
├── README.md
├── schedule.json                      ← 일정 바꿀 때 이 파일
├── send_schedule.py
└── .github/
    └── workflows/
        └── daily-slack.yml            ← 발송 시간 바꿀 때 이 파일
```

핵심 설계: **데이터**(`schedule.json`)와 **코드**(`send_schedule.py`)를 분리했습니다. 일정이 바뀌면 데이터 파일만 고치면 되고, 코드는 읽거나 손댈 필요가 없어요.

---

## 설치 (최초 1회)

처음부터 다시 만들 일이 있다면:

1. **슬랙 웹훅 만들기.** https://api.slack.com/apps → *Create New App* → *From scratch*. **Incoming Webhooks**를 켜고 *Add New Webhook to Workspace* → 채널 선택 → URL 복사. 이 URL은 비밀로 보관하세요(가진 사람은 누구나 채널에 글을 쓸 수 있음).
2. **비공개(private) GitHub 저장소 만들기.**
3. 위 **파일 3개 추가.** `.yml` 파일은 반드시 `.github/workflows/` 안에 있어야 합니다.
4. **웹훅을 시크릿으로 등록.** 저장소에서 *Settings → Secrets and variables → Actions → New repository secret*. 이름은 정확히 `SLACK_WEBHOOK_URL`, 값에 URL 붙여넣기.
5. **테스트.** *Actions* 탭 → *Daily Slack Schedule* → *Run workflow*. 슬랙에 메시지가 뜨는지 확인.

이후엔 매일 알아서 돌아갑니다.

---

## 일정 바꾸는 법

GitHub에서 `schedule.json`을 열고 연필(Edit)을 눌러 날짜를 추가·수정합니다. 하루는 이렇게 생겼습니다.

```json
"2026-06-24": {
  "title": "Wednesday, June 24",
  "items": [
    { "time": "10:00 – 11:00", "activity": "Problem Discovery / Empathy Mapping", "location": "Fluke Hall" }
  ]
}
```

- 날짜 키는 `YYYY-MM-DD` 형식.
- `time`, `location`은 선택사항. `time`을 빼면 시간 없이 표시됩니다.
- 파일에 **없는** 날짜는 그날 **아무것도** 안 보냅니다.

*Commit changes*를 누르면 끝.

**아침까지 안 기다리고 특정 날 테스트:** *Actions → Run workflow*에서 날짜(예: `2026-06-24`)를 입력하세요.

---

## 발송 시간 바꾸는 법 (cron)

시간은 `.github/workflows/daily-slack.yml`의 한 줄에 있습니다:

```yaml
- cron: '0 14 * * *'
```

다섯 칸의 의미:

```
0 14 * * *
│  │ │ │ └─ 요일 (any)
│  │ │ └─── 월 (any)
│  │ └───── 일 (any)
│  └─────── 시
└────────── 분
```

**중요:** GitHub은 **UTC 시간만** 씁니다(현지 시간 아님). 그래서 현지 시간을 UTC로 변환해야 합니다.

- `0 14 * * *` = 14:00 UTC = **태평양 오전 7시** (여름 / PDT).
- 오전 9시로 하고 싶으면? `0 16 * * *`.

숫자만 바꾸고 커밋하면 됩니다.

솔직한 참고사항 몇 가지:
- GitHub은 몇 분(5~20분) 늦게 실행될 수 있어요. "7시 정각"이 아니라 "7시쯤"이 맞는 기대치입니다.
- 가을에 태평양이 표준시(PST)로 바뀌면 같은 UTC 시각이 한 시간 일찍 잡힙니다. 이 프로그램은 8월에 끝나므로 해당 없음.
- 저장소가 **60일간 활동이 없으면** GitHub이 스케줄을 끕니다. 아무 커밋이나 하나 넣으면 다시 깨어납니다.

---

[⬆️ 맨 위로](#top)
