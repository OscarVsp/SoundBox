# -*- coding: utf-8 -*-
import asyncio
from typing import List

import disnake


class Music:
    def __init__(self, name: str, emote: str, volume: float = 1.0) -> None:
        self.file_name = f"cogs/soundbox/sounds/{name}.wav"
        self.name = name
        self.volume = volume
        self.emote: str = emote

    async def play(self, voice: disnake.VoiceClient):
        voice.play(
            disnake.PCMVolumeTransformer(disnake.FFmpegPCMAudio(self.file_name)),
            after=lambda e: print(f"Player error: {e}") if e else None,
        )
        while voice.is_playing():
            await asyncio.sleep(0.1)
        return


music_list: List[Music] = [Music("On les souleve", "<:BoudhaPog:854084071055032340>"), Music("Fontaine", "⛲")]
