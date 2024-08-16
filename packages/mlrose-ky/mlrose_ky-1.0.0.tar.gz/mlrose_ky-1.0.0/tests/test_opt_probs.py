"""Unit tests for opt_probs/"""

# Author: Genevieve Hayes (modified by Kyle Nakamura)
# License: BSD 3 clause

import numpy as np

try:
    import mlrose_ky
except ImportError:
    import sys

    sys.path.append("..")
    import mlrose_ky

from mlrose_ky import OneMax, DiscreteOpt, ContinuousOpt, TSPOpt, OnePointCrossover
from mlrose_ky.neural import NetworkWeights
from mlrose_ky.neural.activation import identity
from mlrose_ky.opt_probs.opt_prob import OptProb


class TestOptProb:
    """Tests for _OptProb class."""

    def test_set_state_max(self):
        """Test set_state method for a maximization problem"""
        problem = OptProb(5, OneMax())
        x = np.array([0, 1, 2, 3, 4])
        problem.set_state(x)
        assert np.array_equal(problem.get_state(), x) and problem.get_fitness() == 10

    def test_set_state_min(self):
        """Test set_state method for a minimization problem"""
        problem = OptProb(5, OneMax(), maximize=False)
        x = np.array([0, 1, 2, 3, 4])
        problem.set_state(x)
        assert np.array_equal(problem.get_state(), x) and problem.get_fitness() == -10

    def test_set_population_max(self):
        """Test set_population method for a maximization problem"""
        problem = OptProb(5, OneMax())
        pop = np.array(
            [
                [0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [100, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, -50],
            ]
        )
        pop_fit = np.array([1, 3, 4, 2, 100, 0, 5, -50])
        problem.set_population(pop)
        assert np.array_equal(problem.get_population(), pop) and np.array_equal(problem.get_pop_fitness(), pop_fit)

    def test_set_population_min(self):
        """Test set_population method for a minimization problem"""
        problem = OptProb(5, OneMax(), maximize=False)
        pop = np.array(
            [
                [0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [100, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, -50],
            ]
        )
        pop_fit = -np.array([1, 3, 4, 2, 100, 0, 5, -50])
        problem.set_population(pop)
        assert np.array_equal(problem.get_population(), pop) and np.array_equal(problem.get_pop_fitness(), pop_fit)

    def test_best_child_max(self):
        """Test best_child method for a maximization problem"""
        problem = OptProb(5, OneMax())
        pop = np.array(
            [
                [0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [100, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, -50],
            ]
        )
        problem.set_population(pop)
        x = problem.best_child()
        assert np.array_equal(x, np.array([100, 0, 0, 0, 0]))

    def test_best_child_min(self):
        """Test best_child method for a minimization problem"""
        problem = OptProb(5, OneMax(), maximize=False)
        pop = np.array(
            [
                [0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [100, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, -50],
            ]
        )
        problem.set_population(pop)
        x = problem.best_child()
        assert np.array_equal(x, np.array([0, 0, 0, 0, -50]))

    def test_best_neighbor_max(self):
        """Test best_neighbor method for a maximization problem"""
        problem = OptProb(5, OneMax())
        pop = np.array(
            [
                [0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [100, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, -50],
            ]
        )
        problem.neighbors = pop
        x = problem.best_neighbor()
        assert np.array_equal(x, np.array([100, 0, 0, 0, 0]))

    def test_best_neighbor_min(self):
        """Test best_neighbor method for a minimization problem"""
        problem = OptProb(5, OneMax(), maximize=False)
        pop = np.array(
            [
                [0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [100, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, -50],
            ]
        )
        problem.neighbors = pop
        x = problem.best_neighbor()
        assert np.array_equal(x, np.array([0, 0, 0, 0, -50]))

    def test_eval_fitness_max(self):
        """Test eval_fitness method for a maximization problem"""
        problem = OptProb(5, OneMax())
        x = np.array([0, 1, 2, 3, 4])
        fitness = problem.eval_fitness(x)
        assert fitness == 10

    def test_eval_fitness_min(self):
        """Test eval_fitness method for a minimization problem"""
        problem = OptProb(5, OneMax(), maximize=False)
        x = np.array([0, 1, 2, 3, 4])
        fitness = problem.eval_fitness(x)
        assert fitness == -10

    def test_eval_mate_probs(self):
        """Test eval_mate_probs method"""
        problem = OptProb(5, OneMax())
        pop = np.array([[0, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 1, 1, 1, 0], [1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1]])
        problem.set_population(pop)
        problem.eval_mate_probs()
        probs = np.array([0.06667, 0.2, 0.26667, 0.13333, 0, 0.33333])
        assert np.allclose(problem.get_mate_probs(), probs, atol=0.00001)

    def test_eval_mate_probs_maximize_false(self):
        """Test eval_mate_probs method"""
        problem = OptProb(5, OneMax(), maximize=False)
        pop = np.array([[0, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 1, 1, 1, 0], [1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1]])
        problem.set_population(pop)
        problem.eval_mate_probs()
        probs = np.array([0.26667, 0.13333, 0.06667, 0.2, 0.33333, 0])
        assert np.allclose(problem.get_mate_probs(), probs, atol=0.00001)

    def test_eval_mate_probs_all_zero(self):
        """Test eval_mate_probs method when all states have zero fitness"""
        problem = OptProb(5, OneMax())
        pop = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
        problem.set_population(pop)
        problem.eval_mate_probs()
        probs = np.array([0.16667, 0.16667, 0.16667, 0.16667, 0.16667, 0.16667])
        assert np.allclose(problem.get_mate_probs(), probs, atol=0.00001)


class TestDiscreteOpt:
    """Tests for DiscreteOpt class."""

    def test_eval_node_probs(self):
        """Test eval_node_probs method"""
        problem = DiscreteOpt(5, OneMax())
        pop = np.array([[0, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 1, 1, 1, 0], [1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1]])
        problem.keep_sample = pop
        problem.eval_node_probs()
        parent = np.array([2, 0, 1, 0])
        probs = np.array(
            [
                [[0.33333, 0.66667], [0.33333, 0.66667]],
                [[1.0, 0.0], [0.33333, 0.66667]],
                [[1.0, 0.0], [0.25, 0.75]],
                [[1.0, 0.0], [0.0, 1.0]],
                [[0.5, 0.5], [0.25, 0.75]],
            ]
        )
        assert np.allclose(problem.node_probs, probs, atol=0.00001) and np.array_equal(problem.parent_nodes, parent)

    def test_find_neighbors_max2(self):
        """Test find_neighbors method when max_val is equal to 2"""
        problem = DiscreteOpt(5, OneMax())
        x = np.array([0, 1, 0, 1, 0])
        problem.set_state(x)
        problem.find_neighbors()
        neigh = np.array([[1, 1, 0, 1, 0], [0, 0, 0, 1, 0], [0, 1, 1, 1, 0], [0, 1, 0, 0, 0], [0, 1, 0, 1, 1]])
        assert np.array_equal(np.array(problem.neighbors), neigh)

    def test_find_neighbors_max_gt2(self):
        """Test find_neighbors method when max_val is greater than 2"""
        problem = DiscreteOpt(5, OneMax(), max_val=3)
        x = np.array([0, 1, 2, 1, 0])
        problem.set_state(x)
        problem.find_neighbors()
        neigh = np.array(
            [
                [1, 1, 2, 1, 0],
                [2, 1, 2, 1, 0],
                [0, 0, 2, 1, 0],
                [0, 2, 2, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 2, 0, 0],
                [0, 1, 2, 2, 0],
                [0, 1, 2, 1, 1],
                [0, 1, 2, 1, 2],
            ]
        )
        assert np.array_equal(np.array(problem.neighbors), neigh)

    def test_find_sample_order(self):
        """Test find_sample_order method"""
        problem = DiscreteOpt(5, OneMax())
        problem.parent_nodes = np.array([2, 0, 1, 0])
        order = np.array([0, 2, 4, 1, 3])
        problem.find_sample_order()
        assert np.array_equal(np.array(problem.sample_order), order)

    def test_find_top_pct_max(self):
        """Test find_top_pct method for a maximization problem"""
        problem = DiscreteOpt(5, OneMax())
        pop = np.array(
            [
                [0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [100, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, -50],
            ]
        )
        problem.set_population(pop)
        problem.find_top_pct(keep_pct=0.25)
        x = np.array([[100, 0, 0, 0, 0], [1, 1, 1, 1, 1]])
        assert np.array_equal(problem.get_keep_sample(), x)

    def test_find_top_pct_min(self):
        """Test find_top_pct method for a minimization problem"""
        problem = DiscreteOpt(5, OneMax(), maximize=False)
        pop = np.array(
            [
                [0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [100, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, -50],
            ]
        )
        problem.set_population(pop)
        problem.find_top_pct(keep_pct=0.25)
        x = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, -50]])
        assert np.array_equal(problem.get_keep_sample(), x)

    def test_random(self):
        """Test random method"""
        problem = DiscreteOpt(5, OneMax(), max_val=5)
        rand = problem.random()
        assert len(rand) == 5 and max(rand) >= 0 and min(rand) <= 4

    def test_random_neighbor_max2(self):
        """Test random_neighbor method when max_val is equal to 2"""
        problem = DiscreteOpt(5, OneMax())
        x = np.array([0, 0, 1, 1, 1])
        problem.set_state(x)
        neigh = problem.random_neighbor()
        sum_diff = np.sum(np.abs(x - neigh))
        assert len(neigh) == 5 and sum_diff == 1

    def test_random_neighbor_max_gt2(self):
        """Test random_neighbor method when max_val is greater than 2"""
        problem = DiscreteOpt(5, OneMax(), max_val=5)
        x = np.array([0, 1, 2, 3, 4])
        problem.set_state(x)
        neigh = problem.random_neighbor()
        abs_diff = np.abs(x - neigh)
        abs_diff[abs_diff > 0] = 1
        sum_diff = np.sum(abs_diff)
        assert len(neigh) == 5 and sum_diff == 1

    def test_random_pop(self):
        """Test random_pop method"""
        problem = DiscreteOpt(5, OneMax())
        problem.random_pop(100)
        pop = problem.get_population()
        pop_fitness = problem.get_pop_fitness()
        assert np.shape(pop)[0] == 100 and np.shape(pop)[1] == 5 and 0 < np.sum(pop) < 500 and len(pop_fitness) == 100

    def test_reproduce_mut0(self):
        """Test reproduce method when mutation_prob is 0"""
        problem = DiscreteOpt(5, OneMax())
        father = np.zeros(5)
        mother = np.ones(5)
        child = problem.reproduce(father, mother, mutation_prob=0)
        assert len(child) == 5 and 0 <= sum(child) <= 5

    def test_reproduce_mut1_max2(self):
        """Test reproduce method when mutation_prob is 1 and max_val is 2"""
        problem = DiscreteOpt(5, OneMax())
        father = np.zeros(5)
        mother = np.ones(5)
        child = problem.reproduce(father, mother, mutation_prob=1)
        assert len(child) == 5 and 0 <= sum(child) <= 5

    def test_reproduce_mut1_max_gt2(self):
        """Test reproduce method when mutation_prob is 1 and max_val is greater than 2"""
        problem = DiscreteOpt(5, OneMax(), max_val=3)
        problem._crossover = OnePointCrossover(problem)
        father = np.zeros(5)
        mother = np.ones(5) * 2
        child = problem.reproduce(father, mother, mutation_prob=1)
        assert len(child) == 5 and 0 < sum(child) < 10

    def test_sample_pop(self):
        """Test sample_pop method"""
        problem = DiscreteOpt(5, OneMax())
        pop = np.array([[0, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 1, 1, 1, 0], [1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1]])
        problem.keep_sample = pop
        problem.eval_node_probs()
        sample = problem.sample_pop(100)
        assert np.shape(sample)[0] == 100 and np.shape(sample)[1] == 5 and 0 < np.sum(sample) < 500


class TestContinuousOpt:
    """Tests for ContinuousOpt class."""

    def test_calculate_updates(self):
        """Test calculate_updates method"""
        X = np.array([[0, 1, 0, 1], [0, 0, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 1, 1], [1, 0, 0, 0]])
        y = np.reshape(np.array([1, 1, 0, 0, 1, 1]), [6, 1])
        nodes = [4, 2, 1]
        fitness = NetworkWeights(X, y, nodes, activation=identity, bias=False, is_classifier=False, learning_rate=1)

        a = list(np.arange(8) + 1)
        b = list(0.01 * (np.arange(2) + 1))
        weights = a + b
        fitness.evaluate(np.asarray(weights))

        problem = ContinuousOpt(10, fitness, maximize=False)

        updates = problem.calculate_updates()
        update1 = np.array([[-0.0017, -0.0034], [-0.0046, -0.0092], [-0.0052, -0.0104], [0.0014, 0.0028]])
        update2 = np.array([[-3.17], [-4.18]])

        assert np.allclose(updates[0], update1, atol=0.001) and np.allclose(updates[1], update2, atol=0.001)

    def test_find_neighbors_range_eq_step(self):
        """Test find_neighbors method when range equals step size"""
        problem = ContinuousOpt(5, OneMax(), step=1)
        x = np.array([0, 1, 0, 1, 0])
        problem.set_state(x)
        problem.find_neighbors()
        neigh = np.array([[1, 1, 0, 1, 0], [0, 0, 0, 1, 0], [0, 1, 1, 1, 0], [0, 1, 0, 0, 0], [0, 1, 0, 1, 1]])
        assert np.array_equal(np.array(problem.neighbors), neigh)

    def test_find_neighbors_range_gt_step(self):
        """Test find_neighbors method when range greater than step size"""
        problem = ContinuousOpt(5, OneMax(), max_val=2, step=1)
        x = np.array([0, 1, 2, 1, 0])
        problem.set_state(x)
        problem.find_neighbors()
        neigh = np.array(
            [[1, 1, 2, 1, 0], [0, 0, 2, 1, 0], [0, 2, 2, 1, 0], [0, 1, 1, 1, 0], [0, 1, 2, 0, 0], [0, 1, 2, 2, 0], [0, 1, 2, 1, 1]]
        )
        assert np.array_equal(np.array(problem.neighbors), neigh)

    def test_random(self):
        """Test random method"""
        problem = ContinuousOpt(5, OneMax(), max_val=4)
        rand = problem.random()
        assert len(rand) == 5 and max(rand) >= 0 and min(rand) <= 4

    def test_random_neighbor_range_eq_step(self):
        """Test random_neighbor method when range equals step size"""
        problem = ContinuousOpt(5, OneMax(), step=1)
        x = np.array([0, 0, 1, 1, 1])
        problem.set_state(x)
        neigh = problem.random_neighbor()
        sum_diff = np.sum(np.abs(x - neigh))
        assert len(neigh) == 5 and sum_diff == 1

    def test_random_neighbor_range_gt_step(self):
        """Test random_neighbor method when range greater than step size"""
        problem = ContinuousOpt(5, OneMax(), max_val=2, step=1)
        x = np.array([0, 1, 2, 3, 4])
        problem.set_state(x)
        neigh = problem.random_neighbor()
        abs_diff = np.abs(x - neigh)
        abs_diff[abs_diff > 0] = 1
        sum_diff = np.sum(abs_diff)
        assert len(neigh) == 5 and sum_diff == 1

    def test_random_pop(self):
        """Test random_pop method"""
        problem = ContinuousOpt(5, OneMax(), step=1)
        problem.random_pop(100)
        pop = problem.get_population()
        pop_fitness = problem.get_pop_fitness()
        assert np.shape(pop)[0] == 100 and np.shape(pop)[1] == 5 and 0 < np.sum(pop) < 500 and len(pop_fitness) == 100

    def test_reproduce_mut0(self):
        """Test reproduce method when mutation_prob is 0"""
        problem = ContinuousOpt(5, OneMax(), step=1)
        father = np.zeros(5)
        mother = np.ones(5)
        child = problem.reproduce(father, mother, mutation_prob=0)
        assert len(child) == 5 and 0 < sum(child) < 5

    def test_reproduce_mut1_range_eq_step(self):
        """Test reproduce method when mutation_prob is 1 and range equals step size"""
        problem = ContinuousOpt(5, OneMax(), step=1)
        father = np.zeros(5)
        mother = np.ones(5)
        child = problem.reproduce(father, mother, mutation_prob=1)
        assert len(child) == 5 and 0 < sum(child) < 5

    def test_reproduce_mut1_range_gt_step(self):
        """Test reproduce method when mutation_prob is 1 and range is greater than step size"""
        problem = ContinuousOpt(5, OneMax(), max_val=2, step=1)
        father = np.zeros(5)
        mother = np.array([2, 2, 2, 2, 2])
        child = problem.reproduce(father, mother, mutation_prob=1)
        assert len(child) == 5 and 0 < sum(child) < 10

    def test_update_state_in_range(self):
        """Test update_state method where all updated values are within the tolerated range"""
        problem = ContinuousOpt(5, OneMax(), max_val=20, step=1)
        x = np.array([0, 1, 2, 3, 4])
        problem.set_state(x)
        y = np.array([2, 4, 6, 8, 10])
        updated = problem.update_state(y)
        assert np.array_equal(updated, (x + y))

    def test_update_state_outside_range(self):
        """Test update_state method where some updated values are outside the tolerated range"""
        problem = ContinuousOpt(5, OneMax(), max_val=5, step=1)
        x = np.array([0, 1, 2, 3, 4])
        problem.set_state(x)
        y = np.array([2, -4, 6, -8, 10])
        updated = problem.update_state(y)
        z = np.array([2, 0, 5, 0, 5])
        assert np.array_equal(updated, z)


class TestTSPOpt:
    """Tests for TSPOpt class."""

    def test_adjust_probs_all_zero(self):
        """Test adjust_probs method when all elements in input vector sum to zero."""
        dists = [(0, 1, 3), (0, 2, 5), (0, 3, 1), (0, 4, 7), (1, 3, 6), (4, 1, 9), (2, 3, 8), (2, 4, 2), (3, 2, 8), (3, 4, 4)]
        problem = TSPOpt(5, distances=dists)
        probs = np.zeros(5)
        assert np.array_equal(problem.adjust_probs(probs), np.zeros(5))

    def test_adjust_probs_non_zero(self):
        """Test adjust_probs method when all elements in input vector sum to some value other than zero."""
        dists = [(0, 1, 3), (0, 2, 5), (0, 3, 1), (0, 4, 7), (1, 3, 6), (4, 1, 9), (2, 3, 8), (2, 4, 2), (3, 2, 8), (3, 4, 4)]
        problem = TSPOpt(5, distances=dists)
        probs = np.array([0.1, 0.2, 0, 0, 0.5])
        x = np.array([0.125, 0.25, 0, 0, 0.625])
        assert np.array_equal(problem.adjust_probs(probs), x)

    def test_find_neighbors(self):
        """Test find_neighbors method"""
        dists = [(0, 1, 3), (0, 2, 5), (0, 3, 1), (0, 4, 7), (1, 3, 6), (4, 1, 9), (2, 3, 8), (2, 4, 2), (3, 2, 8), (3, 4, 4)]
        problem = TSPOpt(5, distances=dists)
        x = np.array([0, 1, 2, 3, 4])
        problem.set_state(x)
        problem.find_neighbors()
        neigh = np.array(
            [
                [1, 0, 2, 3, 4],
                [2, 1, 0, 3, 4],
                [3, 1, 2, 0, 4],
                [4, 1, 2, 3, 0],
                [0, 2, 1, 3, 4],
                [0, 3, 2, 1, 4],
                [0, 4, 2, 3, 1],
                [0, 1, 3, 2, 4],
                [0, 1, 4, 3, 2],
                [0, 1, 2, 4, 3],
            ]
        )
        assert np.array_equal(np.array(problem.neighbors), neigh)

    def test_random(self):
        """Test random method"""
        dists = [(0, 1, 3), (0, 2, 5), (0, 3, 1), (0, 4, 7), (1, 3, 6), (4, 1, 9), (2, 3, 8), (2, 4, 2), (3, 2, 8), (3, 4, 4)]
        problem = TSPOpt(5, distances=dists)
        rand = problem.random()
        assert len(rand) == 5 and len(set(rand)) == 5

    def test_random_mimic(self):
        """Test random_mimic method"""
        dists = [(0, 1, 3), (0, 2, 5), (0, 3, 1), (0, 4, 7), (1, 3, 6), (4, 1, 9), (2, 3, 8), (2, 4, 2), (3, 2, 8), (3, 4, 4)]
        pop = np.array([[1, 0, 3, 2, 4], [0, 2, 1, 3, 4], [0, 2, 4, 3, 1], [4, 1, 3, 2, 0], [3, 4, 0, 2, 1], [2, 4, 0, 3, 1]])
        problem = TSPOpt(5, distances=dists)
        problem.keep_sample = pop
        problem.eval_node_probs()
        problem.find_sample_order()
        rand = problem.random_mimic()
        assert len(rand) == 5 and len(set(rand)) == 5

    def test_random_neighbor(self):
        """Test random_neighbor method"""
        dists = [(0, 1, 3), (0, 2, 5), (0, 3, 1), (0, 4, 7), (1, 3, 6), (4, 1, 9), (2, 3, 8), (2, 4, 2), (3, 2, 8), (3, 4, 4)]
        problem = TSPOpt(5, distances=dists)
        x = np.array([0, 1, 2, 3, 4])
        problem.set_state(x)
        neigh = problem.random_neighbor()
        abs_diff = np.abs(x - neigh)
        abs_diff[abs_diff > 0] = 1
        sum_diff = np.sum(abs_diff)
        assert len(neigh) == 5 and sum_diff == 2 and len(set(neigh)) == 5

    def test_reproduce_mut0(self):
        """Test reproduce method when mutation_prob is 0"""
        dists = [(0, 1, 3), (0, 2, 5), (0, 3, 1), (0, 4, 7), (1, 3, 6), (4, 1, 9), (2, 3, 8), (2, 4, 2), (3, 2, 8), (3, 4, 4)]
        problem = TSPOpt(5, distances=dists)
        father = np.array([0, 1, 2, 3, 4])
        mother = np.array([0, 4, 3, 2, 1])
        child = problem.reproduce(father, mother, mutation_prob=0)
        assert len(child) == 5 and len(set(child)) == 5

    def test_reproduce_mut1(self):
        """Test reproduce method when mutation_prob is 1"""
        dists = [(0, 1, 3), (0, 2, 5), (0, 3, 1), (0, 4, 7), (1, 3, 6), (4, 1, 9), (2, 3, 8), (2, 4, 2), (3, 2, 8), (3, 4, 4)]
        problem = TSPOpt(5, distances=dists)
        father = np.array([0, 1, 2, 3, 4])
        mother = np.array([4, 3, 2, 1, 0])
        child = problem.reproduce(father, mother, mutation_prob=1)
        assert len(child) == 5 and len(set(child)) == 5

    def test_sample_pop(self):
        """Test sample_pop method"""
        dists = [(0, 1, 3), (0, 2, 5), (0, 3, 1), (0, 4, 7), (1, 3, 6), (4, 1, 9), (2, 3, 8), (2, 4, 2), (3, 2, 8), (3, 4, 4)]
        pop = np.array([[1, 0, 3, 2, 4], [0, 2, 1, 3, 4], [0, 2, 4, 3, 1], [4, 1, 3, 2, 0], [3, 4, 0, 2, 1], [2, 4, 0, 3, 1]])
        problem = TSPOpt(5, distances=dists)
        problem.keep_sample = pop
        problem.eval_node_probs()
        sample = problem.sample_pop(100)
        row_sums = np.sum(sample, axis=1)
        assert np.shape(sample)[0] == 100 and np.shape(sample)[1] == 5 and max(row_sums) == 10 and min(row_sums) == 10
