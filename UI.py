import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.style import Style

logger = logging.getLogger("chuvaviva")
logger.setLevel(logging.INFO)
_handler = logging.FileHandler("chuvaviva.log", encoding="utf-8")
_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(_handler)

console = Console()

PALETA = {
    "borda": "blue",
    "titulo": "bold cyan",
    "destaque": "bold yellow",
    "erro": "red"
}

def render_header(titulo):
    console.print(Panel(
        f"[white]{titulo.upper()}[/white]",
        style=PALETA["titulo"],
        border_style=PALETA["borda"]
    ))

def criar_painel(conteudo, titulo, estilo="blue"):
    console.print(Panel(
        conteudo,
        title=f"[bold]{titulo}[/bold]",
        border_style=estilo,
        padding=(1, 2)
    ))