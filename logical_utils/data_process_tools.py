def insert_not_before_last_in_list(lst):
    try:
        last_in_index = len(lst) - 1 - lst[::-1].index('in')
        lst.insert(last_in_index, 'not')
        return lst
    except ValueError:
        pass


def insert_not_before_last_in_str(s):
    index = s.rfind('in')
    if index != -1:
        s = s[:index] + 'not ' + s[index:]
    return s


def insert_not_before_first_in(lst):
    try:
        first_in_index = lst.index('in')
        lst.insert(first_in_index, 'not')
    except ValueError:
        pass


def insert_not_before_first_in(s):
    index = s.find('in')
    if index != -1:
        s = s[:index] + 'not' + s[index:]
    return s


def match_substrings_in_order(string, substrings):
    last_pos = 0
    for substr in substrings:
        pos = string.find(substr, last_pos)
        if pos == -1:
            return False
        last_pos = pos + len(substr)
    return True


def obtain_label(L, index):
    return L[index]


def find_last_str_index(L, str):
    return max((i for i, x in enumerate(L) if x == str), default=-1)


def check_not_together_exist(s, x, y):
    return not (x in s and y in s)


def truncate_from_last_str(s, str):
    index = s.rfind(str)
    if index != -1:
        return s[:index]
    return s