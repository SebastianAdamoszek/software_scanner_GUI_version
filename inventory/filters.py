def apply_filters(programs, search="", publisher="", missing_version_only=False):
    filtered = programs

    if search:
        search_value = search.casefold()
        filtered = [
            program
            for program in filtered
            if search_value in program["name"].casefold()
        ]

    if publisher:
        publisher_value = publisher.casefold()
        filtered = [
            program
            for program in filtered
            if publisher_value in program["publisher"].casefold()
        ]

    if missing_version_only:
        filtered = [program for program in filtered if not program["version"]]

    return filtered


def build_filter_info(search="", publisher="", missing_version_only=False):
    return {
        "search": search,
        "publisher": publisher,
        "missing_version_only": missing_version_only,
        "active": bool(search or publisher or missing_version_only),
    }
