from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live



console = Console(
    force_terminal=True,
    color_system="truecolor"
)


PAGE_SIZE = 30


# =========================
# VERSION
# =========================

def show_version():

    table = Table(
        title="INFORMACJA",
        border_style="cyan"
    )

    table.add_column("Program")
    table.add_column("Wersja")

    table.add_row(
        "Software Scanner CLI + SQLite",
        "1.1"
    )

    console.print(table)


# =========================
# MENU
# =========================

def show_menu(search, publisher, missing):

    status = f"""
Filtry aktywne:

• nazwa: {search or '-'}
• producent: {publisher or '-'}
• brak wersji: {'TAK' if missing else 'NIE'}
"""


    console.print(
        Panel(
            status,
            title="STATUS",
            border_style="yellow"
        )
    )


    table = Table(
        title="MENU",
        border_style="cyan",
        row_styles=["", "on grey11"],
        show_lines=False
    )


    table.add_column(
        "Opcja",
        width=6,
        justify="center"
    )

    table.add_column(
        "Akcja"
    )


    table.add_row("[cyan]1[/cyan]", "Skanuj system")
    table.add_row("[cyan]2[/cyan]", "Filtruj wg nazwy")
    table.add_row("[cyan]3[/cyan]", "Filtruj wg producenta")

    table.add_row(
        "[cyan]4[/cyan]",
        f"Pokaż tylko programy bez wersji: {'TAK' if missing else 'NIE'}"
    )

    table.add_row(
        "[yellow]5[/yellow]",
        "Resetuj filtry"
    )

    table.add_row(
        "[red]6[/red]",
        "Wyjście"
    )


    console.print(table)


    console.print(
        "\n[grey62]Wpisz numer opcji i Enter[/grey62]"
    )



# =========================
# HEADER
# =========================

def show_header():

    console.print(
        Panel.fit(
            "[bold cyan]SOFTWARE INVENTORY SCANNER[/bold cyan]\n"
            "[grey62]Skaner zainstalowanego oprogramowania Windows[/grey62]",
            border_style="cyan"
        )
    )



# =========================
# SYSTEM
# =========================

def show_system_status(system_info):

    table = Table.grid(
        padding=(0, 2)
    )


    table.add_column(
        style="bold"
    )

    table.add_column()


    table.add_row(
        "Administrator",
        format_bool_pl(
            system_info.get("is_admin", False)
        )
    )


    table.add_row(
        "System",
        f"{system_info.get('system','N/A')} "
        f"{system_info.get('release','')} "
        f"({system_info.get('machine','')})"
    )


    console.print(
        Panel(
            table,
            title="System",
            border_style="green"
            if system_info.get("is_admin")
            else "yellow"
        )
    )



# =========================
# SCAN
# =========================

def show_scan_start():

    console.print(
        "[cyan]Skanowanie zainstalowanych programów...[/cyan]"
    )



def show_no_programs_found():

    console.print(
        "[red]Nie znaleziono programów.[/red]"
    )



def show_no_filter_results(total_before_filters):

    table = Table(
        title="BRAK WYNIKÓW",
        border_style="cyan"
    )

    table.add_column(
        "Informacja",
        style="yellow"
    )


    table.add_row(
        "Nie znaleziono programów spełniających filtr."
    )

    table.add_row(
        f"Liczba programów przed filtrem: {total_before_filters}"
    )


    console.print(table)



# =========================
# TABLE PROGRAMS
# =========================

def show_programs_table(programs, start_numbers=1):


    table = Table(
        title="ZAINSTALOWANE PROGRAMY",
        border_style="cyan",
        show_lines=False,
        row_styles=["", "grey62"]
    )


    table.add_column(
        "LP",
        width=4,
        justify="right"
    )


    table.add_column(
        "Program",
        min_width=35,
        overflow="fold"
    )


    table.add_column(
        "Wersja",
        width=18
    )


    table.add_column(
        "Producent",
        min_width=25,
        overflow="fold"
    )


    for i, program in enumerate(
        programs,
        start_numbers
    ):

        table.add_row(
            str(i),
            program.get("name", "-"),
            program.get("version") or "-",
            program.get("publisher") or "-"
        )


    console.print(table)



# =========================
# PROGRAM BROWSER
# =========================

def browse_programs(programs):

    if not programs:
        console.print("[yellow]Brak programów.[/yellow]")
        return


    page = 0

    total_pages = (
        len(programs) + PAGE_SIZE - 1
    ) // PAGE_SIZE


    while True:

        start = page * PAGE_SIZE
        end = start + PAGE_SIZE


        show_programs_table(
            programs[start:end],
            start_numbers=start + 1
        )


        console.print(
            f"\nStrona {page + 1}/{total_pages}"
            f" | Programy {start + 1}-"
            f"{min(end, len(programs))}"
            f" z {len(programs)}"
        )


        # =====================
        # NAWIGACJA
        # =====================

        if total_pages == 1:

            console.print(
                "[cyan][Q][/cyan] Powrót"
            )


        elif page == 0:

            console.print(
                "[cyan][N][/cyan] Następna   "
                "[cyan][Q][/cyan] Powrót"
            )


        elif page == total_pages - 1:

            console.print(
                "[cyan][P][/cyan] Poprzednia   "
                "[cyan][Q][/cyan] Powrót"
            )


        else:

            console.print(
                "[cyan][N][/cyan] Następna   "
                "[cyan][P][/cyan] Poprzednia   "
                "[cyan][Q][/cyan] Powrót"
            )



        choice = input("> ").strip().lower()



        if choice == "n":

            if page < total_pages - 1:
                page += 1



        elif choice == "p":

            if page > 0:
                page -= 1



        elif choice == "q":
            console.print("\n" * 10)
            break



# =========================
# SUMMARY
# =========================

def show_summary(summary):

    table = Table(
        title="Podsumowanie",
        border_style="cyan"
    )


    table.add_column(
        "Metryka"
    )


    table.add_column(
        "Wartość",
        justify="right"
    )


    for key, value in [
        ("Programy", summary.get("program_count",0)),
        ("Przed filtrem", summary.get("total_before_filters",0)),
        ("Producenci", summary.get("publisher_count",0)),
        ("Bez wersji", summary.get("missing_version_count",0)),
        ("Bez producenta", summary.get("missing_publisher_count",0))
    ]:

        table.add_row(
            key,
            str(value)
        )


    console.print(table)



# =========================
# FILTERS
# =========================

def show_filters(filter_info):

    if not filter_info.get("active"):

        console.print(
            "[grey62]Brak aktywnych filtrów[/grey62]"
        )

        return


    table = Table(
        title="Filtry",
        border_style="magenta"
    )


    table.add_column("Filtr")
    table.add_column("Wartość")


    if filter_info.get("search"):

        table.add_row(
            "Nazwa",
            filter_info["search"]
        )


    if filter_info.get("publisher"):

        table.add_row(
            "Producent",
            filter_info["publisher"]
        )


    if filter_info.get("missing_version_only"):

        table.add_row(
            "Bez wersji",
            "TAK"
        )


    console.print(table)



# =========================
# PRODUCERS
# =========================

def show_top_publishers(summary, limit=30):

    top = summary.get(
        "top_publishers",
        []
    )


    table = Table(
        title="LISTA PRODUCENTÓW",
        border_style="green"
    )


    table.add_column("Producent")
    table.add_column("Ilość")


    for item in top[:limit]:

        table.add_row(
            str(item.get("publisher","-")),
            str(item.get("count",0))
        )


    console.print(table)



# =========================
# FILES
# =========================

def show_saved_files(files):
    files = sorted(files, key=lambda file: file.name)

    table = Table(
        title="Zapisane raporty",
        border_style="blue"
    )


    table.add_column("Plik")


    for file in files:

        table.add_row(
            str(file)
        )


    console.print(table)



# =========================
# SUCCESS
# =========================

def show_success():

    console.print(
        "[bold green]Gotowe.[/bold green]"
    )



# =========================
# UTIL
# =========================

def format_bool_pl(value):

    return (
        "[green]TAK[/green]"
        if value
        else "[yellow]NIE[/yellow]"
    )