from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# --- check_guess tests ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_hint_too_high_says_go_lower():
    # FIX verification: original bug had "Go HIGHER!" when guess was too high.
    # Confirm the hint message now correctly says to go lower.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


def test_hint_too_low_says_go_higher():
    # FIX verification: original bug had "Go LOWER!" when guess was too low.
    # Confirm the hint message now correctly says to go higher.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


# --- parse_guess tests ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None


def test_parse_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert err == "That is not a number."


# --- get_range_for_difficulty tests ---

def test_hard_range_is_harder_than_normal():
    # FIX verification: Hard was 1-50 (easier than Normal's 1-100). Now 1-500.
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high


# --- update_score tests ---

def test_score_decreases_on_wrong_guess():
    # FIX verification: original gave +5 on "Too High" for even attempts.
    # Wrong guesses should always cost points.
    score_after = update_score(100, "Too High", 2)
    assert score_after < 100

    score_after = update_score(100, "Too Low", 3)
    assert score_after < 100
