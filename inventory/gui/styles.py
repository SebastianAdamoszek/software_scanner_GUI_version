import tkinter as tk
from tkinter import ttk

SETUP_BUTTON = {
    "style": "Main.TButton",
    "cursor": "hand2",
    "width": 30 
    }


def setup_style():

    style = ttk.Style()

    style.theme_use("clam")

    style.configure(
        "Main.TButton",
        background="#acacac",
        foreground="black",
        font=("Segoe UI", 11),
        padding=(15, 8),
    )

    style.map(
        "Main.TButton",
        background=[
            ("pressed", "#9da0a3"),
            ("active", "gray")
        ],
    )


def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )
