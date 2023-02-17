# -*- coding: utf-8 -*-
import disnake

from .music import music_list


class SoundBoxUI(disnake.ui.View):
    def __init__(self, inter: disnake.ApplicationCommandInteraction) -> None:
        super().__init__(timeout=None)
        self.inter = inter
        self.voice_client: disnake.VoiceClient = None

    async def connect(self, voice_channel: disnake.VoiceChannel):
        self.voice_client = await voice_channel.connect()

    @property
    def embed(self) -> disnake.Embed:
        return disnake.Embed(title="__**Sound Box**__", color=disnake.Colour.dark_teal())

    @classmethod
    async def new(cld, inter: disnake.ApplicationCommandInteraction, voice_channel: disnake.VoiceChannel):
        new_SB = SoundBoxUI(inter)
        await new_SB.connect(voice_channel)
        await inter.edit_original_response(embed=new_SB.embed, view=new_SB)

    async def update(self, inter: disnake.MessageInteraction):
        await inter.edit_original_response(embed=self.embed, view=self)

    @disnake.ui.string_select(
        placeholder="Choisit un son à jouer",
        options=[disnake.SelectOption(label=m.name, value=music_list.index(m), emoji=m.emote) for m in music_list],
    )
    async def music_select(self, select: disnake.ui.StringSelect, inter: disnake.MessageInteraction):
        await inter.response.defer()
        music_to_play = music_list[int(select.values[0])]
        self.music_select.disabled = True
        self.music_select.placeholder = f'Playing "{music_to_play.name}"...'
        await self.update(inter)
        await music_to_play.play(self.voice_client)
        self.music_select.disabled = False
        self.music_select.placeholder = "Choisit un son à jouer"
        await self.update(inter)

    @disnake.ui.button(label="Stop", emoji="❌", style=disnake.ButtonStyle.danger)
    async def btn_stop(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(embed=disnake.Embed(title="__**Sound Box**__"), view=None)
        self.stop()
        await self.voice_client.disconnect()
        await self.inter.delete_original_message()
