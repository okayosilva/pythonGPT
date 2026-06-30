from rich.console import Console
from rich.prompt import Prompt


console = Console()
GREETIING_TITLE = "Bem Vindo ao [bold blue]Quiz PythonGPT![/bold blue]"
PRESS_ENTER_MESSAGE = "Pressione ENTER para continuar..."

def show_greeting(): 
  console.clear()
  console.print(GREETIING_TITLE)


def press_enter_to_continue():
  console.input(
    prompt=PRESS_ENTER_MESSAGE,
    password=True
  )


def create_questions(topic):
  pass


def generate_quiz():
  user_points = 0
  user_response = ""
  user_topic = Prompt.ask("Qual tópico você gostaria de estudar hoje?")

  while user_response != "Não":
    question_created = create_questions(user_topic)

    user_response = Prompt.ask(
      prompt="Deseja continuar jogando?",
      choices=["Sim", "Não"],
    )

  console.print(user_topic)

def main():
  show_greeting()
  press_enter_to_continue()
  generate_quiz()


main()