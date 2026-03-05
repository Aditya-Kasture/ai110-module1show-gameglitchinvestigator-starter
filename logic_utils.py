def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX: Hard was returning 1-50 (easier than Normal). Changed to 1-500.
    if difficulty == "Hard":
        return 1, 500
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # Refactored from app.py using Copilot Agent mode
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: The original hints were inverted — "Go HIGHER!" appeared when the
    # guess was too high (should say "Go LOWER!") and vice versa.
    # FIXME was marked at the original check_guess in app.py.
    if guess == secret:
        return "Win", "Correct!"

    if guess > secret:
        # FIX: Corrected from "Go HIGHER!" to "Go LOWER!"
        return "Too High", "Too high! Go LOWER."
    else:
        # FIX: Corrected from "Go LOWER!" to "Go HIGHER!"
        return "Too Low", "Too low! Go HIGHER."


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # Refactored from app.py using Copilot Agent mode
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIX: Original code rewarded +5 for "Too High" on even attempts, which
    # made no sense. Wrong guesses should always cost points.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
