"""Boucle de chat terminal avec Relay (API Claude)."""

import json
from pathlib import Path

from dotenv import load_dotenv
import anthropic

from src.config import ROOT, load_config, load_profile


def load_history(path: Path) -> list:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def save_history(path: Path, history: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    load_dotenv()  # lit ANTHROPIC_API_KEY depuis .env
    config = load_config()
    system = load_profile(config)
    history_path = ROOT / config["history_path"]
    history = load_history(history_path)
    client = anthropic.Anthropic()

    print("Relay pret. Tape 'exit' pour quitter.")
    while True:
        user = input("> ").strip()
        if user.lower() in {"exit", "quit"}:
            break
        if not user:
            continue
        history.append({"role": "user", "content": user})
        response = client.messages.create(
            model=config["model"],
            max_tokens=config["max_tokens"],
            system=system,
            messages=history,
        )
        reply = response.content[0].text
        history.append({"role": "assistant", "content": reply})
        save_history(history_path, history)
        print(f"\n{reply}\n")


if __name__ == "__main__":
    main()
