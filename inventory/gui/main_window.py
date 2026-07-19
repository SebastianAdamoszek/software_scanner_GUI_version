import os
from pathlib import Path

import tkinter as tk
from tkinter import ttk, filedialog

from inventory.database import create_tables, save_programs
from inventory.gui import state
from inventory.reports import save_reports
from inventory.scanner import scan_installed_programs
from inventory.summary import build_summary
from inventory.system_info import get_system_info
from inventory.gui.styles import (
    SETUP_BUTTON,
    setup_style, 
    center_window
)

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


    status_label.config(
        text=f"⏳ Tworzę raport... ({len(state.programs)} programów)",
        foreground="#1E90FF"
    )

    status_label.update()


    saved_files, report_dir, database_path = save_reports(
        state.programs,
        Path("reports"),
        "all",
        summary,
    )

    report_name = Path(saved_files[0]).stem if saved_files else "Brak raportu"

    print(report_dir)
    print(database_path)

    create_tables(database_path)

    save_programs(
        state.programs,
        database_path,
    )


    status_label.config(
        text=f"✅ Zapisano {report_name} ({len(state.programs)} programów)",
        foreground="#008000"
    )

    status_label.update()

    


def refresh_program_table(table):

    for item in table.get_children():
        table.delete(item)


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


def search_programs(search_var, table, count_label):

    text = search_var.get().lower()

    if not text:
        fill_table(
            table,
            state.programs
        )

        count_label.config(
            text=f"Wszystkie programy: {len(state.programs)}",
            font=("Segoe UI", 11, "bold"),
            foreground="#1E90FF"

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


    count_label.config(
        text=f"Znaleziono: {len(filtered)} z {len(state.programs)}",
        font=("Segoe UI", 11, "bold"),
        foreground="#008000"
    )

    if len(filtered) == 0:

        count_label.config(
            text="⚠ Nie znaleziono programu",
            font=("Segoe UI", 11, "bold"),
            foreground="#FF8C00"
        )

    else:

        count_label.config(
            text=f"Znaleziono: {len(filtered)} z {len(state.programs)}",
            font=("Segoe UI", 11, "bold"),
            foreground="#008000"
        )

import json

def load_report(table, status_label,search_var, count_label):

    filename = filedialog.askopenfilename(
        title="Wybierz plik raportu",
        initialdir=Path("reports"),
        filetypes=(
            ("Pliki JSON", "*.json"),
            # ("Wszystkie pliki", "*.*")
        )
    )

    if filename:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as files:

            data = json.load(files)


        state.programs = data["programs"]


        fill_table(
            table,
            state.programs
        )

        search_programs(
            search_var,
            table,
            count_label
        )

        report_name = Path(filename).stem


        status_label.config(
            text=f"Status: Wczytano raport- {report_name} ({len(state.programs)} programów)"
        )

        status_label.update()


        return data

    return []


def create_window():

    window = tk.Tk()

    setup_style()

    # window.configure(cursor="arrow")

    window.title("Software Scanner for windows")

    center_window(
        window, 800, 900
    )

    # ===== HEADER =====

    title = ttk.Label(
        window,
        text="Software Scanner",
        font=("Arial", 24, "bold"),
        anchor="center"
    )

    title.pack(pady=15, ipadx=20, ipady=10)


    subtitle = ttk.Label(
        window,
        text="System inventory tool",
        font=("Segoe UI", 12),
        anchor="center"
    )

    subtitle.pack(ipadx=20, ipady=10, )


    # ===== BUTTONS =====

    button_frame = ttk.Frame(window)

    button_frame.pack(pady=30)

    scan_button = ttk.Button(
        button_frame,
        text="Skanuj komputer",
        **SETUP_BUTTON,
        command=lambda: (
            run_scan_gui(status),
            refresh_program_table(program_table),
            search_programs(search_var, program_table, count_label)
        ),
    )

    scan_button.pack(padx=10,pady=10)


    load_button = ttk.Button(
        button_frame,
        text="Wczytaj raport",
        **SETUP_BUTTON,
        command=lambda: load_report(
            program_table,
            status,
            search_var,
            count_label
        ),
    )

    load_button.pack(padx=10,pady=10)


    # database_button = ttk.Button(
    #     button_frame,
    #     text="Baza danych",
    #     width=BUTTON_WIDTH,
    #     style="Main.TButton"
    # )

    # database_button.pack(padx=10,pady=10)


    reports_button = ttk.Button(
        button_frame,
        text="Katalog raportów",
        **SETUP_BUTTON,
        command=open_reports_folder,
    )

    reports_button.pack(padx=10, pady=10)



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
                program_table,
                count_label
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

    count_label = ttk.Label(
        search_frame,
        text="Filtr programów: 0",
        font=("Segoe UI", 11, "bold"),
        foreground="#1E90FF"
    )

    count_label.pack(
        side="left",
        padx=10
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

    status_frame = tk.Frame(
        window,
        bd=1,
        relief="sunken",
    )

    status_frame.pack(
        fill="x",
        padx=20,
        pady=(0,20)
    )


    status = ttk.Label(
        status_frame,
        text="✓ Gotowy",
        font=("Segoe UI", 11, "bold"),
        foreground="#006400",
        anchor="w"
    )

    status.pack(
        fill="x",
        padx=10,
        pady=10
    )


    window.mainloop()


if __name__ == "__main__":
    start_gui() # type: ignore