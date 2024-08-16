def fuzzy_dict_key(d: dict, k: str):
    K = k.upper()
    all_keys = list(d.keys())
    match_count = 0
    the_match = None
    for a_k in all_keys:
        if a_k.upper().find(K) < 0:
            pass
        else:
            the_match = a_k
            match_count += 1

    if match_count == 1:
        return the_match

    return None


def fuzzy_list_find(all_strings: list, needle: str):
    NEEDLE = needle.upper()
    match_count = 0
    the_match = None
    for a_string in all_strings:
        if a_string.upper().find(NEEDLE) < 0:
            pass
        else:
            the_match = a_string
            match_count += 1

    if match_count == 1:
        return the_match

    return None
