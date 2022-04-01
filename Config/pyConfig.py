import random


def set_user_sleep_time(mid=5, sig=0.8):
    return random.gauss(mid, sig)

