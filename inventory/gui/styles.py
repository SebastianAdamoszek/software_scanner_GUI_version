import tkinter as tk
from tkinter import ttk




def setup_style():

    style = ttk.Style()

    style.theme_use("clam")

    style.configure(
        "Main.TButton",
        font=("Segoe UI", 11),
        padding=(10, 8)
    )

    style.map(
        "Main.TButton",
        relief=[
            ("pressed", "sunken"),
            ("active", "raised")
        ],
        background=[
            ("active", "#cccccc")
        ]
    )


def setup_button(button):

    button.config(
        cursor="hand2"
    )

    button.bind(
        "<Enter>",
        lambda e: button.configure(
            cursor="hand2"
        )
    )

    button.bind(
        "<Leave>",
        lambda e: button.configure(
            cursor="arrow"
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
