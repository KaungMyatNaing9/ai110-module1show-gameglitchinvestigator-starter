import pytest
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score, get_temperature

# ---------------------------------------------------------------------------
# get_temperature — range 1-100 used for most tests (range = 99)
# ---------------------------------------------------------------------------

class TestGetTemperature:
    # Exact match
    def test_exact_returns_exact(self):
        assert get_temperature(50, 50, 1, 100) == "🎯 Exact!"

    def test_exact_at_boundary_low(self):
        assert get_temperature(1, 1, 1, 100) == "🎯 Exact!"

    def test_exact_at_boundary_high(self):
        assert get_temperature(100, 100, 1, 100) == "🎯 Exact!"

    # Scorching — distance <= 10% of range (range=100 → ≤10 away)
    def test_scorching_very_close(self):
        # distance 5 / range 100 = 5% → Scorching
        assert get_temperature(55, 50, 1, 101) == "🔥 Scorching"

    def test_scorching_boundary(self):
        # distance 10 / range 100 = 10% → Scorching (boundary inclusive)
        assert get_temperature(60, 50, 1, 101) == "🔥 Scorching"

    # Hot — distance <= 20% of range
    def test_hot(self):
        # distance 15 / range 100 = 15% → Hot
        assert get_temperature(65, 50, 1, 101) == "🌶️ Hot"

    # Warm — distance <= 35% of range
    def test_warm(self):
        # distance 25 / range 100 = 25% → Warm
        assert get_temperature(75, 50, 1, 101) == "🌤️ Warm"

    # Cold — distance <= 50% of range
    def test_cold(self):
        # distance 40 / range 100 = 40% → Cold
        assert get_temperature(90, 50, 1, 101) == "❄️ Cold"

    # Freezing — distance > 50% of range
    def test_freezing(self):
        # distance 60 / range 100 = 60% → Freezing
        assert get_temperature(10, 70, 1, 101) == "🧊 Freezing"

    # Works symmetrically — above and below secret same label
    def test_symmetric_above_and_below(self):
        above = get_temperature(60, 50, 1, 101)
        below = get_temperature(40, 50, 1, 101)
        assert above == below

    # Easy difficulty range (1-20, range=19)
    def test_easy_scorching(self):
        # distance 1 / range 19 ≈ 5% → Scorching
        assert get_temperature(10, 9, 1, 20) == "🔥 Scorching"

    def test_easy_freezing(self):
        # distance 18 / range 19 ≈ 95% → Freezing
        assert get_temperature(1, 19, 1, 20) == "🧊 Freezing"

    # Hard difficulty range (1-50, range=49)
    def test_hard_warm(self):
        # distance 12 / range 49 ≈ 24% → Warm
        assert get_temperature(37, 25, 1, 50) == "🌤️ Warm"


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
    """
    Scoring: 100 points per match, deducted equally per attempt used.
    Deduction = 100 / attempt_limit per attempt.
    Loss always returns 0. attempt_number is 1-indexed.
    """

    # --- Easy (limit=6): deduction = 100/6 ≈ 16.67 per attempt ---
    def test_easy_win_attempt_1(self):
        # 100 - 0 deductions = 100
        assert update_score("Win", 1, 6) == 100

    def test_easy_win_attempt_2(self):
        # 100 - 1*(100/6) = 83.33 → rounds to 83
        assert update_score("Win", 2, 6) == 83

    def test_easy_win_attempt_3(self):
        # 100 - 2*(100/6) = 66.67 → rounds to 67
        assert update_score("Win", 3, 6) == 67

    def test_easy_win_attempt_6(self):
        # 100 - 5*(100/6) = 16.67 → rounds to 17
        assert update_score("Win", 6, 6) == 17

    def test_easy_loss(self):
        assert update_score("Too Low", 6, 6) == 0
        assert update_score("Too High", 6, 6) == 0

    # --- Normal (limit=8): deduction = 100/8 = 12.5 per attempt ---
    def test_normal_win_attempt_1(self):
        assert update_score("Win", 1, 8) == 100

    def test_normal_win_attempt_2(self):
        # 100 - 1*12.5 = 87.5 → rounds to 88
        assert update_score("Win", 2, 8) == 88

    def test_normal_win_attempt_8(self):
        # 100 - 7*12.5 = 12.5 → rounds to 12 or 13
        result = update_score("Win", 8, 8)
        assert result == round(100 - 7 * (100 / 8))

    def test_normal_loss(self):
        assert update_score("Too Low", 8, 8) == 0

    # --- Hard (limit=5): deduction = 100/5 = 20 per attempt ---
    def test_hard_win_attempt_1(self):
        assert update_score("Win", 1, 5) == 100

    def test_hard_win_attempt_2(self):
        # 100 - 1*20 = 80
        assert update_score("Win", 2, 5) == 80

    def test_hard_win_attempt_3(self):
        # 100 - 2*20 = 60
        assert update_score("Win", 3, 5) == 60

    def test_hard_win_attempt_5(self):
        # 100 - 4*20 = 20
        assert update_score("Win", 5, 5) == 20

    def test_hard_loss(self):
        assert update_score("Too High", 5, 5) == 0

    # --- General rules ---
    def test_first_attempt_always_100_regardless_of_difficulty(self):
        for limit in (5, 6, 8):
            assert update_score("Win", 1, limit) == 100

    def test_score_decreases_with_more_attempts(self):
        for limit in (5, 6, 8):
            scores = [update_score("Win", a, limit) for a in range(1, limit + 1)]
            assert scores == sorted(scores, reverse=True), f"Scores not decreasing for limit={limit}"

    def test_score_never_goes_negative(self):
        for limit in (5, 6, 8):
            for attempt in range(1, limit + 1):
                assert update_score("Win", attempt, limit) >= 0

    def test_loss_outcomes_all_return_zero(self):
        for outcome in ("Too High", "Too Low", "Bogus"):
            assert update_score(outcome, 3, 6) == 0


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
        limit = ATTEMPT_LIMIT["Normal"]
        score = update_score(outcome, 1, limit)
        assert score == 100

    def test_game_reaches_attempt_limit_easy(self):
        """Simulate exhausting all Easy attempts with wrong guesses → score is 0."""
        limit = ATTEMPT_LIMIT["Easy"]
        final_outcome = None
        for attempt in range(1, limit + 1):
            final_outcome, _ = check_guess(1, 100)  # always "Too Low"
        score = update_score(final_outcome, limit, limit)
        assert score == 0
        assert attempt == limit

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
