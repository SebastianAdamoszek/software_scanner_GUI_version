from collections import Counter


def build_summary(programs, system_info, filter_info=None, total_before_filters=None):
    publishers = [program["publisher"] for program in programs if program["publisher"]]
    missing_versions = [program for program in programs if not program["version"]]
    missing_publishers = [program for program in programs if not program["publisher"]]

    top_publishers = [
        {"publisher": publisher, "count": count}
        for publisher, count in Counter(publishers).most_common(10)
    ]

    return {
        "program_count": len(programs),
        "total_before_filters": total_before_filters if total_before_filters is not None else len(programs),
        "publisher_count": len(set(publishers)),
        "missing_version_count": len(missing_versions),
        "missing_publisher_count": len(missing_publishers),
        "top_publishers": top_publishers,
        "filters": filter_info or {
            "search": "",
            "publisher": "",
            "missing_version_only": False,
            "active": False,
        },
        "system": system_info,
    }
