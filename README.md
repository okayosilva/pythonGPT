# PythonGPT Quiz
Terminal-based multiple-choice quiz with AI-generated questions on a topic of your choice.

## What it does
- You provide a **topic** (e.g., Python, history, networking)
- Choose the difficulty: **Easy**, **Medium**, or **Hard**
- OpenAI generates a question with 4 answer choices
- Correct answer: +1 point | Wrong answer: -1 point (if you already have points)
- At the end, it shows a summary of your performance

## How to use
1. Install the dependencies:
```bash
pip install openai rich python-dotenv
```
2. Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_key_here
```
3. Run it:
```bash
python quiz-gpt.py
```

## Terminal example
```
Welcome to PythonGPT Quiz!
What topic would you like to study today?: Python
What difficulty level? [Easy/Medium/Hard] (Medium): Medium
Which structure creates a dictionary in Python?
1. []
2. ()
3. {}
4. <>
What is your answer? [1/2/3/4]: 3
Congratulations! You got it right!
```

## Technologies
- Python
- OpenAI API
- Rich (terminal interface)
