import tkinter as tk
from tkinter import ttk
from inventory.scanner import scan_installed_programs
from inventory.gui import state
print("IMPORT SCANNER OK")

def run_scan_gui(status_label):

    status_label.config(
        text="Status: Skanowanie..."
    )

    status_label.update()

    state.programs = scan_installed_programs()

    status_label.config(
        text=f"Status: Znaleziono programów: {len(state.programs)}"
    )


def refresh_program_table(table):

    for item in table.get_children():
        table.delete(item)

    for program in state.programs:
        table.insert(
            "",
            "end",
            values=(
                program["name"],
                program["version"],
                program["publisher"],
            )
        )


def create_window():

    window = tk.Tk()

    window.title("Software Scanner")
    window.geometry("700x500")


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


    reports_button = tk.Button(
        button_frame,
        text="Raporty",
        width=25,
        height=2
    )

    reports_button.pack(pady=10)


    database_button = tk.Button(
        button_frame,
        text="Baza danych",
        width=25,
        height=2
    )

    database_button.pack(pady=10)


    # ===== PROGRAM TABLE =====

    columns = (
        "name",
        "version",
        "publisher"
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

    program_table.heading(
        "name",
        text="Program"
    )

    program_table.heading(
        "version",
        text="Version"
    )

    program_table.heading(
        "publisher",
        text="Publisher"
    )


    program_table.column(
        "name",
        width=250
    )

    program_table.column(
        "version",
        width=100
    )

    program_table.column(
        "publisher",
        width=200
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