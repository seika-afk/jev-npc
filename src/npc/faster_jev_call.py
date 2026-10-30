"""Stateful NPC dialogue selection backed by the local SystemOne service."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

import requests
from choices import DIALOGUE_BY_INTENT

URL = "http://localhost:11434/v1/systemone"
MODEL = "tev1:0.8b"
INTENTS = tuple(DIALOGUE_BY_INTENT)

INTENT_CRITERIA = {
    "friendly": "Warm, welcoming, or sociable language that builds rapport.",
    "hostile": "Aggressive, insulting, threatening, or confrontational language.",
    "helpful": "Offers useful advice, assistance, guidance, or information.",
    "question": "Primarily seeks information, clarification, or an answer.",
    "manipulative": "Uses guilt, pressure, deception, or emotional leverage to control someone.",
    "neutral": "Matter-of-fact speech without a strong emotional or persuasive intent.",
}


def _choice(response: requests.Response) -> str:
    response.raise_for_status()
    return response.json()["answers"]["category"]["choice"]




@dataclass
class NPC:
    name: str = "Stranger"
    disposition: int = 0
    history: list[dict[str, str]] = field(default_factory=list)
    session: requests.Session = field(default_factory=requests.Session, repr=False)

    def _ask(self, state: str, criteria: dict[str, str]) -> str:
        payload: dict[str, Any] = {
            "model": MODEL,
            "state": state,
            "questions": {"category": {"type": "choice", "instructions": "Choose exactly one option that best fits the dialogue.", "criteria": criteria}},
        }
        return _choice(self.session.post(URL, json=payload, timeout=30))

    def classify(self, player_text: str) -> str:
        intent = self._ask(player_text, INTENT_CRITERIA)
        return intent

    def respond(self, player_text: str, *, intent: str | None = None) -> str:
        """Reply to a player line and record both sides of the exchange."""
        player_text = player_text.strip()
        if not player_text:
            return "Say something, and I will answer."
        intent = intent or self.classify(player_text)
        options = DIALOGUE_BY_INTENT[intent]
        previous_reply = self.history[-1]["text"] if self.history else None
        available_options = tuple(reply for reply in options if reply != previous_reply) or options
        recent = self.history[-4:]
        transcript = "\n".join(f"{turn['speaker']}: {turn['text']}" for turn in recent)
        context = (
            f"NPC: {self.name}\nDisposition: {self.disposition} (-2 guarded to 2 trusting)\n"
            f"Recent conversation:\n{transcript or '(none)'}\n\nPlayer ({intent}): {player_text}\n"
            "Choose the reply that is most natural, non-repetitive, and fits the NPC disposition."
        )
        response = self._ask(context, {str(i): line for i, line in enumerate(available_options)})
        reply = available_options[int(response)]
        self.disposition = max(-2, min(2, self.disposition + {"friendly": 1, "helpful": 1, "hostile": -1, "manipulative": -1}.get(intent, 0)))
        self.history.extend(({"speaker": "player", "text": player_text, "intent": intent}, {"speaker": self.name, "text": reply}))
        return reply


@lru_cache(maxsize=10_000)
def classify(state: str) -> str:
    """Compatibility helper for code that only needs an intent classification."""
    return NPC().classify(state)


_default_npc = NPC()


def npc_reply(text: str) -> str:
    return _default_npc.respond(text)


def reply(text: str, category: str | None = None) -> str:
    return npc_reply(text)
