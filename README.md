# Quiz PythonGPT

Quiz de múltipla escolha no terminal, com perguntas geradas por IA sobre o assunto que você escolher.

## O que faz

- Você informa um **tópico** (ex: Python, história, redes)
- Escolhe a dificuldade: **Fácil**, **Médio** ou **Difícil**
- A OpenAI gera uma pergunta com 4 alternativas
- Acertou: +1 ponto | Errou: -1 ponto (se já tiver pontos)
- No final, mostra um resumo do seu desempenho

## Como usar

1. Instale as dependências:

```bash
pip install openai rich python-dotenv
```

2. Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_aqui
```

3. Execute:

```bash
python quiz-gpt.py
```

## Exemplo no terminal

```
Bem Vindo ao Quiz PythonGPT!

Qual tópico você gostaria de estudar hoje?: Python
Qual nível de dificuldade? [Fácil/Médio/Difícil] (Médio): Médio

Qual estrutura cria um dicionário em Python?
1. []
2. ()
3. {}
4. <>

Qual é a sua resposta? [1/2/3/4]: 3

Parabéns! Você acertou!
```

## Tecnologias

- Python
- OpenAI API
- Rich (interface no terminal)
