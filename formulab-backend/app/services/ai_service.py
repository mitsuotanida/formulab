import json
import anthropic
from app.config import settings

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _client


def generate_exercise(
    exercise_type: str,
    domain: str,
    difficulty: str,
    ra_focus: list[int],
    custom_context: str | None = None,
) -> dict:
    from app.prompts.generate_exercise import SYSTEM_PROMPT, build_generation_messages
    messages = build_generation_messages(exercise_type, domain, difficulty, ra_focus, custom_context)
    response = _get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def evaluate_formulation(
    exercise_description: str,
    data_table: dict | None,
    reference_solution: dict,
    student_submission: str,
) -> dict:
    from app.prompts.evaluate_formulation import EVALUATION_SYSTEM_PROMPT, build_evaluation_messages
    messages = build_evaluation_messages(exercise_description, data_table, reference_solution, student_submission)
    response = _get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=EVALUATION_SYSTEM_PROMPT,
        messages=messages,
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)
