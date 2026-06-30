from rich.console import Console

GREETIING_TITLE = "Bem Vindo ao [bold blue]Quiz PythonGPT![/bold blue]"

def show_greeting(): 
  console = Console()
  console.clear()
  console.print(GREETIING_TITLE)


def main():
  show_greeting()


main()