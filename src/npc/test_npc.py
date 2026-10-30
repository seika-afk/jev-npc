"""Choice-driven gatekeeper scene for trying different dialogue routes."""

from dataclasses import dataclass

import requests

from faster_jev_call import NPC


@dataclass(frozen=True)
class DialogueChoice:
    text: str
    intent: str


ROUNDS = (
    (
        "The north gate is locked. How do you approach the gatekeeper?",
        (
            DialogueChoice("Greet the guard and introduce yourself politely.", "friendly"),
            DialogueChoice("Tell the guard you found a patrol report on the road.", "helpful"),
            DialogueChoice("Ask why the gate is locked.", "question"),
            DialogueChoice("Demand that the guard open the gate.", "hostile"),
        ),
    ),
    (
        "The guard listens. What do you say next?",
        (
            DialogueChoice("Offer to help the night watch with its work.", "helpful"),
            DialogueChoice("Thank the guard for keeping travelers safe.", "friendly"),
            DialogueChoice("Ask about the road and the next watch shift.", "question"),
            DialogueChoice("Say the guard would help if they were a decent person.", "manipulative"),
            DialogueChoice("Tell the guard you do not have time for this.", "hostile"),
        ),
    ),
)

TRUST_NEEDED_FOR_KEY = 2


def choose(options: tuple[DialogueChoice, ...]) -> DialogueChoice | None:
    for index, option in enumerate(options, start=1):
        print(f"  {index}. {option.text}")
    print("  q. Leave")
    while True:
        selected = input("\nChoose: ").strip().lower()
        if selected in {"q", "quit", "exit"}:
            return None
        if selected.isdigit() and 1 <= int(selected) <= len(options):
            return options[int(selected) - 1]
        print("Choose one of the listed numbers, or q to leave.")


def main() -> None:
    npc = NPC(name="Gatekeeper")
    print("You need the gate key to travel north. The guard does not know you yet.\n")

    for prompt, options in ROUNDS:
        print(prompt)
        choice = choose(options)
        if choice is None:
            return
        try:
            reply = npc.respond(choice.text, intent=choice.intent)
        except (requests.RequestException, KeyError, ValueError, IndexError) as error:
            print(f"\nThe gatekeeper cannot answer right now: {error}")
            return
        print(f"\nYou:      {choice.text}")
        print(f"NPC:      {reply}\n")

    print("You:      May I borrow the gate key to travel north?")
    if npc.disposition >= TRUST_NEEDED_FOR_KEY:
        print("Gatekeeper: You have treated me with respect and helped the watch. You may borrow the key; return it by dusk.")
        print("\nYou received the north gate key.")
    else:
        print("Gatekeeper: I do not know you well enough to lend out the key. Show the watch some respect and come back.")
        print("\nThe gate remains locked.")


if __name__ == "__main__":
    main()
