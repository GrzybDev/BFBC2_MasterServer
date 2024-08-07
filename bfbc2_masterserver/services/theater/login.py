import logging

from bfbc2_masterserver.dataclasses.Handler import BaseTheaterHandler
from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.messages.theater.commands.Login import (
    LoginRequest,
    LoginResponse,
)

logger = logging.getLogger(__name__)


def handle_login(ctx: BaseTheaterHandler, data: LoginRequest):
    if not ctx.client.connection.account or not ctx.client.connection.persona:
        logger.error(f"Persona is not logged in Plasma!")
        return

    if ctx.client.connection.personaSession != data.LKEY:
        logger.error(f"Plasma session key is invalid!")
        return

    database = ctx.manager.database
    persona = database.persona_get_by_id(ctx.client.connection.persona.id)

    response = LoginResponse(NAME=persona.name)
    yield response
