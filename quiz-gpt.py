from typing import Any


import json
from rich.console import Console
from rich.prompt import Prompt


console = Console()
GREETIING_TITLE = "Bem Vindo ao [bold blue]Quiz PythonGPT![/bold blue]"
PRESS_ENTER_MESSAGE = "Pressione ENTER para continuar..."
MOCK_QUEST = {
  "text": "Você gosta de python?",
  "choices": [
    "Sim",
    "Não",
  ],
  "answer": "Sim"
}


def show_greeting(): 
  console.clear()
  console.print(GREETIING_TITLE)


def press_enter_to_continue():
  console.input(
    prompt=PRESS_ENTER_MESSAGE,
    password=True
  )


def create_question(topic):
    quest = json.dumps(MOCK_QUEST)
    return json.loads(quest)


def validate_answer(user_points, user_answer, answer):
  if user_answer == answer:
      user_points += 1
      console.print("[bold green]Parabéns! Você acertou![/bold green]")
      console.print(f"[bold yellow] Você tem {user_points} pontos![/bold yellow]")
      return user_points
  else:
      console.print("[bold red]Que pena! Você errou![/bold red]")
      console.print(f"A resposta certa é: [bold yellow]{answer}![/bold yellow]")


def generate_quiz():
  user_points = 0
  user_answer = ""
  user_topic = Prompt.ask("Qual tópico você gostaria de estudar hoje?")

  while user_answer != "Não":
    question_created = create_question(user_topic)
    choices_created = question_created['choices']
    answer_created = question_created['answer']

    valid_choices = [str(i + 1) for i in range(len(choices_created))]

    console.print(f"[bold green]{question_created['text']}[/bold green]")

    for i, choice in enumerate(choices_created):
      console.print(f"{i + 1}. {choice}") 

    user_answer_index = int(Prompt.ask(prompt="Qual é a sua resposta?", choices=valid_choices)) -1
    user_answer = choices_created[user_answer_index]

    console.clear()
    validate_answer(user_points,user_answer,answer_created)

    user_answer = Prompt.ask(
      prompt="Deseja continuar jogando?",
      choices=["Sim", "Não"],
      default="Sim"
    )

  console.print(user_topic)

def main():
  show_greeting()
  press_enter_to_continue()
  generate_quiz()


main()