class Game:
    members = []
    def __init__(self, gameID, initiator):
        self.gameID = gameID
        self.members.append(initiator)
