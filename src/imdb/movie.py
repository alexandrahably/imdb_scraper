from src.imdb.rating_adjusters import OscarRewardCalculator, ReviewPenaltyCalculator


class Movie:
    """
    Class to represent a single movie that we scraped.
    Includes methods for getting the adjusted rating score.
    """

    def __init__(self, rank: int, title: str, imdb_rating: float, num_of_votes: int, num_of_won_oscars: int):
        # These must be populated by the scraper
        self.rank = rank
        self.title = title
        self.imdb_rating = imdb_rating
        self.num_of_votes = num_of_votes
        self.num_of_won_oscars = num_of_won_oscars

    def to_array_with_original_rating(self) -> [str]:
        return [f'{self.imdb_rating:.2f}', str(self.num_of_votes), str(self.num_of_won_oscars), self.title]

    def to_array_with_adjusted_rating(self, num_of_max_votes) -> [str]:
        return [f'{self.adjusted_rating(num_of_max_votes):.2f}', str(self.num_of_votes), str(self.num_of_won_oscars), self.title]

    def adjusted_rating(self, num_of_max_votes: int) -> float:
        # The adjusted rating takes into account the number of the votes and the number of the Oscars.
        # However, we do not allow a negative adjusted rating.
        penalty = ReviewPenaltyCalculator(num_of_votes=self.num_of_votes,
                                          num_of_max_votes=num_of_max_votes).calculate_penalty_based_on_votes()
        reward = OscarRewardCalculator(self.num_of_won_oscars).calculate_reward_based_on_oscars()
        return max(self.imdb_rating - penalty + reward, 0)
