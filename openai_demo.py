from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY_HERE")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": "What is photosynthesis?"
        }
    ],
    max_tokens=1024
)

answer = response.choices[0].message.content

print(answer)

