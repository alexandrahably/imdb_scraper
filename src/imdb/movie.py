from src.imdb.rating_adjusters import OscarRewardCalculator, ReviewPenaltyCalculator


class Movie(object):
    """
    Class to represent a single movie that we scraped.
    Includes a method for getting the adjusted rating score as well.
    """

    def __init__(self, rank: int, title: str, imdb_rating: float, num_of_votes: int, num_of_won_oscars: int):
        # These must be populated by the scraper
        self.rank = rank
        self.title = title
        self.imdb_rating = imdb_rating
        self.num_of_votes = num_of_votes
        self.num_of_won_oscars = num_of_won_oscars

    def adjusted_rating(self, num_of_max_votes: int) -> float:
        """
        The adjusted rating takes into account the number of the votes and the number of the Oscars.
        However, we do not allow a negative adjusted rating.
        :param num_of_max_votes: An integer number, representing the maximum number of votes present in the referred top list
        :return: The adjusted rating, that takes into account the reward received based on the number of won Oscars,
        and the penalty received based on if the number of votes is remarkably smaller than the maximum.
        """

        penalty = ReviewPenaltyCalculator(num_of_votes=self.num_of_votes,
                                          num_of_max_votes=num_of_max_votes).calculate_penalty_based_on_votes()
        reward = OscarRewardCalculator(self.num_of_won_oscars).calculate_reward_based_on_oscars()
        return max(self.imdb_rating - penalty + reward, 0)

