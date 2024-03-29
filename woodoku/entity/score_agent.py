from config import COMBO_POINTS, GROUP_POINTS, STREAK_POINTS


class ScoreAgent:
    __score: int
    __streak: int
    __combo: int

    def __init__(self) -> None:
        self.__score = 0
        self.__streak = 0
        self.__combo = 0

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
        # Note: assertion can be turned off with -O flag to python
        assert blocks > 0 and groups >= 0, "Precondition violated"

        self.__score += blocks

        if groups:
            self.__score += GROUP_POINTS
            if self.__streak:
                self.__score += STREAK_POINTS * self.__streak
            self.__streak += 1
        else:
            self.__streak = 0

        combos = groups - 1
        if combos > 0:
            self.__score += COMBO_POINTS * combos

    def get_score(self) -> int:
        return self.__score

    def get_streak(self) -> int:
        return self.__streak

    def get_combo(self) -> int:
        return self.__combo
