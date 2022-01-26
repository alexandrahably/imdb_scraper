
class OscarRewardCalculator:

    def __init__(self, num_of_won_oscars: int):
        self.num_of_won_oscars = num_of_won_oscars

    def calculate_reward_based_on_oscars(self) -> float:
        if self.num_of_won_oscars == 0:
            return 0
        if self.num_of_won_oscars <= 2:
            return 0.3
        if self.num_of_won_oscars <= 5:
            return 0.5
        if self.num_of_won_oscars <= 10:
            return 1
        return 1.5


class ReviewPenaltyCalculator:

    def __init__(self, num_of_votes: int, num_of_max_votes: int):
        self.num_of_votes = num_of_votes
        self.num_of_max_votes = num_of_max_votes

    def calculate_penalty_based_on_votes(self) -> float:
        return (self.num_of_max_votes - self.num_of_votes) // 100000 * 0.1

