import json
import re
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from openai import OpenAI

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
QUESTION_GENERATOR_PROMPT = """Você é um especialista sênior com conhecimento amplo e profundo em diversas áreas (técnicas, acadêmicas, corporativas ou gerais), capaz de elaborar perguntas de avaliação sobre qualquer assunto com precisão e rigor.

Você está atuando em um processo de avaliação/seleção e precisa elaborar UMA pergunta de múltipla escolha sobre o tópico informado, para avaliar o conhecimento do candidato/participante.

## Parâmetros de entrada

- Tópico/Assunto: {topic}
- Nível de dificuldade: {dificult}

## Regras para a pergunta

1. A pergunta deve ser clara, objetiva e tecnicamente/conceitualmente precisa dentro do tópico informado.
2. Deve conter exatamente 4 alternativas (nunca mais, nunca menos).
3. Apenas UMA alternativa deve estar correta.
4. As alternativas incorretas (distratores) devem ser plausíveis e relacionadas ao tema, evitando opções absurdas ou claramente erradas — o objetivo é testar conhecimento real, não "sorte".
5. Evite ambiguidade: a pergunta não pode ter mais de uma interpretação válida.
6. A pergunta deve ter uma resposta objetivamente correta e verificável — nunca use perguntas de opinião, gosto pessoal ou subjetivas (ex: "Você gosta de X?").
7. Adapte a complexidade da pergunta ao nível de dificuldade informado:
   - **Fácil**: conceitos fundamentais, definições básicas e aplicações diretas do tópico.
   - **Médio**: compreensão intermediária, relações entre conceitos e cenários práticos comuns.
   - **Difícil**: detalhes avançados, casos de borda, nuances técnicas ou raciocínio em múltiplos passos.
   O nível solicitado é **{dificult}** — calibre a pergunta e os distratores de acordo.
8. Não inclua explicações, comentários, justificativas ou texto adicional fora do formato solicitado.

## Formato de saída obrigatório

Responda somente com um bloco de código JSON contendo um único objeto, sem nenhum texto antes ou depois, sem nome de variável:

```json
{{
  "text": "Texto da pergunta aqui",
  "choices": [
    "Alternativa 1",
    "Alternativa 2",
    "Alternativa 3",
    "Alternativa 4"
  ],
  "answer": "Texto exato da alternativa correta, igual ao que está em choices"
}}
```

## Observações importantes

- O valor de "answer" deve ser idêntico a uma das strings presentes em "choices" (cópia exata, mesma capitalização e pontuação).
- A lista "choices" deve conter sempre 4 itens, sem repetições.
- A saída deve ser um objeto JSON válido, sem atribuição de variável, apenas as chaves {{ }} e seu conteúdo.
- O conteúdo da pergunta deve se adaptar ao tópico informado, mantendo o mesmo padrão de qualidade e formato independentemente do assunto.
"""

console = Console()
load_dotenv()
agent_gpt = OpenAI().chat


def parse_question_response(content: str) -> dict:
  if not content or not content.strip():
    raise ValueError("A API não retornou conteúdo para a pergunta.")

  text = content.strip()
  if text.startswith("```"):
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

  return json.loads(text.strip())


def show_greeting(): 
  console.clear()
  console.print(GREETIING_TITLE)


def press_enter_to_continue():
  console.input(
    prompt=PRESS_ENTER_MESSAGE,
    password=True
  )


def ask_continue_playing():
  return Prompt.ask(
      prompt="Deseja continuar jogando?",
      choices=["Sim", "Não"],
      default="Sim"
    )


def create_question(topic, dificult):
    prompt = QUESTION_GENERATOR_PROMPT.format(topic=topic, dificult=dificult)
    agent_answer = agent_gpt.completions.create(
      model="gpt-4.1-nano",
      messages=[{
        "role": "system",
        "content" : prompt
      },
      {
        "role": "user",
        "content" : f"Gere uma questão de nível {dificult} sobre {topic}"
      }]
    )

    content_answer = agent_answer.choices[0].message.content
    return parse_question_response(content_answer)


def validate_answer(user_points, user_answer, answer):
  if user_answer == answer:
      user_points += 1
      console.print("[bold green]Parabéns! Você acertou![/bold green]")
      console.print(f"[bold yellow] Você tem {user_points} pontos![/bold yellow]")
      return user_points
  else:
      console.print("[bold red]Que pena! Você errou![/bold red]")
      console.print(f"A resposta certa é: [bold yellow]{answer}![/bold yellow]")

      if user_points > 0:
        user_points -= 1

      return user_points


def finish_quiz(user_points, number_of_questions):
  console.clear()

  if number_of_questions == 0:
    console.print("[dim]Você saiu sem responder nenhuma pergunta. Até a próxima![/dim]")
    return

  percentage = (user_points / number_of_questions) * 100

  if user_points == number_of_questions:
    title = "Desempenho excepcional!"
    message = "Você manteve a pontuação máxima. Domínio total do conteúdo!"
    border_style = "green"
  elif percentage >= 70:
    title = "Bom trabalho!"
    message = "Resultado sólido. Continue praticando para chegar na perfeição."
    border_style = "yellow"
  elif percentage >= 40:
    title = "Continue estudando!"
    message = "Você está no caminho certo. Revise o tópico e jogue novamente."
    border_style = "blue"
  else:
    title = "Não desista!"
    message = "Cada tentativa conta. Volte com calma e vá evoluindo aos poucos."
    border_style = "red"

  summary = (
    f"[bold]Perguntas respondidas:[/bold] {number_of_questions}\n"
    f"[bold]Pontuação final:[/bold] [bold cyan]{user_points}[/bold cyan]\n"
    f"[bold]Aproveitamento:[/bold] [bold]{percentage:.0f}%[/bold]"
  )

  console.print(Rule("[bold magenta]Quiz finalizado[/bold magenta]", style="magenta"))
  console.print(Panel(
    f"{message}\n\n{summary}",
    title=f"[bold]{title}[/bold]",
    border_style=border_style,
    padding=(1, 2),
  ))
  console.print("\n[dim]Obrigado por jogar o [bold blue]Quiz PythonGPT[/bold blue]![/dim]")


def generate_quiz():
  number_of_questions = 0
  user_points = 0
  user_answer = ""
  user_topic = Prompt.ask("Qual tópico você gostaria de estudar hoje?")
  user_dificult = Prompt.ask("Qual nível de dificuldade você gostaria de estudar?",
  choices=["Fácil", "Médio", "Difícil"], default="Médio")

  while user_answer != "Não":
    with console.status("[bold green]Gerando pergunta...[/bold green]", spinner="dots"):
      question_created = create_question(user_topic, user_dificult)
      
    choices_created = question_created['choices']
    answer_created = question_created['answer']
    valid_choices = [str(i + 1) for i in range(len(choices_created))]

    console.print(f"[bold green]{question_created['text']}[/bold green]")

    for i, choice in enumerate(choices_created):
      console.print(f"{i + 1}. {choice}") 

    user_answer_index = int(Prompt.ask(prompt="Qual é a sua resposta?", choices=valid_choices)) -1
    user_answer = choices_created[user_answer_index]

    console.clear()
    number_of_questions += 1
    user_points = validate_answer(user_points, user_answer, answer_created)
    user_answer = ask_continue_playing()
  
  finish_quiz(user_points, number_of_questions)



def main():
  show_greeting()
  press_enter_to_continue()
  generate_quiz()


main()