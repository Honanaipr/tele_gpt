import asyncio

from tortoise import Tortoise, run_async

from tele_gpt.models import User


async def init_db() -> None:
    await Tortoise.init(
        config_file="tele_gpt/tortoise_config.json",
    )
    await Tortoise.generate_schemas()
