__author__ = 'shovan'


def who_is_this(s):
    try:
        int(s)
        return True
    except ValueError:
        return False