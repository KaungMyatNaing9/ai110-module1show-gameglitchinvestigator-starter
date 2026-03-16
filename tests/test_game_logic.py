import pytest
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

# ---------------------------------------------------------------------------
# check_guess
# NOTE: check_guess returns a TUPLE (outcome, message), not a plain string.
# ---------------------------------------------------------------------------

class TestCheckGuessWin:
    def test_exact_match(self):
        outcome, msg = check_guess(50, 50)
        assert outcome == "Win"

    def test_win_message_contains_correct(self):
        _, msg = check_guess(50, 50)
        assert "Correct" in msg

    def test_win_at_boundary_low(self):
        outcome, _ = check_guess(1, 1)
        assert outcome == "Win"

    def test_win_at_boundary_high(self):
        outcome, _ = check_guess(100, 100)
        assert outcome == "Win"

    def test_win_at_zero(self):
        outcome, _ = check_guess(0, 0)
        assert outcome == "Win"

    def test_win_negative(self):
        outcome, _ = check_guess(-5, -5)
        assert outcome == "Win"


class TestCheckGuessHints:
    """Hint direction must match the relationship between guess and secret."""

    # --- Go LOWER (guess is too high) ---
    def test_guess_above_secret_outcome(self):
        outcome, _ = check_guess(60, 50)
        assert outcome == "Too High"

    def test_guess_above_secret_hint_says_lower(self):
        _, msg = check_guess(60, 50)
        assert "LOWER" in msg or "lower" in msg.lower()

    def test_guess_one_above_secret(self):
        outcome, msg = check_guess(51, 50)
        assert outcome == "Too High"
        assert "LOWER" in msg or "lower" in msg.lower()

    def test_guess_far_above_secret(self):
        outcome, _ = check_guess(1000, 1)
        assert outcome == "Too High"

    # --- Go HIGHER (guess is too low) ---
    def test_guess_below_secret_outcome(self):
        outcome, _ = check_guess(40, 50)
        assert outcome == "Too Low"

    def test_guess_below_secret_hint_says_higher(self):
        _, msg = check_guess(40, 50)
        assert "HIGHER" in msg or "higher" in msg.lower()

    def test_guess_one_below_secret(self):
        outcome, msg = check_guess(49, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in msg or "higher" in msg.lower()

    def test_guess_far_below_secret(self):
        outcome, _ = check_guess(1, 1000)
        assert outcome == "Too Low"

    # --- Hints must NOT be swapped ---
    def test_hint_not_swapped_high(self):
        """When guess > secret, hint must NOT say HIGHER."""
        _, msg = check_guess(99, 1)
        assert "HIGHER" not in msg

    def test_hint_not_swapped_low(self):
        """When guess < secret, hint must NOT say LOWER."""
        _, msg = check_guess(1, 99)
        assert "LOWER" not in msg

    # --- Negative and zero boundaries ---
    def test_guess_zero_secret_positive(self):
        outcome, _ = check_guess(0, 10)
        assert outcome == "Too Low"

    def test_guess_negative(self):
        outcome, _ = check_guess(-10, 5)
        assert outcome == "Too Low"

    def test_secret_negative(self):
        outcome, _ = check_guess(5, -10)
        assert outcome == "Too High"


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

class TestGetRangeForDifficulty:
    def test_easy_range(self):
        assert get_range_for_difficulty("Easy") == (1, 20)

    def test_normal_range(self):
        assert get_range_for_difficulty("Normal") == (1, 100)

    def test_hard_range(self):
        assert get_range_for_difficulty("Hard") == (1, 50)

    def test_unknown_difficulty_defaults_to_normal(self):
        assert get_range_for_difficulty("Unknown") == (1, 100)

    def test_empty_string_defaults(self):
        assert get_range_for_difficulty("") == (1, 100)

    def test_easy_low_bound(self):
        low, _ = get_range_for_difficulty("Easy")
        assert low == 1

    def test_easy_high_bound(self):
        _, high = get_range_for_difficulty("Easy")
        assert high == 20

    def test_hard_high_bound(self):
        _, high = get_range_for_difficulty("Hard")
        assert high == 50

    def test_normal_high_bound(self):
        _, high = get_range_for_difficulty("Normal")
        assert high == 100

    def test_each_difficulty_low_starts_at_one(self):
        for diff in ("Easy", "Normal", "Hard"):
            low, _ = get_range_for_difficulty(diff)
            assert low == 1, f"{diff} low should be 1"

    def test_case_sensitive_easy(self):
        """'easy' (lowercase) is not a recognized difficulty."""
        assert get_range_for_difficulty("easy") == (1, 100)  # falls through to default


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

class TestParseGuess:
    # --- Invalid / empty ---
    def test_none_input(self):
        ok, val, err = parse_guess(None)
        assert ok is False and val is None and err == "Enter a guess."

    def test_empty_string(self):
        ok, val, err = parse_guess("")
        assert ok is False and val is None and err == "Enter a guess."

    def test_non_numeric_string(self):
        ok, val, err = parse_guess("abc")
        assert ok is False and val is None and err == "That is not a number."

    def test_special_chars(self):
        ok, val, err = parse_guess("!@#")
        assert ok is False and val is None

    def test_whitespace_only(self):
        ok, _, _ = parse_guess("   ")
        assert ok is False

    # --- Valid integers ---
    def test_valid_integer(self):
        ok, val, err = parse_guess("42")
        assert ok is True and val == 42 and err is None

    def test_valid_integer_one(self):
        ok, val, _ = parse_guess("1")
        assert ok is True and val == 1

    def test_valid_integer_hundred(self):
        ok, val, _ = parse_guess("100")
        assert ok is True and val == 100

    def test_valid_negative_integer(self):
        ok, val, _ = parse_guess("-5")
        assert ok is True and val == -5

    def test_valid_zero(self):
        ok, val, _ = parse_guess("0")
        assert ok is True and val == 0

    # --- Floats (should be truncated to int) ---
    def test_float_truncation(self):
        ok, val, _ = parse_guess("3.7")
        assert ok is True and val == 3

    def test_float_exact(self):
        ok, val, _ = parse_guess("50.0")
        assert ok is True and val == 50

    def test_float_truncates_toward_zero(self):
        ok, val, _ = parse_guess("9.9")
        assert ok is True and val == 9


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

class TestUpdateScore:
    # --- Win: points = max(100 - 10*(attempt_number - 1), 10), attempt is 1-indexed ---
    def test_win_attempt_1_scores_100(self):
        # First guess correct: 100 - 10*(1-1) = 100
        assert update_score(0, "Win", 1) == 100

    def test_win_attempt_2_scores_90(self):
        # 100 - 10*(2-1) = 90
        assert update_score(0, "Win", 2) == 90

    def test_win_attempt_10_scores_10(self):
        # 100 - 10*(10-1) = 10
        assert update_score(0, "Win", 10) == 10

    def test_win_minimum_10_points(self):
        # attempt 11+ → floored at 10
        assert update_score(0, "Win", 11) == 10
        assert update_score(0, "Win", 100) == 10

    def test_win_adds_to_existing_score(self):
        # 50 + 100 = 150
        assert update_score(50, "Win", 1) == 150

    # --- Too High: always -10, attempt number does not matter ---
    def test_too_high_deducts_ten(self):
        assert update_score(100, "Too High", 1) == 90
        assert update_score(100, "Too High", 2) == 90
        assert update_score(100, "Too High", 7) == 90

    def test_too_high_same_penalty_regardless_of_attempt(self):
        # Every attempt deducts the same amount
        results = {update_score(100, "Too High", a) for a in range(1, 10)}
        assert results == {90}

    def test_too_high_score_can_go_negative(self):
        assert update_score(5, "Too High", 1) == -5

    # --- Too Low: always -10, same as Too High ---
    def test_too_low_deducts_ten(self):
        assert update_score(100, "Too Low", 1) == 90
        assert update_score(100, "Too Low", 3) == 90
        assert update_score(100, "Too Low", 7) == 90

    def test_too_low_score_can_go_negative(self):
        assert update_score(5, "Too Low", 1) == -5

    # --- Too High and Too Low must be symmetric ---
    def test_too_high_and_too_low_same_penalty(self):
        for attempt in range(1, 9):
            assert update_score(100, "Too High", attempt) == update_score(100, "Too Low", attempt)

    # --- Unknown outcome: score unchanged ---
    def test_unknown_outcome_unchanged(self):
        assert update_score(42, "SomeOtherOutcome", 3) == 42

    def test_unknown_outcome_zero_score(self):
        assert update_score(0, "Bogus", 1) == 0


# ---------------------------------------------------------------------------
# Game flow: difficulty range + attempt limit integration
# ---------------------------------------------------------------------------

ATTEMPT_LIMIT = {"Easy": 6, "Normal": 8, "Hard": 5}

class TestDifficultyAndAttempts:
    @pytest.mark.parametrize("difficulty,expected_low,expected_high,expected_attempts", [
        ("Easy",   1,  20, 6),
        ("Normal", 1, 100, 8),
        ("Hard",   1,  50, 5),
    ])
    def test_difficulty_config(self, difficulty, expected_low, expected_high, expected_attempts):
        low, high = get_range_for_difficulty(difficulty)
        assert low == expected_low
        assert high == expected_high
        assert ATTEMPT_LIMIT[difficulty] == expected_attempts

    @pytest.mark.parametrize("difficulty", ["Easy", "Normal", "Hard"])
    def test_secret_within_range(self, difficulty):
        import random
        low, high = get_range_for_difficulty(difficulty)
        for _ in range(50):
            secret = random.randint(low, high)
            assert low <= secret <= high

    def test_easy_range_smaller_than_normal(self):
        _, easy_high = get_range_for_difficulty("Easy")
        _, normal_high = get_range_for_difficulty("Normal")
        assert easy_high < normal_high

    def test_hard_range_smaller_than_normal(self):
        _, hard_high = get_range_for_difficulty("Hard")
        _, normal_high = get_range_for_difficulty("Normal")
        assert hard_high < normal_high

    def test_game_win_on_first_attempt(self):
        secret = 42
        ok, guess, _ = parse_guess("42")
        assert ok
        outcome, msg = check_guess(guess, secret)
        assert outcome == "Win"
        score = update_score(0, outcome, 1)
        # attempt_number=1 → 100 - 10*(1-1) = 100
        assert score == 100

    def test_game_reaches_attempt_limit_easy(self):
        """Simulate exhausting all Easy attempts with wrong guesses."""
        limit = ATTEMPT_LIMIT["Easy"]
        score = 0
        for attempt in range(1, limit + 1):
            outcome, _ = check_guess(1, 100)   # always "Too Low"
            score = update_score(score, outcome, attempt)
        # All wrong → each deducts 10
        assert score == -10 * limit
        assert attempt == limit  # we hit the limit

    def test_full_game_win_easy(self):
        """Simulate a single-guess win on Easy."""
        low, high = get_range_for_difficulty("Easy")
        secret = 10
        assert low <= secret <= high
        ok, guess, _ = parse_guess("10")
        assert ok
        outcome, _ = check_guess(guess, secret)
        assert outcome == "Win"

    def test_full_game_too_many_attempts_normal(self):
        """After attempt_limit wrong guesses, game should be considered lost."""
        limit = ATTEMPT_LIMIT["Normal"]
        attempts = 0
        for _ in range(limit):
            ok, guess, _ = parse_guess("1")
            outcome, _ = check_guess(guess, 100)
            attempts += 1
        assert attempts >= limit
        assert outcome != "Win"
