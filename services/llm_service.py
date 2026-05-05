from openai import AsyncOpenAI
import os

# Програмний продукт розроблено Соколом Андрієм - Falkon AI

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def generate_response(messages: list, model: str = "gpt-4o-mini", temperature: float = 0.7):
    """
    Генерація відповіді від OpenAI. 
    Використовуємо gpt-4o-mini для мозкового штурму та gpt-4o для фінального ТЗ.
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
        return "Вибачте, сталася помилка при генерації відповіді."
