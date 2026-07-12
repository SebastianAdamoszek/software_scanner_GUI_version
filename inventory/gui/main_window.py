import tkinter as tk


def create_window():
    window = tk.Tk()

    window.title("Software Scanner")
    window.geometry("600x400")

    title = tk.Label(
        window,
        text="Software Scanner",
        font=("Arial", 20)
    )

    title.pack(pady=30)


    scan_button = tk.Button(
        window,
        text="Skanuj komputer",
        width=25,
        height=2
    )

    scan_button.pack(pady=10)


    reports_button = tk.Button(
        window,
        text="Raporty",
        width=25,
        height=2
    )

    reports_button.pack(pady=10)


    exit_button = tk.Button(
        window,
        text="Zamknij",
        width=25,
        height=2,
        command=window.destroy
    )

    exit_button.pack(pady=10)


    window.mainloop()


if __name__ == "__main__":
    start_gui()