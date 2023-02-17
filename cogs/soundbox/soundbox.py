# -*- coding: utf-8 -*-
import disnake
from disnake.ext import commands

from .soundboxUI import SoundBoxUI
from bot import Bot


class SoundBox(commands.Cog):
    def __init__(self, bot: Bot):
        """Initialize the cog"""
        self.bot: Bot = bot

    @commands.slash_command(name="soundbox")
    async def soundbox(
        self,
        inter: disnake.ApplicationCommandInteraction,
        voice_channel: disnake.VoiceChannel = commands.Param(description="Le channel vocal à rejoindre."),
    ):
        await inter.response.defer()
        await SoundBoxUI.new(inter, voice_channel)


def setup(bot: commands.InteractionBot):

    bot.add_cog(SoundBox(bot))
