
class Movie:
    def __init__(self, rank: int, title: str, year: int, imdb_rating: float, num_of_votes: int, num_of_won_oscars: int):
        self.rank = rank
        self.title = title
        self.year = year
        self.imdb_rating = imdb_rating
        self.num_of_votes = num_of_votes
        self.num_of_won_oscars = num_of_won_oscars

    def __calculate_penalty_based_on_votes(self, num_of_max_votes: int):
        return (num_of_max_votes - self.num_of_votes) // 100000 * 0.1

    def __calculate_reward_based_on_oscars(self):
        if self.num_of_won_oscars == 0:
            return 0
        elif self.num_of_won_oscars <= 2:
            return 0.3
        elif self.num_of_won_oscars <= 5:
            return 0.5
        elif self.num_of_won_oscars <= 10:
            return 1
        else:
            return 1.5

    def adjusted_rating(self, num_of_max_votes: int):
        penalty = self.__calculate_penalty_based_on_votes(num_of_max_votes)
        reward = self.__calculate_reward_based_on_oscars()
        return self.imdb_rating - penalty + reward

