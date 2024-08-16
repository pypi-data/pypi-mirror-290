from datetime import timedelta

def get_timedelta_for_freq(freq: str) -> timedelta:
    """Returns the appropriate timedelta object based on the frequency."""
    if freq == '1m':
        return timedelta(minutes=1)
    elif freq == '3m':
        return timedelta(minutes=3)
    elif freq == '5m':
        return timedelta(minutes=5)
    elif freq == '15m':
        return timedelta(minutes=15)
    elif freq == '1h':
        return timedelta(hours=1)
    elif freq == '1d' or freq == 'd':
        return timedelta(days=1)
    else:
        raise ValueError(f"Frequency '{freq}' is not supported.")
