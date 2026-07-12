import argparse
from pathlib import Path

from inventory.console_ui import (
    browse_programs,
    show_header,
    show_menu,
    show_scan_start,
    show_no_programs_found,
    show_no_filter_results,
    show_programs_table,
    show_summary,
    show_system_status,
    show_top_publishers,
    show_saved_files,
    show_filters,
    show_success,
    show_version,
)

from inventory.filters import apply_filters, build_filter_info
from inventory.logger_setup import setup_logging
from inventory.reports import save_reports
from inventory.scanner import scan_installed_programs
from inventory.summary import build_summary
from inventory.system_info import get_system_info
from inventory.database import save_programs, create_tables

DEFAULT_OUTPUT_DIR = "reports"


# =========================
# ARG PARSER
# =========================
def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--output", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--format", choices=["txt", "csv", "json", "all"], default="all")
    parser.add_argument("--timeout", type=int, default=30)

    parser.add_argument("--search", default="")
    parser.add_argument("--publisher", default="")
    parser.add_argument("--missing-version-only", action="store_true")

    parser.add_argument("--menu", action="store_true")

    return parser.parse_args()


# =========================
# CORE SCAN
# =========================
def run_scan(args):
    setup_logging()
    show_header()
    show_scan_start()

    system_info = get_system_info()
    show_system_status(system_info)

    programs = scan_installed_programs(timeout=args.timeout)

    if not programs:
        show_no_programs_found()
        return


    total_before = len(programs)

    filter_info = build_filter_info(
        search=args.search,
        publisher=args.publisher,
        missing_version_only=args.missing_version_only,
    )

    programs = apply_filters(
        programs,
        search=args.search,
        publisher=args.publisher,
        missing_version_only=args.missing_version_only,
    )

    if not programs:
        show_no_filter_results(total_before)
        return

    output_dir = Path(args.output)

    summary = build_summary(
        programs,
        system_info,
        filter_info=filter_info,
        total_before_filters=total_before,
    )

    saved_files, report_dir, base_name = save_reports(
        programs,
        output_dir,
        args.format,
        summary,
    )

    database_path = report_dir / f"{base_name}.db"
    
    create_tables(database_path)

    save_programs(programs, database_path)

    saved_files.append(database_path)

    # =========================
    # OUTPUT (RICH)
    # =========================
    show_summary(summary)
    show_top_publishers(summary)
    show_filters(summary["filters"])
    show_saved_files(saved_files)
    browse_programs(programs)
    show_success()


# =========================
# MENU MODE
# =========================
def menu():
    search = ""
    publisher = ""
    missing = False

    while True:
        show_menu(search, publisher, missing)

        choice = input("\n👉 Wybierz opcję (1-6): ").strip()

        # =========================
        # SCAN
        # =========================
        if choice in ["", "1"]:
            print("\n[INFO] Uruchamianie skanowania systemu...\n")

            args = build_args(search, publisher, missing)
            run_scan(args)

            input("\n✔ Skan zakończony. Naciśnij ENTER aby wrócić do menu...")
            

        # =========================
        # SEARCH FILTER
        # =========================
        elif choice == "2":
            search = input("🔎 Wpisz nazwę programu (np. chrome, python): ").strip()
            print(f"[OK] Filtr ustawiony: nazwa = '{search or '-'}'")

        # =========================
        # PUBLISHER FILTER
        # =========================
        elif choice == "3":
            publisher = input("🏢 Wpisz producenta (np. Microsoft): ").strip()
            print(f"[OK] Filtr ustawiony: producent = '{publisher or '-'}'")

        # =========================
        # MISSING VERSION
        # =========================
        elif choice == "4":
            missing = not missing
            state = "AKTYWNY" if missing else "WYŁĄCZONY"
            print(f"[OK] Filtr 'brak wersji' → {state}")

        # =========================
        # RESET
        # =========================
        elif choice == "5":
            search = ""
            publisher = ""
            missing = False
            print("\n[RESET] Wszystkie filtry zostały wyczyszczone.")

        # =========================
        # EXIT
        # =========================
        elif choice == "6":
            print("\n[EXIT] Zamykanie programu...")
            break

        # =========================
        # INVALID INPUT
        # =========================
        else:
            print("\n[ERROR] Nieprawidłowa opcja. Wybierz 1-6.")


# =========================
# ARGS BUILDER
# =========================
def build_args(search, publisher, missing):
    class Args:
        pass

    args = Args()
    args.output = DEFAULT_OUTPUT_DIR
    args.format = "all"
    args.timeout = 30

    args.search = search
    args.publisher = publisher
    args.missing_version_only = missing

    return args


# =========================
# START
# =========================
if __name__ == "__main__":

    args = parse_args()

    show_version()

    menu()