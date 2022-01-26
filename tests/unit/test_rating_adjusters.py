from unittest import TestCase

from src.imdb.rating_adjusters import OscarRewardCalculator, ReviewPenaltyCalculator


class TestOscarRewardCalculator(TestCase):

    def test_calculate_reward_based_on_oscars_0(self):
        reward = OscarRewardCalculator(0).calculate_reward_based_on_oscars()
        self.assertEqual(reward, 0, "No Oscar means no reward is added.")

    def test_calculate_reward_based_on_oscars_1or2(self):
        reward = OscarRewardCalculator(1).calculate_reward_based_on_oscars()
        self.assertEqual(reward, 0.3, "1 Oscar means 0.3 reward is added.")
        reward = OscarRewardCalculator(2).calculate_reward_based_on_oscars()
        self.assertEqual(reward, 0.3, "2 Oscar means 0.3 reward is added.")

    def test_calculate_reward_based_on_oscars_3to5(self):
        reward = OscarRewardCalculator(3).calculate_reward_based_on_oscars()
        self.assertEqual(reward, 0.5, "3 Oscar means 0.5 reward is added.")
        reward = OscarRewardCalculator(4).calculate_reward_based_on_oscars()
        self.assertEqual(reward, 0.5, "4 Oscar means 0.5 reward is added.")
        reward = OscarRewardCalculator(5).calculate_reward_based_on_oscars()
        self.assertEqual(reward, 0.5, "5 Oscar means 0.5 reward is added.")

    def test_calculate_reward_based_on_oscars_6to10(self):
        reward = OscarRewardCalculator(6).calculate_reward_based_on_oscars()
        self.assertEqual(reward, 1, "6 Oscar means 1 reward is added.")
        reward = OscarRewardCalculator(9).calculate_reward_based_on_oscars()
        self.assertEqual(reward, 1, "9 Oscar means 1 reward is added.")
        reward = OscarRewardCalculator(10).calculate_reward_based_on_oscars()
        self.assertEqual(reward, 1, "10 Oscar means 1 reward is added.")

    def test_calculate_reward_based_on_oscars_10plus(self):
        reward = OscarRewardCalculator(11).calculate_reward_based_on_oscars()
        self.assertEqual(reward, 1.5, "11 Oscar means 1.5 reward is added.")
        reward = OscarRewardCalculator(70).calculate_reward_based_on_oscars()
        self.assertEqual(reward, 1.5, "70 Oscar means 1.5 reward is added.")


class TestReviewPenaltyCalculator(TestCase):

    def test_calculate_penalty_based_on_votes_less_than_100k_deviation(self):
        penalty = ReviewPenaltyCalculator(10, 10).calculate_penalty_based_on_votes()
        self.assertEqual(penalty, 0, "Less than 100k deviation means 0 penalty.")
        penalty = ReviewPenaltyCalculator(10, 100009).calculate_penalty_based_on_votes()
        self.assertEqual(penalty, 0, "Less than 100k deviation means 0 penalty.")

    def test_calculate_penalty_based_on_votes_100k_deviation(self):
        penalty = ReviewPenaltyCalculator(10, 100010).calculate_penalty_based_on_votes()
        self.assertEqual(penalty, 0.1, "100k deviation means 0.1 penalty.")

    def test_calculate_penalty_based_on_votes_multiple_100k_deviation(self):
        penalty = ReviewPenaltyCalculator(10, 200056).calculate_penalty_based_on_votes()
        self.assertEqual(penalty, 0.2, "200k deviation means 0.2 penalty.")
        penalty = ReviewPenaltyCalculator(10, 503014).calculate_penalty_based_on_votes()
        self.assertEqual(penalty, 0.5, "500k deviation means 0.5 penalty.")
