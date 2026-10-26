# EGN 321 · Assignment 8.1 — Silent Handoff Operating Guide

**Application:** Unattended Temperature Monitoring Dashboard  
**Repository for this handoff:** https://github.com/Barquito0/EGN-321-Module-8_1  
**Verified earlier application:** https://github.com/Barquito0/EGN-321-Module-7_2  
**Operator audience:** an assigned classmate who has not developed this project.

> **Start here.** This guide is written for someone working alone. Please do not request verbal help from the author during the silent handoff. If a step fails, write down the step, message, and time. Do **not** delete databases to make the problem disappear.
>
> **Important architecture note:** The original Module 7.2 application remains in its previous repository. This handoff package fetches a **pinned, verified version** of that existing application into `application/` on first setup. A network connection is required for this first download. On later starts, it uses the already-downloaded copy and preserves its SQLite state. This guide does not claim the first download works offline.

## 1. Project Overview

This program watches replayed readings from an Arduino-style **virtual temperature sensor**, validates each measurement, stores original historical and replay records in **SQLite**, displays a live **Flask dashboard**, and reports unhealthy operation. The system makes noisy, missing, rejected, stale, and failed data visible instead of hiding problems behind a single last-known number.

The application evolves the course's earlier manually entered calculation/checking process: Module 5 replaced typed temperature input with simulator readings; Module 6 retained a searchable history; Modules 7.1 and 7.2 added alerts, unattended restart, and failure investigation. This handoff package improves setup and operations without changing the original engineering filtering and alert rules. **No particular spreadsheet workbook was replaced directly by the Module 7 dashboard**; its original process was manual temperature monitoring and manual checks of recent data.

Intended users are students, engineers, or operations personnel checking a small simulated temperature feed. It is **not** a certified safety instrument or production plant controller.

## 2. System Requirements

| Item | Requirement |
|---|---|
| Computer | Windows 10/11, macOS, or Linux; permission to create folders and listen on localhost |
| Python | **3.11 or newer**; Python installed and accessible from a terminal |
| Git | Required **once** to download the pinned Module 7.2 application |
| Network | Internet on first setup to access GitHub and install Python packages; optional for later local monitoring |
| Browser | Chrome, Firefox, Edge, or Safari (localhost access, no browser account needed) |
| Python libraries | Flask and pytest, installed by `requirements.txt` |
| Storage | At least 50 MB free for working SQLite history and logs |
| Port | TCP `5000` on `127.0.0.1` must be available, or set environment variable `PORT` |
| Included sample | `data/module6_sample_sensor_history.csv` (1,756 original rows, timestamps in source file) |
| Working database | Created/preserved automatically under `application/state/monitor.db` |
| Optional variables | `PORT`, `REPLAY_SECONDS`, `CLASSROOM_DEMO`, `STALE_DEGRADED_SECONDS`, `STALE_FAILED_SECONDS` |

**Do not open this server to the public Internet.** The Flask development server is configured for local classroom use; it has no authentication or TLS. The supervisor restarts an exited Flask child process but cannot recover from a computer that is powered off.

## 3. Installation

1. Open **Terminal** (Mac/Linux) or **PowerShell** (Windows). Install Python and Git first if not already present.
2. Copy the commands for **your operating system** below. Wait for each command to complete successfully before starting the next.

### Windows PowerShell

```powershell
git clone https://github.com/Barquito0/EGN-321-Module-8_1.git
cd EGN-321-Module-8_1
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\prepare_application.py
.\.venv\Scripts\python.exe scripts\preflight.py
.\.venv\Scripts\python.exe scripts\start_monitor.py
```

If Python 3.11 is not installed but 3.12 or 3.13 is installed, change `py -3.11` to `py -3.12` or `py -3.13` for the virtual-environment creation command. Using the `\.venv\Scripts\python.exe` path avoids PowerShell execution-policy/activation problems.

### macOS / Linux

```bash
git clone https://github.com/Barquito0/EGN-321-Module-8_1.git
cd EGN-321-Module-8_1
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python scripts/prepare_application.py
./.venv/bin/python scripts/preflight.py
./.venv/bin/python scripts/start_monitor.py
```

A successful preflight prints **READY**. Leave the terminal with `start_monitor.py` running, then open **http://127.0.0.1:5000**. If any preflight line says **FAIL**, follow its `Fix:` line before moving on.

### Where does the source code come from?

`scripts/prepare_application.py` checks out a specific earlier-course commit (`2f8fe29c21dc5c05496c622caa893a352d9420ce`) from the student's Module 7.2 repository. It saves a revision receipt in `application-version.json`. It **does not** replace an existing `application/` directory or delete its database. Do not alter the pinned revision during a graded silent handoff.

## 4. Quick Start

If you **already completed installation** and have returned on another day:

1. Open the `EGN-321-Module-8_1` folder in a terminal.
2. Run the existing virtual-environment Python:
   - Windows: `.\.venv\Scripts\python.exe scripts\start_monitor.py`
   - Mac/Linux: `./.venv/bin/python scripts/start_monitor.py`
3. Open **http://127.0.0.1:5000** in a browser.
4. Wait around 2–5 seconds for a fresh `MODULE6_SOURCE_REPLAY` temperature.
5. Check that **System Health = HEALTHY** and the latest source status is **OK**.
6. Switch between **Replay** and **Original Archive** history views to inspect readings.
7. When done, press **Ctrl+C** in the running terminal. Keep the SQLite database and logs for next time.

**No value has to be typed into the dashboard.** The replay source supplies measurements automatically.

## 5. Normal Operation

The source is the included classroom temperature replay. With `CLASSROOM_DEMO=0`, the monitor reads samples, validates numeric values and source flags, appends accepted/rejected rows to the SQLite working database, evaluates a persistent high-temperature alert, and updates the dashboard. It processes a replay sample about every **2 seconds**. The original archived timestamps remain unchanged, while the arrival time (`captured_at_utc`) is separately recorded as UTC.

**Practice a normal workflow:** open the dashboard, note the latest temperature in **°C**, read its source/arrival timestamp and status, switch to **Original Archive**, verify that historical measurements appear, then switch back to **Replay** and verify the newest arrival updates. Open `/api/status` in a second browser tab for structured status and `/api/history?mode=archive&limit=20` for source data. Successful routine operation shows `HEALTHY`, `OK`, a non-empty accepted reading, recent replay activity, and an **inactive** high-temperature alert.

The archive contains **1,756 original source timestamps** from October 1–2, 2026, covering **five sensors** (8,780 sensor rows in the original Module 6 database). Those **historical timestamps are not current device time**. There are two source gaps: 25 missing 60-second slots and 20 missing 60-second slots. The system does not invent temperatures inside those gaps.

## 6. Inputs and Units

| Input | Unit / format | Required? | Accepts / examples |
|---|---|---|---|
| Sensor reading | Celsius, floating-point | Yes (via CSV replay) | Finite values, **0–50°C** absolute acceptance range |
| Source status | Text | Yes | `OK` accepted if numeric/in range; other source statuses rejected |
| Original source timestamp | ISO-like text from CSV | Yes | `2026-10-01T08:00:00` (timezone unspecified) |
| Sample number | Positive integer from CSV | Yes | `1`, `2`, and so on |
| Arrival timestamp | UTC ISO datetime | Automatic | Logged when the replay worker receives a sample |
| Replay interval | Seconds | Optional | `REPLAY_SECONDS=2` default; do not assume it is the original archive cadence |
| Demo mode | `0` or `1` | Optional | `0` (ordinary replay), `1` (clearly labeled synthetic alert/missing tests) |
| Web port | TCP port | Optional | `5000` by default |

`data/module6_sample_sensor_history.csv` is included as reference. The fetched application includes its own unmodified copy; do not edit or reformat the original CSV for the handoff test. The raw value, accepted value, status, source timestamp, and arrival timestamp remain distinct in SQLite.

## 7. What the Tool Refuses

The tool intentionally does **not** treat these as trustworthy measurements: missing input; nonnumeric or nonfinite temperature; source status other than `OK`; temperatures below 0°C or above 50°C; or a stale/failed replay as a *current* observation. A failed or missing reading is recorded with `accepted_value=NULL`; the dashboard displays **no current accepted value** rather than reusing an old number. Stale input is not silently substituted.

Startup cannot succeed safely without Python/Flask, the required replay CSV, a writable SQLite folder, and a free local port. The preflight helper clearly reports these problems; `prepare_application.py` also refuses to overwrite an incomplete existing app directory. Do not delete the database to bypass these refusals.

## 8. Expected Output

The dashboard shows the current accepted temperature (°C) or an unavailable indicator, last **arrival timestamp**, source provenance/status, **health state**, alert state, and historical plots/tables. The **Replay** chart uses arrival times; **Original Archive** displays the source's older timestamps and retains gaps. `http://127.0.0.1:5000/api/status` returns machine-readable JSON, and `/api/history?mode=replay&limit=20` returns recent records.

The working SQLite database lives in `application/state/monitor.db`. The JSONL log is `application/logs/monitor.jsonl`. When the feed is healthy, new accepted rows increase and a recent `READING_ACCEPTED` event is visible.

## 9. System Health and Alerts

| State | Meaning | Operator action |
|---|---|---|
| **RECOVERING** | Process started but no new replay reading has arrived | Wait for one replay interval; check startup logs if it persists |
| **HEALTHY** | Current accepted reading ≤8 seconds old, no active alert | Normal operation |
| **DEGRADED** | Latest input rejected/missing, replay age >8 seconds, **or** high-temperature alert active | Check source status, age, and logs; pause test only if performing documented troubleshooting |
| **FAILED** | No replay input arrived for >18 seconds | Check pause flag, worker status, and logs; follow recovery steps |

Alert trigger: **3 consecutive accepted temperature readings ≥30.0°C**. It does not trigger on one noisy spike. The high alert clears only after **2 consecutive accepted readings ≤28.5°C** (hysteresis). Missing or rejected data do not silently clear an active alert. Alert state is persisted in SQLite across process restarts. Ordinary classroom history generally does not cross 30°C; `CLASSROOM_DEMO=1` deliberately injects labeled test values, **not real measurements**.

## 10. Logs

| Location | Purpose |
|---|---|
| `application/logs/monitor.jsonl` | Machine-written UTC activity, warnings, alert activation/clearing, stale/failed input, errors and recovery |
| `application/state/monitor.db` → `monitor_events` | Persistent timestamped operational events |
| `application/state/monitor.db` → `readings` | Raw/accepted/rejected observations and source/arrival provenance |
| `application/evidence/` | Earlier verified Module 7.2 screenshots and recorded recovery/failure investigation |

To view recent logs, open **a second terminal**, navigate to this handoff folder, and run:

- Windows: `.\.venv\Scripts\python.exe scripts\view_logs.py --last 15`
- Mac/Linux: `./.venv/bin/python scripts/view_logs.py --last 15`

Examples: `STARTUP`, `READING_ACCEPTED`, `SOURCE_PAUSED`, `STALE_INPUT`, `INPUT_FAILED`, `SOURCE_RESUMED`, `HEALTH_RECOVERED`, `ALERT_ACTIVATED`, `ALERT_CLEARED`. Logs explain what the software **observed**; they do not prove physical sensor calibration or an unknown person's actions.

## 11. Troubleshooting

| Problem | Likely cause | What to check / do |
|---|---|---|
| `git` command not found | Git not installed | Install Git, reopen terminal, rerun `prepare_application.py` |
| `ModuleNotFoundError: flask` | Dependencies not installed in active Python | Re-run `venv` Python `-m pip install -r requirements.txt`; use same Python to start |
| `APP MISSING` | Source checkout step skipped | Run `scripts/prepare_application.py`; Internet needed once |
| Port 5000 already in use | Another server or previous app instance running | Stop old process with Ctrl+C or choose a free `PORT` |
| No readings / **DEGRADED** | Paused source, invalid input, slow worker | Check `source_control.py status`, `view_logs.py`, and `/api/status` |
| Health **FAILED** | No data for >18s | Resume a paused source; check process/worker and SQLite; wait for a new reading |
| Database unavailable | Permission, full disk, damaged path | Check `application/state`, disk space and JSONL `APPLICATION_ERROR`; do not delete DB |
| High-temp alert active | Persistent ≥30°C accepted data or classroom demo | Check readings/provenance, wait for 2 valid ≤28.5°C to clear; do not manually falsify data |
| Archive readings look old | They are from Oct 2026 source CSV | Switch to **Replay** to see current arrival times |
| Alert data appear unexpectedly | `CLASSROOM_DEMO=1` was enabled | Restart with `CLASSROOM_DEMO=0`; demo readings are labeled `TEST_INJECTED` |

## 12. Recovery Procedures

### A. Demonstrate and recover from a stopped replay source (safe classroom test)

1. Confirm dashboard shows **HEALTHY** and a recent accepted replay reading.
2. In a **second terminal**, use the same venv Python to run `scripts/source_control.py pause`.
3. Leave the monitoring terminal open. Watch the dashboard move to **DEGRADED** after roughly 8 seconds and **FAILED** after roughly 18 seconds; the last reading must **not** appear current.
4. Open `scripts/view_logs.py --last 20`, and look for `SOURCE_PAUSED`, `STALE_INPUT`, and `INPUT_FAILED`.
5. In the second terminal run `scripts/source_control.py resume`.
6. Wait for a **new** accepted reading and **HEALTHY**. Check `SOURCE_RESUMED` and `HEALTH_RECOVERED` in the logs.
7. Verify historical readings are still present. **Do not remove or reset `monitor.db`.**

Windows command examples:

```powershell
.\.venv\Scripts\python.exe scripts\source_control.py pause
.\.venv\Scripts\python.exe scripts\view_logs.py --last 20
.\.venv\Scripts\python.exe scripts\source_control.py resume
```

macOS / Linux examples:

```bash
./.venv/bin/python scripts/source_control.py pause
./.venv/bin/python scripts/view_logs.py --last 20
./.venv/bin/python scripts/source_control.py resume
```

### B. Flask application exits

The `scripts/start_monitor.py` launcher runs the existing **supervisor**. A child-process exit triggers automatic restart; open the dashboard again and confirm a fresh reading after restart. If the supervisor itself exits, restart `scripts/start_monitor.py`. **Host boot automation is not activated by the handoff package.** The earlier systemd example is available in `application/scripts/monitor7.service.example` for an authorized Linux administrator to configure separately.

### C. Unreadable database

Stop the app; make a copy of `application/state/monitor.db`, including any `-wal` or `-shm` files if present. Check disk space/permissions and examine logs. Only after preserving a backup may a technical operator investigate repair or reseeding; reseeding destroys unique replay events and **is not** an acceptable shortcut in the handoff.

## 13. Assumptions

This is a **classroom simulator/replay**, not a calibrated real thermometer. The source uses Celsius, and original timestamps have no stated timezone. The Module 6 archive cadence is **60 seconds**; Module 7 arrival/replay cadence defaults to **2 seconds** and is a different clock. The machine has access to the first-run GitHub repository and a free localhost port. The default dashboard operates locally. Classroom thresholds (0–50°C acceptance, ≥30°C high alert) are not certified physical safety limits.

## 14. Known Limitations

- No physical sensor calibration, independent external measurement, email/SMS notifications, or safety shutdown.
- `application/` is downloaded from an earlier repository on first setup; first installation **needs Internet and Git**.
- It does not run after a computer power failure unless the host operator sets up boot-time process management.
- Uses Flask's classroom development server, not a hardened Internet-facing deployment.
- Historical source gaps cannot be reconstructed. Rejecting data does not prove what happened between samples.
- A supervisor cannot correct database corruption, broken host filesystems, or a permanently missing sensor source.
- No guarantee that a partner can operate the project successfully until the **actual silent handoff** is conducted and recorded.

## 15. Testing

Run from this repository root after installing dependencies:

- Windows: `.\.venv\Scripts\python.exe -m pytest -q`
- macOS/Linux: `./.venv/bin/python -m pytest -q`

This tests the handoff helper scripts. To run the inherited application's original tests after `prepare_application.py`:

- Windows: `.\.venv\Scripts\python.exe scripts\run_application_tests.py`
- macOS/Linux: `./.venv/bin/python scripts/run_application_tests.py`

The inherited test helper runs pytest from `application/` to use the original application package imports. The inherited test suite uses the original data available in `application/data`. Do not claim the partner operated the app merely because automated tests passed.

## 16. AI Usage

AI helped organize this guide, draft preflight and source controls, and propose tests. Automated helper tests were executed locally; results and remaining verification needs are recorded in [`AI_LOG.md`](AI_LOG.md). AI did not observe a classmate or fabricate their responses. The **author must remain silent** during the actual partner run.

---

## Silent handoff — complete only after a real classmate test

Read [`docs/SILENT_HANDOFF_PROTOCOL.md`](docs/SILENT_HANDOFF_PROTOCOL.md). The partner attempts all tasks in [`docs/OPERATOR_TASK_SHEET.md`](docs/OPERATOR_TASK_SHEET.md), while the author records results in [`docs/HANDOFF_OBSERVATION_TEMPLATE.md`](docs/HANDOFF_OBSERVATION_TEMPLATE.md). After the test, document real difficulties in [`docs/PROBLEMS_FOUND_TEMPLATE.md`](docs/PROBLEMS_FOUND_TEMPLATE.md), make **two additional improvements based on the actual issues**, record their before/change/after in [`docs/POST_HANDOFF_IMPROVEMENTS_TEMPLATE.md`](docs/POST_HANDOFF_IMPROVEMENTS_TEMPLATE.md), and complete [`docs/REFLECTION_TEMPLATE.md`](docs/REFLECTION_TEMPLATE.md).

**No partner observations, post-handoff improvements, or reflection answers are claimed as complete in this starter submission.** The preflight and pause/resume helpers are **pre-handoff usability improvements**, not substitutes for the two changes that must follow the real partner test.


## Handoff report working draft

A proposed operator report for Megan Kahn is saved at [`docs/MEGAN_KAHN_HANDOFF_REPORT_DRAFT.md`](docs/MEGAN_KAHN_HANDOFF_REPORT_DRAFT.md). Its observation entries and reflection are **not verified test evidence**. The author must confirm what happened during an actual silent handoff; the operator must be an assigned classmate unless the instructor authorizes a substitute. Real outcomes and genuinely post-handoff improvements belong in the corresponding templates in `docs/`.
