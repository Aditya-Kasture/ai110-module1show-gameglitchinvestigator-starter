# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** A number-guessing game where the player picks a difficulty, gets a range, and tries to guess the secret number within a limited number of attempts using higher/lower hints.

**Bugs found:**
1. Inverted hints — "Go HIGHER!" when guess was too high, "Go LOWER!" when too low.
2. Secret alternated between `int` and `str` on even attempts, breaking comparisons.
3. Hard difficulty returned range 1–50 (easier than Normal's 1–100).
4. Hardcoded "between 1 and 100" in UI regardless of difficulty.
5. New Game button ignored difficulty when picking a new secret.
6. Wrong guesses on even attempts gave +5 to score instead of -5.
7. All functions in `logic_utils.py` raised `NotImplementedError` — tests always failed.

**Fixes applied:**
- Corrected hint messages in `check_guess` (Too High → Go LOWER, Too Low → Go HIGHER).
- Removed the `str()` conversion on even attempts; secret is always compared as `int`.
- Fixed Hard difficulty range to 1–500.
- Refactored all game logic from `app.py` into `logic_utils.py` and updated imports.
- Fixed UI range display and New Game button to use `get_range_for_difficulty`.
- Made all wrong guesses consistently deduct 5 points.
- Updated and expanded tests (10 total, all passing).

## 📸 Demo

- All 10 pytest tests passing:

```
tests/test_game_logic.py::test_winning_guess PASSED
tests/test_game_logic.py::test_guess_too_high PASSED
tests/test_game_logic.py::test_guess_too_low PASSED
tests/test_game_logic.py::test_hint_too_high_says_go_lower PASSED
tests/test_game_logic.py::test_hint_too_low_says_go_higher PASSED
tests/test_game_logic.py::test_parse_valid_integer PASSED
tests/test_game_logic.py::test_parse_empty_string PASSED
tests/test_game_logic.py::test_parse_non_number PASSED
tests/test_game_logic.py::test_hard_range_is_harder_than_normal PASSED
tests/test_game_logic.py::test_score_decreases_on_wrong_guess PASSED
10 passed in 0.02s
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
