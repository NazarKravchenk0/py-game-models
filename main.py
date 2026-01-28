import json
from pathlib import Path
from typing import Any

from db.models import Guild, Player, Race, Skill


def _extract_players(data: Any) -> list[dict]:
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        if "players" in data and isinstance(data["players"], list):
            return data["players"]
        return [v for v in data.values() if isinstance(v, dict)]

    return []


def main() -> None:
    players_path = Path(__file__).resolve().parent / "players.json"
    with players_path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    players = _extract_players(raw_data)

    for player_data in players:
        race_raw = player_data.get("race")

        if isinstance(race_raw, str):
            race_name = race_raw
            race_description = ""
            race_skills = player_data.get("skills", [])
        elif isinstance(race_raw, dict):
            race_name = race_raw.get("name", "")
            race_description = race_raw.get("description", "") or ""
            race_skills = race_raw.get("skills", []) or []
        else:
            race_name = ""
            race_description = ""
            race_skills = []

        race, _ = Race.objects.get_or_create(
            name=race_name,
            defaults={"description": race_description},
        )

        for skill_raw in race_skills:
            if isinstance(skill_raw, dict):
                skill_name = skill_raw.get("name", "")
                bonus = skill_raw.get("bonus", "") or ""
            else:
                skill_name = str(skill_raw)
                bonus = ""

            Skill.objects.get_or_create(
                name=skill_name,
                defaults={
                    "bonus": bonus,
                    "race": race,
                },
            )

        guild_obj = None
        guild_raw = player_data.get("guild")

        if isinstance(guild_raw, str):
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_raw,
                defaults={"description": None},
            )
        elif isinstance(guild_raw, dict):
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_raw.get("name", ""),
                defaults={
                    "description": guild_raw.get("description"),
                },
            )

        Player.objects.update_or_create(
            nickname=player_data.get("nickname", ""),
            defaults={
                "email": player_data.get("email", ""),
                "bio": player_data.get("bio", ""),
                "race": race,
                "guild": guild_obj,
            },
        )


if __name__ == "__main__":
    main()
