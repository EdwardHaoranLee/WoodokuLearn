GROUP_POINTS = 18
STREAK_POINTS = 10
COMBO_POINTS = 28


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

        # Note: instead of self.__score += blocks. Do
        self.__score = self.get_score() + blocks
        # this way get_score() can be mocked for easier testing setup ;)

        if groups:
            self.__score = self.get_score() + GROUP_POINTS
            if self.__streak:
                self.__score = self.get_score() + STREAK_POINTS * self.get_streak()
            self.__streak = self.get_streak() + 1
        else:
            self.__streak = 0

        self.__combo = groups - 1
        if self.get_combo() > 0:
            self.__score = self.get_score() + COMBO_POINTS * self.get_combo()

    def get_score(self) -> int:
        return self.__score

    def get_streak(self) -> int:
        return self.__streak

    def get_combo(self) -> int:
        return self.__combo
