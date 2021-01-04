from pathlib import Path

import discord
from discord.ext import commands

import os

from dotenv import load_dotenv

load_dotenv()


class MusicBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]

        super().__init__(command_prefix=self.prefix, case_insensitive=True)

    def setup(self):
        print("Starting up...")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f"Loaded {cog}.")

        print("Startup complete.")

    def run(self):
        self.setup()

        TOKEN = os.environ.get("TOKEN")

        print("Running bot...")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing connection...")
        await super().close()

    async def close(self):
        print("Shutting down...")
        await self.shutdown()

    async def on_connect(self):
        print("Connected...")

    async def on_disconnect(self):
        print("Disconnected.")

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Ready.")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or(".")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)
