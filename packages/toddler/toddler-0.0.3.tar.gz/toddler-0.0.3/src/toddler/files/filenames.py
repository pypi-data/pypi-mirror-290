import re
import numpy as np


def parse_integers(string, *patterns) -> tuple[int, ...]:
    results = []
    for pattern in patterns:
        match = re.search(pattern, string)
        if match:
            results.append(int(match.group(1)))

    if len(results) == 1:
        return results[0]
    if len(results) == 0:
        return ()

    return results


def sorted_glob(folder, pattern, sortby, *patterns):
    sort_pattern = re.compile(patterns[sortby])
    return sorted(
        glob(folder, pattern, *patterns),
        key=lambda x: parse_integers(x[0].stem, sort_pattern),
    )


def glob(folder, pattern, *patterns):
    for file in folder.glob(pattern):
        yield file, parse_integers(file.stem, *patterns)


def unique_values(folder, pattern, filter="*.*"):
    files = list(folder.glob(filter))
    pattern = re.compile(pattern)
    vals = np.zeros((len(files),), dtype=int)

    for i, f in enumerate(files):
        vals[i] = re.findall(pattern, f.stem)[0]

    return np.unique(vals)
