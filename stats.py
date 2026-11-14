# stats.py - mean, median, mode, stddev, percentiles

def mean(xs):
    if not xs:
        return 0
    return sum(xs) / len(xs)

def median(xs):
    if not xs:
        return 0
    s = sorted(xs)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2.0

def mode(xs):
    if not xs:
        return None
    counts = {}
    for x in xs:
        counts[x] = counts.get(x, 0) + 1
    return max(counts, key=counts.get)

def variance(xs):
    if len(xs) < 2:
        return 0
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)

def stddev(xs):
    return variance(xs) ** 0.5

def percentile(xs, p):
    if not xs:
        return 0
    s = sorted(xs)
    k = (len(s) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(s) - 1)
    if f == c:
        return s[f]
    return s[f] * (c - k) + s[c] * (k - f)

def min_max(xs):
    if not xs:
        return [None, None]
    return [min(xs), max(xs)]
