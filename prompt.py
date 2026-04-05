domain: str = "Fitness"
tone: str = "Friendly"
audience: str = "Beginner"
question: str = "How much protein do I need for daily intake?"

prompt: str = f"""You are a {domain} expert.

RULES:
Only answer questions about {domain}.

STYLE:
- Tone: {tone}
- Audience: {audience}

QUESTION:
{question}
"""

print(prompt)
