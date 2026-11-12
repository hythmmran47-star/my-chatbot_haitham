"""Gemini integration for the medical-learning chatbot.

The API key is read from the server environment. Never hard-code credentials
or expose them through frontend code or committed files.
"""

import logging
import os
from typing import Any

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an educational assistant for medical students.
Answer educational questions about anatomy, physiology, pathology, and general
medical concepts in clear language. Explain technical terms and organize longer
answers. Do not diagnose a real person or prescribe medication. You are not a
substitute for qualified medical care. For possible emergencies, advise the
user to contact local emergency services or a qualified healthcare professional.
If a question is outside medical education, politely explain your scope.
Respond in the language used by the user whenever possible.
""".strip()


def _format_history(history: list[dict[str, Any]] | None) -> str:
    if not history:
        return ""
    lines: list[str] = []
    for item in history[-20:]:
        content = str(item.get("content", "")).strip()
        if not content:
            continue
        sender = str(item.get("sender", "user")).lower()
        role = "Assistant" if sender in {"bot", "assistant", "model"} else "User"
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def call_gemini(
    user_message: str,
    system_prompt: str = SYSTEM_PROMPT,
    history: list[dict[str, Any]] | None = None,
) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY is not configured.")
        return "لم يتم إعداد مفتاح خدمة الذكاء الاصطناعي. أضف GOOGLE_API_KEY إلى ملف .env ثم أعد تشغيل التطبيق."

    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        context = _format_history(history)
        parts = [system_prompt.strip()]
        if context:
            parts.append("Previous conversation:\n" + context)
        parts.append("User: " + user_message.strip())
        response = model.generate_content("\n\n".join(parts))
        answer = getattr(response, "text", None)
        if answer and answer.strip():
            return answer.strip()
        logger.warning("Gemini returned an empty response.")
        return "لم أتمكن من إنشاء إجابة الآن. أعد صياغة سؤالك وحاول مرة أخرى."
    except Exception:
        logger.exception("Gemini request failed.")
        return "تعذر الاتصال بخدمة الذكاء الاصطناعي حاليًا. تحقق من الاتصال والإعدادات ثم حاول مرة أخرى."
