# Hack Day Nairobi — Preparation Plan (Oct 30)

Target: **Hacktoberfest Hack Day Nairobi x iTech Club**
Zetech University Technology Park, Mang'u Campus — Fri Oct 30 7:00PM → Oct 31 6:00AM EAT

## Challenges (from the MLH event)

| Challenge | id | Requirement |
|-----------|----|-------------|
| Best Use of Gemma 4 | `01a03b87-be22-9180-5e2d-b3beeb66666d` | Build with Gemma 4 (lightweight, multimodal, open weights via Gemini API). Text + images, focused AI tool, rapid prototyping. |
| Best Open-Source AI Project | `01a0d987-0c41-12ea-13ac-5b85755dc2f3` | Original project, open-source/open-weight AI central, public GitHub repo + open-source license. |

One project may enter both — both are genuinely used.

## Strategy: extend Touch Grass Birder → audio + photo ID

**Track A (offline audio — already built):**
- BirdNET (acoustic, local) + Gemma 3 1B (llama.cpp) field notes. MIT repo, live on Render.

**Track B (Gemma 4 multimodal — new, Hack Day capstone):**
- New `POST /api/vision`: upload a bird photo → **Gemma 4** (via Gemini API) returns species guess + behavior/field-mark note (multimodal).
- Frontend: add a "Snap a photo" tile next to "Listen".
- Keep a local fallback so the app still works with signal-out if the API key is absent.

## What we need before the event

1. **Gemini API key (free)** — Google AI Studio: `https://aistudio.google.com/apikey`. This is the only hard dependency for Track B. (Gemma API docs: links from the event page.)
2. Optionally deploy the demo to **DigitalOcean App Platform** (account already connected); DO published a skill for the event: `npx skills add digitalocean-labs/do-app-platform-skills`.
3. Weeks 2–4 DEV Challenge projects (Oct 12/19/26) — any that fit outdoors/AI fold into the same repo or are demoed alongside.

## Event-day flow

1. Check in (code/venue; self check-in opens when event starts).
2. Demo Birder audio ID + photo ID; walk the judges through the architecture diagram.
3. Submit project via MLH + enter the two challenges above (actively submitting on the day).
4. Sticker book: attending this Fest earns the "Attend an in-person Fest" sticker.

## Open questions for the user

- Get a Gemini API key (free) so Track B is testable before Oct 30?
- Install the DO App Platform skill now for a second deployment?
- Countdown: Weeks 2–4 builds also run in this repo — confirm reuse vs. new repo.