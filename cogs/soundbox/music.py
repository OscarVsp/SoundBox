# -*- coding: utf-8 -*-
from typing import List

import disnake


class Music:
    def __init__(self, name: str, emote: str, volume: float = 1.0, description: str = None) -> None:
        self.file_name = f"cogs/soundbox/sounds/{name}.wav"
        self.name = name
        self.description = description
        self.volume = volume
        self.emote: str = emote

    @property
    def sound(self) -> disnake.PCMVolumeTransformer:
        sound = disnake.PCMVolumeTransformer(disnake.FFmpegPCMAudio(self.file_name))
        sound.volume = self.volume
        return sound


music_list: List[Music] = [
    Music("On les souleve", "<:BoudhaPog:854084071055032340>", description="Ace D Ashura durant une finale de Clash"),
    Music("Fontaine", "⛲", description="Ace D Ashura en trolling"),
]
