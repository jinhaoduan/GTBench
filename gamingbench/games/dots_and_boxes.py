

from gamingbench.games.openspiel_adapter import OpenSpielGame


class KuhnPoker(DotsAndBoxes):

    def __init__(self) -> None:
        super().__init__("dots_and_boxes")
        self.game_name = 'dots_and_boxes'
        pass
