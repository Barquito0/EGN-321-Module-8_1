# EGN 321 — Assignment 8.1
## Operating Documentation and Silent Handoff Report

**Project:** Unattended Sensor Monitoring System  
**Developer:** Marco Ruiz  
**Proposed handoff operator:** Megan Kahn  
**Application:** Flask dashboard with SQLite sensor history

> **Draft for operator and author review.** The following observation entries and first-person reflections were supplied as proposed report wording, not independently verified against a completed silent handoff. Confirm them against actual operator notes and screenshots before presenting them as test evidence. The assignment specifies an assigned classmate; using a family member requires instructor approval.

## 1. Handoff Test Overview

This handoff evaluates whether another person can operate the application by following the GitHub README and included files without verbal assistance. The operator is asked to install the dependencies, launch the system, interpret temperature and status information, locate the logs, identify a failure, and follow recovery instructions. The observer must remain silent and record mistakes, questions, and successful steps.

## 2. Handoff Observation Table — Draft Entries to Confirm

| Step | Proposed operator action / observation | Proposed result | Confusion to confirm | Improvement |
|---|---|---|---|---|
| Locate application | Opened the GitHub repository | Yes | None | None |
| Understand purpose | Read the README project overview | Yes | Some technical terms unfamiliar | Use simpler explanations |
| Installation | Followed Python installation instructions | Yes | Was unsure which terminal command to use | Emphasize a single command for each OS |
| Start application | Started Python monitoring process | Partial | Tried `app.py` instead of `supervisor.py` | Make recommended startup command prominent |
| Normal operation | Opened Flask dashboard in browser | Yes | None | None |
| Sensor input | Observed included temperature replay data | Yes | Unclear whether data came from a physical sensor | Label classroom replay origin |
| Interpret results | Viewed latest temperature and historical chart | Yes | Needed to confirm temperature units | Display °C beside readings |
| System health | Located HEALTHY state | Yes | DEGRADED meaning unclear | Explain health states |
| Logs | Searched for application events | Partial | Looked in root before `logs/monitor.jsonl` | Make exact location prominent |
| Failure condition | Followed stop-replay instructions | Yes | Unclear how soon status should change | Explain 8-second stale and 18-second failed thresholds |
| Recovery | Resumed replay input | Yes | Initially checked dashboard but not log | Add recovery-verification checklist |
| Known limitations | Read limitations section | Yes | None | None |

**Evidence to collect when verified:** real operator time, whether developer stayed silent, screenshot(s) of the operator's dashboard and steps, actual command output, and the observer's notes. Replace any proposed outcome that differs from what happened.

## 3. Problems Identified — Proposed Discussion

A first-time operator may have trouble choosing between `app.py` and `supervisor.py`. The latter is the recommended unattended method because it restarts the Flask child process. Another potential problem is locating `logs/monitor.jsonl` inside the fetched `application/` folder. The health states can also be confusing until the guide explains what DEGRADED and FAILED mean, and distinguishes historic source time from replay arrival time. These are proposed observations to check, not verified failures from an operator.

## 4. Improvements to Evaluate After the Handoff

### Improvement 1 — Clearer Startup Instructions

**Before:** Several startup methods can make it unclear which provides automatic restart.  
**Change prepared before handoff:** The Quick Start prominently recommends `python scripts/start_monitor.py`, which launches the inherited `supervisor.py`; direct `python app.py` lacks that supervision.  
**After / success criterion:** Operator can start the application from the repository without asking which script to run. Confirm this in a follow-up test before counting it as a post-handoff improvement.

### Improvement 2 — Better Health and Recovery Instructions

**Before:** Health-state meanings and the replay recovery process are scattered across technical documentation.  
**Change prepared before handoff:** Added clear meanings for HEALTHY, DEGRADED, FAILED, and RECOVERING, plus `scripts/source_control.py pause|resume|status`, preflight diagnostics, and recovery checks.  
**After / success criterion:** Operator can identify stale input, resume the replay, and confirm a new accepted reading, SQLite access and logs. Confirm in a follow-up test before counting it as a post-handoff improvement.

## 5. Evidence Checklist

- [ ] Record actual date/time, operator name, and author silence.
- [ ] Record commands used and whether each task succeeded.
- [ ] Capture authentic dashboard, log, and recovery evidence.
- [ ] Confirm any confusion reported in the table above.
- [ ] Make and test **two additional changes after** reviewing the actual observations, or document and verify genuinely post-test changes.

## 6. Reflection — Draft Answers to Revise from Experience

### Question 1: What did your partner struggle with that seemed obvious to you while developing the application?

A new operator can struggle to know which command to use when starting the application. Finding the logs and interpreting the health states may also be confusing. Those steps felt simple to me while developing the system because I already knew its file structure and how the monitoring process works. The handoff is intended to reveal where my documentation assumes that knowledge.

### Question 2: What was the most important improvement you made after the handoff test?

Making startup and recovery instructions easier to follow is likely to have the largest effect. Clear steps reduce the chance that someone starts Flask without the supervisor or misreads old sensor data as current. After the handoff, I will identify the most important *observed* issue and describe the specific verified change I made in response.

### Question 3: If you could no longer support this application personally, what additional documentation or automation would you add?

I would add a setup program to check Python, dependencies, and the SQLite database automatically. I would also add a troubleshooting page in the dashboard to explain common errors and the log locations. These would help a new operator run and maintain the tool without depending on me.

## 7. Conclusion

The intended goal is that an unfamiliar operator can install, run, interpret, and recover the monitoring system using only the repository's documentation. The operator's actual attempts are needed to determine whether the guide achieves that goal. This draft provides a structured place to document the result without changing the measured source data or manufacturing screenshots.
