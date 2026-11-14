# text.py - string helpers not covered by the builtin `string` module

def words(s):
    return s.split()

def lines(s):
    return s.splitlines()

def truncate(s, n, suffix="..."):
    if len(s) <= n:
        return s
    return s[:n] + suffix

def wrap(s, width):
    words_list = s.split()
    out = []
    line = ""
    for w in words_list:
        if not line:
            line = w
        elif len(line) + 1 + len(w) <= width:
            line = line + " " + w
        else:
            out.append(line)
            line = w
    if line:
        out.append(line)
    return "\n".join(out)

def title_case(s):
    return " ".join(w.capitalize() for w in s.split())

def snake_case(s):
    out = []
    for i, ch in enumerate(s):
        if ch.isupper():
            if i > 0:
                out.append("_")
            out.append(ch.lower())
        elif ch == " " or ch == "-":
            out.append("_")
        else:
            out.append(ch)
    return "".join(out)

def camel_case(s):
    parts = s.replace("-", "_").split("_")
    if not parts:
        return ""
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])

def count_of(s, sub):
    if not sub:
        return 0
    return s.count(sub)

def is_palindrome(s):
    clean = "".join(c for c in s.lower() if c.isalnum())
    return clean == clean[::-1]
