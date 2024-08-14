import random


def guess_my_age(min_age=10, max_age=150):
    if min_age >= max_age:
        raise ValueError("Min age can not be greater than or equal to Max age.")
    random.randint(min_age, max_age)
