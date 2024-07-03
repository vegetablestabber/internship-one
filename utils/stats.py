score_categorisers = {
    "s = -1": lambda arr: arr[arr == -1],
    "s = 0": lambda arr: arr[arr == 0],
    "0 < s < 1": lambda arr: arr[(arr > 0) & (arr < 1)],
    "s = 1": lambda arr: arr[arr == 1]
}

SCORE_CATEGORIES = score_categorisers.keys()

classify_scores = lambda f, lst: {c: [f(m, arr) for arr in lst] for c, m in score_categorisers.items()}

get_count = lambda m, arr: len(m(arr))

get_percent = lambda m, arr: len(m(arr)) / len(arr)