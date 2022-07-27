GROUP_POINTS = 18
STREAK_POINTS = 10
COMBO_POINTS = 28


class ScoreAgent:
    __score: int
    __streaks: int

    def __init__(self):
        self.__score = 0
        self.__streaks = 0

    def calculate_winning(self, blocks: int, groups: int) -> None:
        """Given `groups`, calculate score and add to score

        Precondition: blocks > 0, groups >= 0

        Scoring Rules:
            1. 1 point for each block placed
            2. A single groups scores 18 points
            3. Each streak adds 10 points on top of the previous streak
            4. Each additional combo adds 28 points

        Args:
            blocks (int): The number of blocks placed
            groups (int): The number of groups completed
        """
        self.__score += blocks

        if groups:
            self.__score += GROUP_POINTS
            if self.__streaks:
                self.__score += STREAK_POINTS * self.__streaks
            self.__streaks += 1
        else:
            self.__streaks = 0

        combos = groups - 1
        if combos > 0:
            self.__score += COMBO_POINTS * combos

    def get_score(self) -> int:
        return self.__score
