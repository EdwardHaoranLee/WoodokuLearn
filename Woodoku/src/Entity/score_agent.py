from typing import Dict


class ScoreAgent:
    __score: int

    def __init__(self):
        pass

    def calculate_winning(self, group_info: Dict[str, int]) -> None:
        """Given `groups`, calculate score and add to score

        Args:
            group_info (Dict[str, int]): A dictionary mapping from name of the
            group to the number of groups. e.g. { "row": 1, "column": 2, "box": 0 }
        """
        pass

    def get_score(self) -> int:
        return self.__score
