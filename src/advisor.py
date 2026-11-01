"""Farmer advice from the Groq LLM."""
from groq import Groq

from . import config

SYSTEM = (
    "You are an experienced agricultural advisor talking to farmers. "
    "Use simple words and keep answers short. "
    "Reply in {language}, unless the farmer writes in another language, then reply in theirs. "
    "Suggest organic and home remedies first, then chemical options. "
    "You may name a pesticide or its active ingredient, but never state an exact dose: "
    "tell the farmer to read the product label or ask the nearest agricultural extension office. "
    "If a question is not about farming, politely say you can only help with farming. "
    "If you do not know something, say so instead of guessing."
)

_client = None  # created on first use so the app can start without a key


def ask(messages):
    global _client
    if _client is None:
        _client = Groq(api_key=config.GROQ_API_KEY)
    r = _client.chat.completions.create(
        model=config.GROQ_MODEL,
        temperature=config.GROQ_TEMPERATURE,
        messages=[{"role": "system", "content": SYSTEM.format(language=config.REPLY_LANGUAGE)}] + messages,
    )
    return r.choices[0].message.content
