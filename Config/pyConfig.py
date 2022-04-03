import random


def set_user_sleep_time(mid=5, sig=0.8):
    gauss = random.gauss(mid, sig)
    return [0, gauss][gauss > 0]

