def inclusion(data: str, super_string: str) -> bool:
    return data in super_string


def min_length(data: str, min_length: int) -> bool:
    return len(data) >= min_length


def apply_filter_pipeline(data: list[str], *fns):
    for fn in fns:
        data = list(map(fn, data))
        # NOTE: if transformation results in empty string, it is filtered out
        data = list(filter(lambda x: x, data))
    return data


def get_filter_mask(data: list[str], *fns):
    mask = [True] * len(data)
    for fn in fns:
        mask = [x and fn(data[i]) for i, x in enumerate(mask)]
      
    return mask