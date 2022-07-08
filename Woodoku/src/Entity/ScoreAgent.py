from typing import Dict


class ScoreAgent:
    __score: int

    def __init__(self):
        pass

    def calculate_winning(self, winning_map: Dict[str, int]) -> None:
        """
        Given winning map, calculate score and add to score.

        :param winning_map: e.g. { "row": 1, "column": 2, "3x3 block": 0 }
        :return:
        """
        pass

    def get_score(self) -> int:
        return self.__score
