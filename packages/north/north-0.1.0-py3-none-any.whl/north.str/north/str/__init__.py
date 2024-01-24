import re


def _space_numbers(match: re.Match[str]) -> str:
    return f"{match.group(1)} {match.group(2)} {match.group(3)}"


def _add_word_boundaries_to_numbers(s: str) -> str:
    pattern = re.compile(r"([a-zA-Z])(\d+)([a-zA-Z]?)")
    return pattern.sub(_space_numbers, s)


def _to_camel_init_case(s: str, init_case: bool) -> str:
    s = _add_word_boundaries_to_numbers(s)
    s = s.strip(" ")
    n = ""
    cap_next = init_case
    for v in s:
        if (v >= "A" and v <= "Z") or (v >= "0" and v <= "9"):
            n += v
        if v >= "a" and v <= "z":
            if cap_next:
                n += v.upper()
            else:
                n += v
        if v == "_" or v == " " or v == "-":
            cap_next = True
        else:
            cap_next = False
    return n


def _to_screaming_delimited(s: str, sep: str, screaming: bool) -> str:
    s = _add_word_boundaries_to_numbers(s)
    s = s.strip(" ")
    n = ""
    for i, v in enumerate(s):
        next_case_is_changed = False
        if i + 1 < len(s):
            next_char = s[i + 1]
            if (v >= "A" and v <= "Z" and next_char >= "a" and next_char <= "z") or (
                v >= "a" and v <= "z" and next_char >= "A" and next_char <= "Z"
            ):
                next_case_is_changed = True

        if i > 0 and n[-1] != sep and next_case_is_changed:
            if v >= "A" and v <= "Z":
                n += sep + v
            elif v >= "a" and v <= "z":
                n += v + sep
        elif v == " " or v == "_" or v == "-":
            n += sep
        else:
            n += v
    if screaming:
        n = n.upper()
    else:
        n = n.lower()
    return n


def to_camel(s: str) -> str:
    return _to_camel_init_case(s, True)


def to_lower_camel(s: str) -> str:
    if not s:
        return s
    if s[0] >= "A" and s[0] <= "Z":
        s = s[0].lower() + s[1:]
    return _to_camel_init_case(s, False)


def to(s: str, sep: str, screaming: bool) -> str:
    return _to_screaming_delimited(s, sep, screaming)


def to_screaming(s: str, sep: str) -> str:
    return _to_screaming_delimited(s, sep, True)


def to_delimited(s: str, sep: str) -> str:
    return _to_screaming_delimited(s, sep, False)


def to_kebab(s: str) -> str:
    return _to_screaming_delimited(s, "-", False)


def to_snake(s: str) -> str:
    return _to_screaming_delimited(s, "_", False)


def to_screaming_kebab(s: str) -> str:
    return _to_screaming_delimited(s, "-", True)


def to_screaming_snake(s: str) -> str:
    return _to_screaming_delimited(s, "_", True)


def to_lower(s: str) -> str:
    return s.lower()


def to_upper(s: str) -> str:
    return s.upper()


def to_title(s: str) -> str:
    return s.title()
