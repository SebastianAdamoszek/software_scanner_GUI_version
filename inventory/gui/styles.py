import tkinter as tk
from tkinter import ttk


def setup_style():

    style = ttk.Style()

    style.configure(
        "TButton",
        font=("Arial", 11),
        padding=8
    )

    style.configure(
        "Treeview",
        font=("Arial", 10),
        rowheight=28
    )

    style.configure(
        "Treeview.Heading",
        font=("Arial", 11, "bold")
    )


def setup_button(button):

    normal_color = "#eeeeee"
    hover_color = "#d0e8ff"

    button.config(
        cursor="hand2",
        bg=normal_color,
        activebackground=hover_color
    )

    button.bind(
        "<Enter>",
        lambda e: button.config(
            bg=hover_color
        )
    )

    button.bind(
        "<Leave>",
        lambda e: button.config(
            bg=normal_color
        )
    )


def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )