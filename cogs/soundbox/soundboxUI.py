# -*- coding: utf-8 -*-
import asyncio
import logging

import disnake

from .music import Music
from .music import music_list


class SoundBoxUI(disnake.ui.View):
    def __init__(self, inter: disnake.ApplicationCommandInteraction) -> None:
        super().__init__(timeout=None)
        self.inter = inter
        self.voice_client: disnake.VoiceClient = None
        self.global_volume: float = 0.5

    async def connect(self, voice_channel: disnake.VoiceChannel):
        self.voice_client = await voice_channel.connect()

    @property
    def embed(self) -> disnake.Embed:
        return disnake.Embed(
            title="__**Sound Box**__",
            description=f"""Selected sound: **"{music_list[int(self.music_select.values[0])].name if len(self.music_select.values) > 0 else 'None'}"**\nSound volume: {int(self.global_volume*100)}%""",
            color=disnake.Colour.dark_teal(),
        )

    @classmethod
    async def new(cld, inter: disnake.ApplicationCommandInteraction, voice_channel: disnake.VoiceChannel):
        new_SB = SoundBoxUI(inter)
        await new_SB.connect(voice_channel)
        await inter.edit_original_response(embed=new_SB.embed, view=new_SB)

    async def update(self, inter: disnake.MessageInteraction):
        await inter.edit_original_response(embed=self.embed, view=self)

    async def play_sound(self, music: Music, inter: disnake.MessageInteraction):
        self.music_select.disabled = True
        self.music_select.placeholder = f'Playing "{music.name}"...'
        self.btn_replay.disabled = True
        await self.update(inter)

        sound = music.sound
        sound.volume = sound.volume * self.global_volume
        self.voice_client.play(
            sound,
            after=lambda e: logging.error(f"Sound player error: {e}") if e else None,
        )
        while self.voice_client.is_playing():
            await asyncio.sleep(0.1)

        self.music_select.disabled = False
        self.music_select.placeholder = music.name
        self.btn_replay.disabled = False
        await self.update(inter)

    @disnake.ui.string_select(
        placeholder="Choisit un son à jouer",
        options=[
            disnake.SelectOption(label=m.name, value=music_list.index(m), emoji=m.emote, description=m.description)
            for m in music_list
        ],
    )
    async def music_select(self, select: disnake.ui.StringSelect, inter: disnake.MessageInteraction):
        await inter.response.defer()
        if select.disabled == False:
            select.disabled = True
            await self.play_sound(music_list[int(self.music_select.values[0])], inter)

    @disnake.ui.button(label="Replay", emoji="🔁", style=disnake.ButtonStyle.green, disabled=True)
    async def btn_replay(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        await self.play_sound(music_list[int(self.music_select.values[0])], inter)

    @disnake.ui.button(emoji="🔉", style=disnake.ButtonStyle.primary)
    async def btn_vol_down(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.global_volume -= 0.1
        self.btn_vol_up.disabled = False
        if self.global_volume <= 0.0:
            self.global_volume = 0.0
            button.disabled = True
        await self.update(inter)

    @disnake.ui.button(emoji="🔊", style=disnake.ButtonStyle.primary)
    async def btn_vol_up(self, button: disnake.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.global_volume += 0.1
        self.btn_vol_down.disabled = False
        if self.global_volume >= 1.0:
            self.global_volume = 1.0
            button.disabled = True
        await self.update(inter)

    @disnake.ui.button(label="Stop", emoji="❌", style=disnake.ButtonStyle.danger)
    async def btn_stop(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(embed=disnake.Embed(title="__**Sound Box**__"), view=None)
        self.stop()
        await self.voice_client.disconnect()
        await self.inter.delete_original_message()
