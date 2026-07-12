import csv
import json
from datetime import datetime
from pathlib import Path


REPORT_FIELDS = [
    "name",
    "version",
    "publisher",
    "install_date",
    "install_location",
    "uninstall_string",
]


def save_reports(programs, output_dir, report_format, summary):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = output_dir / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    base_name = f"software_inventory_{timestamp}"

    formats = ["txt", "csv", "json"] if report_format == "all" else [report_format]
    saved_files = []

    for current_format in formats:
        if current_format == "txt":
            saved_files.append(save_txt(programs, run_dir / f"{base_name}.txt", summary))
        elif current_format == "csv":
            saved_files.append(save_csv(programs, run_dir / f"{base_name}.csv"))
        elif current_format == "json":
            saved_files.append(save_json(programs, run_dir / f"{base_name}.json", summary))

    return saved_files, run_dir, base_name


def save_txt(programs, file_path, summary):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("SOFTWARE INVENTORY REPORT\n")
        file.write("=========================\n")
        file.write(f"Generated: {datetime.now()}\n")
        file.write(f"Programs found: {len(programs)}\n\n")
        file.write("SUMMARY\n")
        file.write("-------\n")
        file.write(f"Programs before filters: {summary['total_before_filters']}\n")
        file.write(f"Unique publishers: {summary['publisher_count']}\n")
        file.write(f"Programs without version: {summary['missing_version_count']}\n")
        file.write(f"Programs without publisher: {summary['missing_publisher_count']}\n")
        file.write(f"Running as administrator: {format_bool(summary['system']['is_admin'])}\n")
        file.write(
            "System: "
            f"{summary['system']['system']} "
            f"{summary['system']['release']} "
            f"({summary['system']['machine']})\n\n"
        )

        file.write("FILTERS\n")
        file.write("-------\n")
        if summary["filters"]["active"]:
            file.write(f"Name contains: {summary['filters']['search'] or '-'}\n")
            file.write(f"Publisher contains: {summary['filters']['publisher'] or '-'}\n")
            file.write(
                "Missing version only: "
                f"{format_bool(summary['filters']['missing_version_only'])}\n\n"
            )
        else:
            file.write("No active filters\n\n")

        file.write("TOP PUBLISHERS\n")
        file.write("--------------\n")
        if summary["top_publishers"]:
            for item in summary["top_publishers"]:
                file.write(f"- {item['publisher']}: {item['count']}\n")
        else:
            file.write("- No publisher data\n")

        file.write("\nPROGRAMS\n")
        file.write("--------\n")

        for index, program in enumerate(programs, start=1):
            file.write(f"{index}. {program['name']}\n")
            file.write(f"   Version: {program['version'] or '-'}\n")
            file.write(f"   Publisher: {program['publisher'] or '-'}\n")
            file.write(f"   Install date: {program['install_date'] or '-'}\n")
            file.write(f"   Install location: {program['install_location'] or '-'}\n")
            file.write(f"   Uninstall string: {program['uninstall_string'] or '-'}\n\n")

    return file_path


def save_csv(programs, file_path):
    with open(file_path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=REPORT_FIELDS)
        writer.writeheader()
        writer.writerows(programs)

    return file_path


def save_json(programs, file_path, summary):
    report_data = {
        "summary": summary,
        "programs": programs,
    }

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report_data, file, ensure_ascii=False, indent=2)

    return file_path


def format_bool(value):
    return "yes" if value else "no"
