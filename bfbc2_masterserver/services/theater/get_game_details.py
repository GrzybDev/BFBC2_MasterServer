from bfbc2_masterserver.messages.theater.commands.GetGameDetails import (
    GetGameDetailsRequest,
    GetGameDetailsResponse,
)


def handle_get_game_details(ctx, data: GetGameDetailsRequest):
    yield GetGameDetailsResponse()
