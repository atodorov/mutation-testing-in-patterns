def validate_percent(percent):
    if percent < 0 or percent > 100:
        raise Exception("Percent must be between 0 and 100")

    return percent
