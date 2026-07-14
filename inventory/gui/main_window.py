import os
from pathlib import Path

import tkinter as tk
from tkinter import ttk

from inventory.database import create_tables, save_programs
from inventory.gui import state
from inventory.reports import save_reports
from inventory.scanner import scan_installed_programs
from inventory.summary import build_summary
from inventory.system_info import get_system_info

def run_scan_gui(status_label):

    status_label.config(
        text="Status: Skanowanie..."
    )

    status_label.update()

    state.programs = scan_installed_programs()

    if not state.programs:
        status_label.config(
            text="Status: Nie znaleziono programów"
        )
        return


    system_info = get_system_info()


    summary = build_summary(
        state.programs,
        system_info,
        filter_info={
            "active": False,
            "search": "",
            "publisher": "",
            "missing_version_only": False,
        },
        total_before_filters=len(state.programs),
    )


    saved_files, report_dir, database_path = save_reports(
        state.programs,
        Path("reports"),
        "all",
        summary,
    )

    print(report_dir)
    print(database_path)

    create_tables(database_path)

    save_programs(
        state.programs,
        database_path,
    )


    status_label.config(
        text=f"Status: Zapisano raport ({len(state.programs)} programów)"
    )


def refresh_program_table(table):

    for item in table.get_children():
        table.delete(item)

    # for program in state.programs:
    #     table.insert(
    #         "",
    #         "end",
    #         values=(
    #             program["name"],
    #             program["version"],
    #             program["publisher"],
    #             program["install_date"],
    #         )
    #     )
    fill_table(
    table,
    state.programs
)

def open_reports_folder():

    reports_path = Path("reports")

    if reports_path.exists():
        os.startfile(reports_path)


def sort_column(tree, col, reverse):
    data = [
        (tree.set(item, col), item)
        for item in tree.get_children("")
    ]

    data.sort(
        reverse=reverse
    )

    for index, (_, item) in enumerate(data):
        tree.move(item, "", index)

    tree.heading(
        col,
        command=lambda: sort_column(
            tree,
            col,
            not reverse
        )
    )


def fill_table(table, programs):
    for item in table.get_children():
        table.delete(item)

    for program in programs:
        table.insert(
            "",
            "end",
            values=(
                program["name"],
                program["version"],
                program["publisher"],
                program["install_date"],
            )
        )


def search_programs(search_var, table):

    text = search_var.get().lower()

    if not text:
        fill_table(
            table,
            state.programs
        )
        return


    filtered = [
        program
        for program in state.programs
        if text in program["name"].lower()
    ]


    fill_table(
        table,
        filtered
    )


def create_window():

    window = tk.Tk()

    window.title("Software Scanner")
    window.geometry("800x900")


    # ===== HEADER =====

    title = tk.Label(
        window,
        text="Software Scanner",
        font=("Arial", 24, "bold")
    )

    title.pack(pady=30)


    subtitle = tk.Label(
        window,
        text="System inventory tool",
        font=("Arial", 12)
    )

    subtitle.pack()


    # ===== BUTTONS =====

    button_frame = tk.Frame(window)

    button_frame.pack(pady=40)


    scan_button = tk.Button(
    button_frame,
    text="Skanuj komputer",
    width=25,
    height=2,
    command=lambda:(
        run_scan_gui(status),
        refresh_program_table(program_table)
    )
)

    scan_button.pack(pady=10)

    database_button = tk.Button(
        button_frame,
        text="Baza danych",
        width=25,
        height=2
    )

    database_button.pack(pady=10)

    reports_button = tk.Button(
        button_frame,
        text="Otwórz katalog raportów",
        width=25,
        height=2,
        command=open_reports_folder
)

    reports_button.pack(pady=10)



        # ===== SEARCH =====

    search_frame = ttk.Frame(window)

    search_frame.pack(
        padx=20,
        pady=10,
        fill="x"
    )


    search_var = tk.StringVar()

    search_var.trace_add(
        "write",
        lambda *args: search_programs(
                search_var,
                program_table
        )
    )


    search_label = ttk.Label(
        search_frame,
        text="Szukaj:"
    )

    search_label.pack(
        side="left",
        padx=5
    )


    search_entry = ttk.Entry(
        search_frame,
        textvariable=search_var,
        width=40
    )

    search_entry.pack(
        side="left",
        padx=5
    )


    # ===== PROGRAM TABLE =====

    columns = (
        "name",
        "version",
        "publisher",
        "install_date"
    )

    program_table = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=10
    )

    scrollbar = ttk.Scrollbar(
    window,
    orient="vertical",
    command=program_table.yview
    )

    program_table.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    headers = {
        "name": "Program",
        "version": "Version",
        "publisher": "Publisher",
        "install_date": "Install Date",
    }

    for column, title in headers.items():
        program_table.heading(
            column,
            text=title,
            command=lambda col=column: sort_column(
                program_table,
                col,
                False
        )
    )


    widths = {
        "name": 250,
        "version": 100,
        "publisher": 200,
        "install_date": 120,
    }

    for column, width in widths.items():
        program_table.column(
            column,
            width=width
    )

    program_table.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )




    # ===== STATUS =====

    status = tk.Label(
        window,
        text="Status: Gotowy",
        anchor="w"
    )

    status.pack(
        side="bottom",
        fill="x",
        padx=20,
        pady=20
    )


    window.mainloop()


if __name__ == "__main__":
    start_gui()