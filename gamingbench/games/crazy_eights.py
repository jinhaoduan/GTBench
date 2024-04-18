

from gamingbench.games.openspiel_adapter import OpenSpielGame


class CrazyEights(OpenSpielGame):


    def __init__(self) -> None:
        super().__init__("crazy_eights")
        self.game_name = 'crazy_eights'
        pass
