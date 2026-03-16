def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
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
    if guess == secret:
        return "Win", "🎉 Correct!"
#FIXME: The hints ae reversed
    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(outcome: str, attempt_number: int, attempt_limit: int) -> int:
    """Calculate the final score for a completed game.

    Win:  100 points minus an equal deduction for each attempt used.
          Deduction per attempt = 100 / attempt_limit.
          Examples (Easy, limit=6): win attempt 1 → 100, attempt 6 → ~17.
    Loss: 0 points.

    attempt_number is 1-indexed (1 = first guess).
    """
    if outcome == "Win":
        points_per_attempt = 100 / attempt_limit
        score = round(100 - (attempt_number - 1) * points_per_attempt)
        return max(score, 0)

    return 0
