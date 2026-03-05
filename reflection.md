# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, several things were immediately wrong.

**Bug 1 — Inverted hints:** When I guessed a number that was too high (e.g., guessing 80 when the secret was 50), the game told me "Go HIGHER!" — the exact opposite of the correct hint. The same was true in reverse: guessing too low showed "Go LOWER!" This made it impossible to converge on the secret number using the hints.

**Bug 2 — Secret type alternation:** On every even-numbered attempt, the code secretly converted the target number to a string before comparing. This meant comparisons like `40 > "50"` were being evaluated, causing a TypeError fallback that performed string-based comparison — where `"9" > "50"` is `True` because Python compares strings character by character. The game appeared to give inconsistent results with no obvious cause.

**Bug 3 — Hard difficulty easier than Normal:** The Hard difficulty setting returned a range of 1–50, which is actually narrower (easier) than Normal's 1–100. A player choosing Hard expecting a challenge would find it easier to guess in Hard than Normal.

**Bonus bugs noticed:** The UI always said "Guess a number between 1 and 100" regardless of difficulty. The "New Game" button always picked a random number from 1–100 ignoring difficulty. The attempt counter started at 1 (not 0), causing the "attempts left" display to be off by one from the start. Wrong guesses on even attempts gave +5 to score instead of -5.

---

## 2. How did you use AI as a teammate?

I used Claude Code (Claude Sonnet 4.6) as my AI pair programmer throughout this project.

**Correct suggestion:** I asked the AI to explain why the hints were backwards, and it correctly identified that the return values in `check_guess` had the messages swapped — "Go HIGHER!" was in the `guess > secret` branch and "Go LOWER!" was in the else branch. I verified this by tracing through the code manually: if `guess=80` and `secret=50`, then `80 > 50` is True, so it returned "Go HIGHER!" which is wrong. The fix was simple: swap the messages. I confirmed it in the live app by guessing a high number and checking the hint.

**Incorrect/misleading suggestion:** When I asked about the score behavior, an initial pass suggested that the +5 bonus on even "Too High" attempts might be intentional as a "risk/reward" mechanic. But this interpretation doesn't hold up: the game has no explanation of this mechanic to the user, and it rewards incorrect guesses in an arbitrary way (based on attempt parity, not skill). I rejected this framing and removed the asymmetric logic, making all wrong guesses cost 5 points consistently. I verified by running `test_score_decreases_on_wrong_guess` in pytest.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed when two conditions were met: the relevant pytest test passed, and I manually verified the behavior in the live Streamlit app.

For the inverted hints bug, I ran `pytest tests/test_game_logic.py` before and after the fix. Before the fix, `test_hint_too_high_says_go_lower` failed because the message contained "HIGHER" instead of "LOWER." After moving the corrected `check_guess` into `logic_utils.py`, all five original-style tests passed and the two new hint-direction tests also passed.

For the string/int alternation bug, I verified it manually by submitting two guesses in sequence (making the second attempt be attempt #2, an even number) and observing that the comparison now behaved correctly in both cases. I also added `test_hard_range_is_harder_than_normal` and `test_score_decreases_on_wrong_guess` to confirm the difficulty range and score fixes.

AI helped me understand what a good test looked like: rather than testing implementation details, test observable outcomes. For example, instead of checking that `guess > secret` returns a specific string literal, I check that the word "LOWER" appears anywhere in the message — making the test more resilient to minor wording changes.

---

## 4. What did you learn about Streamlit and state?

In the original app, the secret number kept changing because every time you interacted with the page (clicked a button, typed in an input), Streamlit re-ran the entire Python script from top to bottom. Without `st.session_state`, the line `random.randint(low, high)` executed again on every rerun, generating a new secret each time.

Streamlit "reruns" are how the framework updates the UI: any user interaction triggers a fresh execution of the whole script. `st.session_state` is a dictionary that persists across these reruns, so values stored there survive each refresh. Think of it like a sticky note that Streamlit keeps on the side — the script re-reads it on every run instead of starting from scratch.

The fix that gave the game a stable secret was wrapping the random number generation in `if "secret" not in st.session_state:` — this ensures the secret is only generated once (on the very first run), and on all subsequent reruns it reads the already-stored value.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is the "read before you fix" approach: before touching any code, I read the entire file to understand the full picture. Several of the bugs in this project were only visible in context — the string/int alternation bug only made sense after seeing how `secret` was passed to `check_guess` a few lines later.

Next time I work with AI on a coding task, I would give it more specific, constrained prompts. Broad prompts like "fix the score logic" led to a rationalization of buggy behavior. Narrow prompts like "this function takes two ints and should return 'Too High' when guess > secret — is it doing that?" led to accurate analysis.

This project changed how I think about AI-generated code: it can produce syntactically valid, confidently-written code that is logically wrong in subtle ways (inverted conditions, type mismatches). Human review isn't optional — it's the most important step.
