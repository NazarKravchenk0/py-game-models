import json
from pathlib import Path

from db.models import Guild, Player, Race, Skill


def main() -> None:
    players_path = Path(__file__).resolve().parent / "players.json"
    with players_path.open("r", encoding="utf-8") as f:
        players = json.load(f)

    for player_data in players:
        # --- Race ---
        race_data = player_data["race"]
        race, _ = Race.objects.get_or_create(
            name=race_data["name"],
            defaults={"description": race_data.get("description", "") or ""},
        )

        # --- Skills (unique by name, but also tied to race) ---
        for skill_data in race_data.get("skills", []):
            Skill.objects.get_or_create(
                name=skill_data["name"],
                defaults={
                    "bonus": skill_data.get("bonus", "") or "",
                    "race": race,
                },
            )

        # --- Guild (can be missing / null) ---
        guild_obj = None
        guild_data = player_data.get("guild")
        if guild_data:
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_data["name"],
                defaults={"description": guild_data.get("description")},
            )

        # --- Player (unique by nickname) ---
        Player.objects.update_or_create(
            nickname=player_data["nickname"],
            defaults={
                "email": player_data["email"],
                "bio": player_data["bio"],
                "race": race,
                "guild": guild_obj,
            },
        )


if __name__ == "__main__":
    main()
