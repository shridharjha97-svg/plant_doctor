"""Chat logic, kept separate from the Streamlit screen so it is easy to test."""
from . import advisor, classifier, config


def reply(text, image_bytes, history):
    """Answer a question and/or a leaf photo.

    history: earlier [{"role", "content"}] messages (text only).
    """
    prefix, user_turn = "", text

    if image_bytes:
        try:
            name, conf = classifier.diagnose(image_bytes)[0]
        except Exception:
            return "The photo could not be opened. Please try again with a JPG or PNG image."
        # Low confidence: do not guess and do not call the LLM
        if conf < config.MIN_CONFIDENCE:
            return (
                f"I am not sure what this is (closest match: {name}, {conf:.0%}).\n\n"
                "Take one leaf, close up, in good light, facing the camera, and scan it again. "
                "You can also describe the symptoms in the chat."
            )
        prefix = f"🔍 **Detected:** {name} ({conf:.0%} confidence)\n\n"
        user_turn = (
            f"A model detected '{name}' on my crop leaf photo (confidence {conf:.0%}). "
            "Explain the symptoms, cause, treatment and prevention. " + text
        )

    try:
        answer = advisor.ask(history + [{"role": "user", "content": user_turn}])
    except Exception as e:
        return prefix + f"The advice service is not responding right now. Please try again in a moment.\n\n(Technical: {e})"
    # The prefix stays in the stored history, so follow-up questions remember the diagnosis
    return prefix + answer
