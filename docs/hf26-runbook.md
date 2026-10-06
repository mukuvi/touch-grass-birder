# Hacktoberfest 2026 Runbook — James

One-page plan for finishing the sticker book and every DEV challenge. This is the
source of truth for what to do and when.

## Sticker book (target: 15 = Completionist raffle)

Current: 6/24. Milestone 2 = 10 (bonus holographic sticker).

| # | Sticker | Status | When |
|---|---------|--------|------|
| 1 | Sign in | done | Oct 5 |
| 2 | Add address | done | Oct 5 |
| 3 | Connect DEV account | done | |
| 4 | Submit Week 1 DEV Challenge | done | Oct 6 (live) |
| 5 | Install + log in to DevRelay | done | Oct 5 |
| 6 | Connect DigitalOcean | done | Oct 5 |
| 7 | Pre-event survey | done | |
| 8 | Join MLH Community Discord | TODO (me) | link on hacktoberfest.com/my |
| 9 | Check into a livestream | TODO | see schedule below |
| 10 | Check into 3 livestreams | TODO | |
| 11 | GHW register (GHW: Hacktoberfest) | REGISTERED | Oct 9–15 |
| 12 | GHW livestream check-in | TODO | Fri Oct 9 opening ceremony |
| 13 | GHW 15 points | TODO | Oct 9–15 |
| 14 | GHW 30 points | TODO | |
| 15 | GHW 75 points | TODO | |
| 16 | Week 2 DEV Challenge | not started | Mon Oct 12 |
| 17 | Week 3 DEV Challenge | not started | Mon Oct 19 |
| 18 | Week 4 DEV Challenge | not started | Mon Oct 26 |
| 19 | Post-event survey | TODO | releases later in Oct |
| 20 | Attend Fest (Nairobi Hack Day) | REGISTERED | Oct 30, 7PM EAT |

## Key dates (local = Nairobi, UTC+3)

- Week 1 close: Sun Oct 11, 11:59 PM PDT = Mon Oct 12, 9:59 AM EAT
- GHW: Hacktoberfest: Oct 9 17:00 → Oct 15 20:00
- Week 2 (Oct 12 → Oct 18 · id 80), Week 3 (Oct 19 → 25 · id 81), Week 4 (Oct 26 → Nov 1 · id 82)
- Nairobi Hack Day x iTech Club: Fri Oct 30, 7:00 PM EAT → Oct 31

## Livestreams (check in = code shown on screen)

- Tonight (Oct 6) 8PM: Shopping for Skills and MCP Servers with OpenCode
- Wed Oct 7 5PM: Which Model Actually Wins? Picking Open-Weight Models
- Fri Oct 9 5PM: GHW Opening Ceremony
- Daily through Oct 15: "Today in GHW" + building workshops (schedule: hacktoberfest.com/schedule)

## Challenge playbook (repeat every week)

1. Fetch `get_challenges` → confirm active week; `get_challenge_details` for rubric.
2. Build the project (open-weight model / open-source AI at the core).
3. Draft post from the week's template into `docs/dev-submission-draft.md`.
4. Save the agent session (DevRelay) and embed `{% agent_session <slug> %}`.
5. Commit code + draft, push to `github.com/mukuvi/touch-grass-birder`.
6. Create DEV draft (`published: false`), fill demo URL, publish after user OK.
7. Verify tags (always `hf26challenge`), live demo, MIT repo link, prize categories.

## Week 1 artifacts

- Post: https://dev.to/mukuvi/touch-grass-birder-a-bird-call-identifier-that-works-with-no-signal-1hnp
- Demo: https://touch-grass-birder.onrender.com
- Repo: https://github.com/mukuvi/touch-grass-birder
- Agent session: building-touch-grass-birder-for-the-hf26-week-1-challenge-gb3nc0
- Categories: Best Use of Gemma, Best Use of Render