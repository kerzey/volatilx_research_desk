# Running the daily and weekly checks by hand

Use this when the computer was asleep or off at the scheduled time and a check didn't run.

| Routine | Normally runs | Writes | Takes |
|---|---|---|---|
| Daily check | Mon–Fri 17:45 (your local time) | `research/reports/daily/<date>.md` | seconds |
| Weekly snapshot | Saturday 07:00 | `research/reports/weekly/<date>.md` | 20–30 min |

Windows only runs them if the computer is **awake and you are logged in**. If the computer
was asleep, Windows *may* run the most recent missed one by itself within ~10 minutes of waking —
so start with Step 0.

---

## Step 0 — Did Windows already catch up?

Look in the `logs/` folder of the desk. A file named `daily-<today>.log` or
`weekly-<today>.log` means that job already ran after the computer woke up. Skip that job
below, or you'll just get a duplicate report.

## Step 1 — Open Git Bash in the desk folder

Open **Git Bash** (Start menu → "Git Bash"), then:

```bash
cd "/c/Users/sahin/OneDrive/Desktop/VolatilX_Research_Desk"
```

## Step 2 — Daily check

### 2a. For last night only (the usual case)

```bash
./scripts/research_routines.sh daily
```

This is exactly what the scheduler runs: it loads the keys, checks the latest SAS run, writes
the report, and posts RED / ALL CLEAR to Discord.

One quirk: the file is named with **today's** date, not the trading date. If you run it on
Saturday for Friday's run, the file is `2026-09-12.md` but the contents are about 09-11. The
first line of the report says which trading date it checked.

### 2b. For one or more missed days (catching up)

Load the keys once:

```bash
set -a; . ./.env.research; set +a
```

Then run one line per missed **trading day** (weekdays; skip market holidays):

```bash
python research/lib/daily_check.py --date 2026-09-11 > research/reports/daily/2026-09-11.md
```

Change the date on both sides of the `>` for each day. Differences from 2a:
- the file is named after the trading date, which is what you want for catch-up;
- nothing is posted to Discord;
- the "did the nightly job finish on time" freshness check is skipped, because it only makes
  sense on the day itself.

## Step 3 — Weekly snapshot

```bash
./scripts/research_routines.sh weekly
```

This starts Claude in the background and takes 20–30 minutes; the window looks frozen while it
works. Leave it open. It is finished when the prompt (`$`) comes back.

Alternative: in a desk session (`./scripts/start_desk.sh`), type `/weekly-performance`. You see
it working, but you then have to ask it to save the report under `research/reports/weekly/`.

## Step 4 — Read the result

Open the new file(s) in VS Code.

- **Daily** — the top line is one of:
  - `ALL CLEAR` — nothing to do;
  - `RED` — something broke (a missing run, a count collapsing). Look into it before trading
    on that night's picks;
  - `AMBER` — numbers drifting. Just note it; no action needed.
- **Weekly** — a descriptive snapshot. No verdicts; nothing to act on by itself. It may add
  ideas to `research/BACKLOG.md`.

If a report file is empty or only has an error message, the job failed. Scroll back in the Git
Bash window for the error (most often: `.env.research` missing a key, or no internet).

## Step 5 — Save it in git

```bash
git add research/reports research/BACKLOG.md
git commit -m "Routine reports (manual catch-up)"
git push origin master
```

---

## Easiest alternative: the Run button

Start menu → **Task Scheduler** → **Task Scheduler Library** → right-click
**VolatilX Research Daily** (or **Weekly**) → **Run**. It does the same thing as Step 2a /
Step 3, including the today's-date file name.

## Stopping it from happening again (optional)

Let the tasks wake the computer from sleep. In **PowerShell** (not Git Bash):

```powershell
foreach ($n in 'VolatilX Research Daily','VolatilX Research Weekly') {
  $t = Get-ScheduledTask -TaskName $n
  $t.Settings.WakeToRun = $true
  Set-ScheduledTask -InputObject $t
}
```

This only helps when the computer is **asleep** — a fully shut-down computer can't be woken.
Windows also has to allow it: Settings → System → Power → *Edit power plan* →
*Change advanced power settings* → **Sleep → Allow wake timers → Enable**.
