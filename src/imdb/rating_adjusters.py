
class OscarRewardCalculator:
    """
    This class facilitates extra reward calculation for movies with Oscars.
    For adjusted ratings of movies, we calculate an increase (=reward) for a movie based on the number of Oscars it received.
    """

    def __init__(self, num_of_won_oscars: int):
        """
        Constructs the necessary attribute that is needed to calculate the rewards of a movie.
        :param num_of_won_oscars: Number (int) of Oscars the referred movie has won
        """
        self.num_of_won_oscars = num_of_won_oscars

    def calculate_reward_based_on_oscars(self) -> float:
        """
        For adjusted ratings of movies, we calculate an increase (=reward) for a movie based on the number of Oscars it received.
        - 1 or 2 Oscars → 0.3 point
        - 3 or 5 Oscars → 0.5 point
        - 6 - 10 Oscars → 1 point
        - 10+ Oscars → 1.5 point
        For example, if a movie is awarded 4 Oscar titles and the original IMDB rating is 7.5, the adjusted value will increase to 8 points.
        :return: reward (float): A reward (=increase) that should be applied to the rating of the referred movie
        """
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
    """
    Ratings give us an impression of how many people think a film is good or bad.
    The goal of this class is to calculate a decrease (=penalty) for those films where the number of reviews is low.
    - We find the film with the maximum number of reviews (from the top list of movies) 'num_of_max_votes'. This is going to be the benchmark.
    - We compare every movie’s number of reviews to this and penalize each movie based on a rule: every 100k deviation translates to 0.1 point reduction.
    """

    def __init__(self, num_of_votes: int, num_of_max_votes: int):
        """
        Constructs all necessary attributes that are needed to calculate the penalties of a movie.
        :param num_of_votes: Number (int) of Oscars the referred movie has won
        :param num_of_max_votes: Number (int) of the maximum votes a movie from the referred top list has received
        """
        self.num_of_votes = num_of_votes
        self.num_of_max_votes = num_of_max_votes

    def calculate_penalty_based_on_votes(self) -> float:
        """
        For every 100k deviation from the maximum vote number 'num_of_max_votes' translates to a point deduction of 0.1.
        For example, suppose the maximum number of reviews is 2.456.123. For a given movie with 1.258.369
        ratings and an IMDB score of 9.4, the amount of the deduction is 1.1 and therefore the adjusted rating is 8.3.
        :return: penalty: A float number, that represents the penalty (=decrease) that should be applied to the rating of the referred movie
        """
        return (self.num_of_max_votes - self.num_of_votes) // 100000 * 0.1

