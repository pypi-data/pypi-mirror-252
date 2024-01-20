from datetime import datetime, date, timedelta


def subtract(
    base: list[dict[str, date]],
    exclusion: list[dict[str, date]],
) -> list[dict[str, date]]:
    tmp_base_range_list = base
    for e in exclusion:
        new_base_range_list = []
        for b in tmp_base_range_list:
            new_base_range_list.extend(shrink(base=b, exclusion=e))
        tmp_base_range_list = consolidate(new_base_range_list)
    return tmp_base_range_list


def shrink(base: dict[str, date], exclusion: dict[str, date]) -> list[dict[str, date]]:
    """Shrink base date range and return a list of date ranges in <base> but not
    in <exclusion> date range"""
    b = base
    e = exclusion
    if e["start"] <= b["start"] and b["end"] <= e["end"]:
        # completely excluded
        return []
    if e["end"] < b["start"] or b["end"] < e["start"]:
        # no overlap at all, keep base
        return [{"start": b["start"], "end": b["end"]}]
    # Overlap guaranteed:
    result = []
    if b["start"] < e["start"]:
        # keep left
        end = e["start"] - timedelta(days=1)
        result.append({"start": b["start"], "end": end})
    if e["end"] < b["end"]:
        # keep right
        start = e["end"] + timedelta(days=1)
        result.append({"start": start, "end": b["end"]})
    return result


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


def filter(base: list[dict[str, date]], days: list[int]) -> list[dict[str, date]]:
    """Filter ranges by keeping only the days of week in <days>"""
    result = list()
    for range in consolidate(ranges=base):
        result.extend(_filter_range(range=range, days=days))
    return result


def _filter_range(range: dict[str, date], days: list[int]) -> list[dict[str, date]]:
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
