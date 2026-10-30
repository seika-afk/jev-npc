"""Command-line entry point for a small stateful NPC conversation."""

from .faster_jev_call import NPC, NPCServiceError


def main() -> None:
    npc = NPC()
    print(f"You are speaking with {npc.name}. Type /quit to leave.")
    while True:
        try:
            player_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if player_text.lower() in {"/quit", "/exit"}:
            return
        try:
            print(f"{npc.name}: {npc.respond(player_text)}")
        except NPCServiceError as error:
            print(f"{npc.name}: I cannot find the words right now. ({error})")
