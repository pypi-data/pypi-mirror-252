from datetime import datetime, date, timedelta


def _filter_range(range: dict[str, date], days: list[int]) -> list[dict[str, date]]:
    if days == [0, 1, 2, 3, 4, 5, 6]:
        return [range]
    result = list()
    current_date = range["start"]
    range_start = None
    range_end = None
    while current_date <= range["end"]:
        if current_date.weekday() in days:
            if not range_start:
                range_start = current_date
            range_end = current_date
            if current_date == range["end"]:
                result.append({"start": range_start, "end": range_end})
        else:
            if range_start:
                result.append({"start": range_start, "end": range_end})
                range_start = None
                range_end = None
        current_date += timedelta(days=1)
    return result


def filter(base: list[dict[str, date]], days: list[int]) -> list[dict[str, date]]:
    """Filter ranges by keeping only the days of week in <days>"""
    if days == [0, 1, 2, 3, 4, 5, 6]:
        return base
    result = list()
    for range in consolidate(ranges=base):
        result.extend(_filter_range(range=range, days=days))
    return result


def _inner_join_range(
    left: dict[str, date], right: dict[str, date]
) -> list[dict[str, date]]:
    # No overlap
    if left["end"] < right["start"] or right["end"] < left["start"]:
        return []
    # Partial or complete overlap
    return [
        {
            "start": max(right["start"], left["start"]),
            "end": min(right["end"], left["end"]),
        }
    ]


def inner_join(
    left: list[dict[str, date]],
    right: list[dict[str, date]],
    left_days: list[int] = [0, 1, 2, 3, 4, 5, 6],
    right_days: list[int] = [0, 1, 2, 3, 4, 5, 6],
) -> list[dict[str, date]]:
    right = consolidate(right)
    left = consolidate(left)
    if left_days != right_days:
        days = [k for k in left_days if k in right_days]
        right = filter(base=right, days=days)
        left = filter(base=left, days=days)
    result = []
    for r in right:
        for l in left:
            result.extend(_inner_join_range(right=r, left=l))
    return result


def _left_outer_join_range(
    left: dict[str, date], right: dict[str, date]
) -> list[dict[str, date]]:
    # No overlap
    if left["end"] < right["start"] or right["end"] < left["start"]:
        return [left]

    # right encapsulates left
    if right["start"] <= left["start"] and left["end"] < right["end"]:
        return []

    # left encapsulates right or overlap
    result = []
    if left["start"] < right["start"]:
        result.append(
            {"start": left["start"], "end": right["start"] - timedelta(days=1)}
        )
    if right["end"] < left["end"]:
        result.append({"start": right["end"] + timedelta(days=1), "end": left["end"]})
    return result


def left_outer_join(
    left: list[dict[str, date]],
    right: list[dict[str, date]],
    left_days: list[int] = [0, 1, 2, 3, 4, 5, 6],
    right_days: list[int] = [0, 1, 2, 3, 4, 5, 6],
) -> list[dict[str, date]]:
    if left_days != right_days:
        right = filter(base=right, days=right_days)
    result = left
    for r in right:
        tmp_result = []
        for l in result:
            tmp_result.extend(_left_outer_join_range(left=l, right=r))
        result = tmp_result
    return filter(base=result, days=left_days)


def subtract(
    base: list[dict[str, date]],
    exclusion: list[dict[str, date]],
) -> list[dict[str, date]]:
    return left_outer_join(left=base, right=exclusion)


def shrink(base: dict[str, date], exclusion: dict[str, date]) -> list[dict[str, date]]:
    """Shrink base date range and return a list of date ranges in <base> but not
    in <exclusion> date range"""
    return _left_outer_join_range(left=base, right=exclusion)


def expand(base: dict[str, date], expansion: dict[str, date]) -> dict[str, date]:
    """Expand and returns new <base> date range if it overlaps or touches the
    <expansion> date range"""
    b = base
    e = expansion
    if (
        b["end"] + timedelta(days=1) < e["start"]
        or e["end"] + timedelta(days=1) < b["start"]
    ):
        # no overlap and no touching, return empty
        return {}
    # Overlap or touching guaranteed:
    return {"start": min(b["start"], e["start"]), "end": max(b["end"], e["end"])}


def consolidate(ranges: list[dict[str, date]]) -> list[dict[str, date]]:
    """Consolidate date ranges to elimiate any overlapping and/or touching
    date ranges"""
    if not ranges:
        return []
    result = []
    remaining_ranges = []
    base = ranges[0]
    for range in ranges[1:]:
        if expanded_range := expand(base, range):
            base = expanded_range
        else:
            remaining_ranges.append(range)
    result.append(base)
    result.extend(consolidate(remaining_ranges))
    return result


def _convert_str_to_date(data: str | date) -> date:
    if not isinstance(data, date):
        data = datetime.strptime(data, "%Y-%m-%d").date()
    return data


def _clean_range(range: dict[str, str | date]) -> dict[str, date]:
    keys = ["start", "end"]
    result = {}
    for k in keys:
        if k not in range:
            raise ValueError(f"mising key {k} in {range}")
        result[k] = _convert_str_to_date(range[k])
    return result


def clean(ranges: list[dict[str, str | date]]) -> list[dict[str, date]]:
    """Keep only the 'start' and 'end' keys and convert values to type
    datetime.date"""
    result = []
    for range in ranges:
        result.append(_clean_range(range))
    return result
