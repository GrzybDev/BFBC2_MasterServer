class Client:
    def __init__(self):
        from bfbc2_masterserver.dataclasses.Handler import BaseHandler

        self.plasma: BaseHandler
        self.theater: BaseHandler
