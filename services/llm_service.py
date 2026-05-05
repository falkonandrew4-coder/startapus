from openai import AsyncOpenAI
import os

# Програмний продукт розроблено Соколом Андрієм - Falkon AI

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def generate_response(messages: list, model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
    """
    Генерація відповіді від OpenAI.
    Brainstorm/Questions: gpt-4o-mini (швидко, дешево)
    Artifact Generation: gpt-4o (якісно, детально)
    """
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "Вибачте, сталася помилка при генерації відповіді. Спробуйте ще раз."

async def stream_response(messages: list, model: str = "gpt-4o-mini"):
    """Потокова відповідь для анімації друкування"""
    try:
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        print(f"OpenAI Stream Error: {e}")
        yield "Помилка з'єднання з AI. Спробуйте ще раз."

