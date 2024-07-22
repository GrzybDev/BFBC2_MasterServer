import logging

from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.messages.theater.commands.Login import (
    LoginRequest,
    LoginResponse,
)

logger = logging.getLogger(__name__)


def handle_login(ctx: BaseTheaterHandler, data: LoginRequest):
    uid = int(ctx.manager.redis.get(f"persona:{data.LKEY}").decode("utf-8"))

    if not uid or ctx.plasma.connection.personaId != uid:
        logger.error(f"Persona is not logged in Plasma!")
        return

    database = ctx.manager.database
    persona = database.get_persona_by_id(uid)

    response = LoginResponse(NAME=persona.name)

    yield response
