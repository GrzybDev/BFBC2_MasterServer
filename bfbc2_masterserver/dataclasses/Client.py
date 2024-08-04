class Client:
    def __init__(self):
        from bfbc2_masterserver.dataclasses.Handler import (
            BaseHandler,
            BaseTheaterHandler,
        )

        self.plasma: BaseHandler
        self.theater: BaseTheaterHandler
