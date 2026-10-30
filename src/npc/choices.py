"""Dialogue data used by the NPC conversation engine."""

from __future__ import annotations


DIALOGUE_BY_INTENT: dict[str, tuple[str, ...]] = {
    "friendly": (
        "Good to meet you. It has been a quiet shift at the gate.",
        "You seem considerate. Not many travelers bother to be polite.",
        "I appreciate the respectful approach. What brings you to the north road?",
    ),
    "hostile": (
        "Threats do not open this gate. Step back.",
        "Keep that tone to yourself. The key stays with me.",
        "We can talk when you are ready to be civil. Until then, no key.",
    ),
    "helpful": (
        "That patrol report is useful. I will make sure the watch hears about it.",
        "Thanks for looking out for the people on this road.",
        "That kind of help matters. The night watch has been stretched thin.",
    ),
    "question": (
        "The gate is locked because the road beyond is dangerous after dark.",
        "I have been on watch since dawn. The next guard arrives at sunset.",
        "The north road is rough, but the bridge is passable today.",
    ),
    "manipulative": (
        "Guilt will not change my mind. The key stays here.",
        "Say what you want plainly; do not try to pressure me for the key.",
        "Do not corner me with words. You will not get the key that way.",
    ),
    "neutral": (
        "The gate closes at sunset. That is the rule.",
        "Understood. I will keep watch until the next guard arrives.",
        "Fair enough. It has been a long day at the post.",
    ),
}

scattered_dialogues = {intent: list(lines) for intent, lines in DIALOGUE_BY_INTENT.items()}
