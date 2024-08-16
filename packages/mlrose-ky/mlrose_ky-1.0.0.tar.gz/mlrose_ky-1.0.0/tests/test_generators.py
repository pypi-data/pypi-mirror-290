"""Unit tests for generators/"""

import pytest
import numpy as np

try:
    import mlrose_ky
except ImportError:
    import sys

    sys.path.append("..")
    import mlrose_ky

from mlrose_ky import ContinuousPeaks, DiscreteOpt, FourPeaks, SixPeaks, FlipFlopOpt, QueensOpt, OneMax
from mlrose_ky.generators import (
    ContinuousPeaksGenerator,
    FlipFlopGenerator,
    FourPeaksGenerator,
    SixPeaksGenerator,
    KnapsackGenerator,
    MaxKColorGenerator,
    QueensGenerator,
    TSPGenerator,
    OneMaxGenerator,
)

SEED = 12


# noinspection PyTypeChecker
class TestContinuousPeaksGenerator:

    def test_generate_size_zero(self):
        """Test generate method raises ValueError when size is zero"""
        with pytest.raises(ValueError) as excinfo:
            ContinuousPeaksGenerator.generate(SEED, size=0)
        assert str(excinfo.value) == "Size must be a positive integer. Got 0"

    def test_generate_negative_size(self):
        """Test generate method raises ValueError when size is a negative integer"""
        with pytest.raises(ValueError) as excinfo:
            ContinuousPeaksGenerator.generate(SEED, size=-5)
        assert str(excinfo.value) == "Size must be a positive integer. Got -5"

    def test_generate_non_integer_size(self):
        """Test generate method raises ValueError when size is a non-integer value"""
        with pytest.raises(ValueError) as excinfo:
            ContinuousPeaksGenerator.generate(SEED, size="ten")
        assert str(excinfo.value) == "Size must be a positive integer. Got ten"

    def test_generate_negative_threshold_percentage(self):
        """Test generate method raises ValueError when threshold_percentage is less than 0"""
        with pytest.raises(ValueError) as excinfo:
            ContinuousPeaksGenerator.generate(SEED, size=10, threshold_percentage=-0.1)
        assert str(excinfo.value) == "Threshold percentage must be between 0 and 1. Got -0.1"

    def test_generate_threshold_percentage_greater_than_one(self):
        """Test generate method raises ValueError when threshold_percentage is greater than 1"""
        with pytest.raises(ValueError) as excinfo:
            ContinuousPeaksGenerator.generate(SEED, size=10, threshold_percentage=1.1)
        assert str(excinfo.value) == "Threshold percentage must be between 0 and 1. Got 1.1"

    def test_generate_non_float_threshold_percentage(self):
        """Test generate method raises ValueError when threshold_percentage is a non-float value"""
        with pytest.raises(ValueError) as excinfo:
            ContinuousPeaksGenerator.generate(SEED, size=10, threshold_percentage="high")
        assert str(excinfo.value) == "Threshold percentage must be a float. Got str"

    def test_generate_default_size(self):
        """Test generate method with default size"""
        problem = ContinuousPeaksGenerator.generate(SEED)

        assert problem.length == 20

    def test_generate_default_threshold_percentage(self):
        """Test generate method with default threshold_percentage"""
        size = 20
        problem = ContinuousPeaksGenerator.generate(SEED, size)

        assert problem.length == size
        assert problem.fitness_fn.threshold_percentage == 0.1

    def test_generate_with_seed(self):
        """Test generate method with a specified SEED"""
        problem = ContinuousPeaksGenerator.generate(SEED)
        np.random.seed(SEED)
        expected_fitness = ContinuousPeaks()
        expected_problem = DiscreteOpt(length=20, fitness_fn=expected_fitness)

        assert problem.length == expected_problem.length
        assert problem.fitness_fn.__class__ == expected_problem.fitness_fn.__class__
        assert problem.fitness_fn.threshold_percentage == expected_problem.fitness_fn.threshold_percentage

    def test_generate_custom_size_and_threshold(self):
        """Test generate method with custom size and threshold_percentage"""
        size = 30
        threshold_percentage = 0.2
        problem = ContinuousPeaksGenerator.generate(SEED, size=size, threshold_percentage=threshold_percentage)

        assert problem.length == size
        assert problem.fitness_fn.threshold_percentage == threshold_percentage


# noinspection PyTypeChecker
class TestFlipFlopGenerator:

    def test_generate_size_zero(self):
        """Test generate method raises ValueError when size is zero."""
        with pytest.raises(ValueError) as excinfo:
            FlipFlopGenerator.generate(SEED, size=0)
        assert str(excinfo.value) == "Size must be a positive integer. Got 0."

    def test_generate_negative_size(self):
        """Test generate method raises ValueError when size is negative."""
        with pytest.raises(ValueError) as excinfo:
            FlipFlopGenerator.generate(SEED, size=-5)
        assert str(excinfo.value) == "Size must be a positive integer. Got -5."

    def test_generate_non_integer_size(self):
        """Test generate method raises ValueError when size is a non-integer value."""
        with pytest.raises(TypeError):
            FlipFlopGenerator.generate(SEED, size="ten")

    def test_generate_default_size(self):
        """Test generate method with default size."""
        problem = FlipFlopGenerator.generate(SEED)

        assert problem.length == 20

    def test_generate_with_seed(self):
        """Test generate method with a specified SEED."""
        problem = FlipFlopGenerator.generate(SEED)
        np.random.seed(SEED)
        expected_problem = FlipFlopOpt(length=20)

        assert problem.length == expected_problem.length
        assert problem.__class__ == expected_problem.__class__

    def test_generate_custom_size(self):
        """Test generate method with custom size."""
        size = 30
        problem = FlipFlopGenerator.generate(SEED, size=size)

        assert problem.length == size


# noinspection PyTypeChecker
class TestFourPeaksGenerator:

    def test_generate_size_zero(self):
        """Test generate method raises ValueError when size is zero."""
        with pytest.raises(ValueError) as excinfo:
            FourPeaksGenerator.generate(SEED, size=0)
        assert str(excinfo.value) == "Size must be a positive integer. Got 0."

    def test_generate_negative_size(self):
        """Test generate method raises ValueError when size is negative."""
        with pytest.raises(ValueError) as excinfo:
            FourPeaksGenerator.generate(SEED, size=-5)
        assert str(excinfo.value) == "Size must be a positive integer. Got -5."

    def test_generate_non_integer_size(self):
        """Test generate method raises ValueError when size is a non-integer value."""
        with pytest.raises(TypeError):
            FourPeaksGenerator.generate(SEED, size="ten")

    def test_generate_negative_threshold_percentage(self):
        """Test generate method raises ValueError when threshold_percentage is less than 0."""
        with pytest.raises(ValueError) as excinfo:
            FourPeaksGenerator.generate(SEED, size=10, threshold_percentage=-0.1)
        assert str(excinfo.value) == "Threshold percentage must be between 0 and 1. Got -0.1."

    def test_generate_threshold_percentage_greater_than_one(self):
        """Test generate method raises ValueError when threshold_percentage is greater than 1."""
        with pytest.raises(ValueError) as excinfo:
            FourPeaksGenerator.generate(SEED, size=10, threshold_percentage=1.1)
        assert str(excinfo.value) == "Threshold percentage must be between 0 and 1. Got 1.1."

    def test_generate_non_float_threshold_percentage(self):
        """Test generate method raises ValueError when threshold_percentage is a non-float value."""
        with pytest.raises(TypeError):
            FourPeaksGenerator.generate(SEED, size=10, threshold_percentage="high")

    def test_generate_default_size(self):
        """Test generate method with default size."""
        problem = FourPeaksGenerator.generate(SEED)

        assert problem.length == 20

    def test_generate_default_threshold_percentage(self):
        """Test generate method with default threshold_percentage."""
        size = 20
        problem = FourPeaksGenerator.generate(SEED, size)

        assert problem.length == size
        assert problem.fitness_fn.threshold_percentage == 0.1

    def test_generate_with_seed(self):
        """Test generate method with a specified SEED."""
        problem = FourPeaksGenerator.generate(SEED)
        np.random.seed(SEED)
        expected_fitness = FourPeaks()
        expected_problem = DiscreteOpt(length=20, fitness_fn=expected_fitness)

        assert problem.length == expected_problem.length
        assert problem.fitness_fn.__class__ == expected_problem.fitness_fn.__class__
        assert problem.fitness_fn.threshold_percentage == expected_problem.fitness_fn.threshold_percentage

    def test_generate_custom_size_and_threshold(self):
        """Test generate method with custom size and threshold_percentage."""
        size = 30
        threshold_percentage = 0.2
        problem = FourPeaksGenerator.generate(SEED, size=size, threshold_percentage=threshold_percentage)

        assert problem.length == size
        assert problem.fitness_fn.threshold_percentage == threshold_percentage


# noinspection PyTypeChecker
class TestSixPeaksGenerator:

    def test_generate_size_zero(self):
        """Test generate method raises ValueError when size is zero."""
        with pytest.raises(ValueError) as excinfo:
            SixPeaksGenerator.generate(SEED, size=0)
        assert str(excinfo.value) == "Size must be a positive integer. Got 0."

    def test_generate_negative_size(self):
        """Test generate method raises ValueError when size is negative."""
        with pytest.raises(ValueError) as excinfo:
            SixPeaksGenerator.generate(SEED, size=-5)
        assert str(excinfo.value) == "Size must be a positive integer. Got -5."

    def test_generate_non_integer_size(self):
        """Test generate method raises ValueError when size is a non-integer value."""
        with pytest.raises(TypeError):
            SixPeaksGenerator.generate(SEED, size="ten")

    def test_generate_negative_threshold_percentage(self):
        """Test generate method raises ValueError when threshold_percentage is less than 0."""
        with pytest.raises(ValueError) as excinfo:
            SixPeaksGenerator.generate(SEED, size=10, threshold_percentage=-0.1)
        assert str(excinfo.value) == "Threshold percentage must be between 0 and 1. Got -0.1."

    def test_generate_threshold_percentage_greater_than_one(self):
        """Test generate method raises ValueError when threshold_percentage is greater than 1."""
        with pytest.raises(ValueError) as excinfo:
            SixPeaksGenerator.generate(SEED, size=10, threshold_percentage=1.1)
        assert str(excinfo.value) == "Threshold percentage must be between 0 and 1. Got 1.1."

    def test_generate_non_float_threshold_percentage(self):
        """Test generate method raises ValueError when threshold_percentage is a non-float value."""
        with pytest.raises(TypeError):
            SixPeaksGenerator.generate(SEED, size=10, threshold_percentage="high")

    def test_generate_default_size(self):
        """Test generate method with default size."""
        problem = SixPeaksGenerator.generate(SEED)

        assert problem.length == 20

    def test_generate_default_threshold_percentage(self):
        """Test generate method with default threshold_percentage."""
        size = 20
        problem = SixPeaksGenerator.generate(SEED, size)

        assert problem.length == size
        assert problem.fitness_fn.threshold_percentage == 0.1

    def test_generate_with_seed(self):
        """Test generate method with a specified SEED."""
        problem = SixPeaksGenerator.generate(SEED)
        np.random.seed(SEED)
        expected_fitness = SixPeaks()
        expected_problem = DiscreteOpt(length=20, fitness_fn=expected_fitness)

        assert problem.length == expected_problem.length
        assert problem.fitness_fn.__class__ == expected_problem.fitness_fn.__class__
        assert problem.fitness_fn.threshold_percentage == expected_problem.fitness_fn.threshold_percentage

    def test_generate_custom_size_and_threshold(self):
        """Test generate method with custom size and threshold_percentage."""
        size = 30
        threshold_percentage = 0.2
        problem = SixPeaksGenerator.generate(SEED, size=size, threshold_percentage=threshold_percentage)

        assert problem.length == size
        assert problem.fitness_fn.threshold_percentage == threshold_percentage


# noinspection PyTypeChecker
class TestKnapsackGenerator:

    def test_generate_valid_case(self):
        """Test generate method with valid parameters."""
        number_of_item_types = 10
        max_item_count = 5
        max_weight_per_item = 25
        max_value_per_item = 10
        max_weight_percentage = 0.6
        multiply_by_max_item_count = True

        problem = KnapsackGenerator.generate(
            seed=SEED,
            number_of_item_types=number_of_item_types,
            max_item_count=max_item_count,
            max_weight_per_item=max_weight_per_item,
            max_value_per_item=max_value_per_item,
            max_weight_percentage=max_weight_percentage,
            multiply_by_max_item_count=multiply_by_max_item_count,
        )

        assert problem.length == number_of_item_types
        assert problem.max_val == max_item_count

    def test_generate_invalid_seed(self):
        """Test generate method raises ValueError when SEED is not an integer."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(seed="not_an_int")
        assert str(excinfo.value) == "Seed must be an integer. Got not_an_int"

    def test_generate_invalid_number_of_item_types(self):
        """Test generate method raises ValueError when number_of_item_types is invalid."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, number_of_item_types=0)
        assert str(excinfo.value) == "Number of item types must be a positive integer. Got 0"

    def test_generate_invalid_max_item_count(self):
        """Test generate method raises ValueError when max_item_count is invalid."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, max_item_count=-1)
        assert str(excinfo.value) == "Max item count must be a positive integer. Got -1"

    def test_generate_invalid_max_weight_per_item(self):
        """Test generate method raises ValueError when max_weight_per_item is invalid."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, max_weight_per_item=0)
        assert str(excinfo.value) == "Max weight per item must be a positive integer. Got 0"

    def test_generate_invalid_max_value_per_item(self):
        """Test generate method raises ValueError when max_value_per_item is invalid."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, max_value_per_item=-10)
        assert str(excinfo.value) == "Max value per item must be a positive integer. Got -10"

    def test_generate_default_parameters(self):
        """Test generate method with default parameters."""
        problem = KnapsackGenerator.generate(seed=SEED)

        assert problem.length == 10
        assert problem.max_val == 5

    def test_generate_invalid_max_weight_percentage(self):
        """Test generate method raises ValueError when max_weight_percentage is invalid."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, max_weight_percentage=1.5)
        assert str(excinfo.value) == "Max weight percentage must be a float between 0 and 1. Got 1.5"

    def test_generate_invalid_multiply_by_max_item_count(self):
        """Test generate method raises ValueError when multiply_by_max_item_count is not a boolean."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, multiply_by_max_item_count="yes")
        assert str(excinfo.value) == "multiply_by_max_item_count must be a boolean. Got yes"

    def test_generate_max_weight_percentage_zero(self):
        """Test generate method with max_weight_percentage set to 0"""
        max_weight_percentage = 0.0

        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(seed=SEED, max_weight_percentage=max_weight_percentage)
        assert str(excinfo.value) == "max_weight_pct must be greater than 0."


# noinspection PyTypeChecker
class TestMaxKColorGenerator:

    def test_generate_negative_max_colors(self):
        """Test generate method raises ValueError when max_colors is a negative integer."""
        with pytest.raises(ValueError) as excinfo:
            MaxKColorGenerator.generate(SEED, number_of_nodes=10, max_colors=-3)
        assert str(excinfo.value) == "Max colors must be a positive integer or None. Got -3"

    def test_generate_non_integer_max_colors(self):
        """Test generate method raises ValueError when max_colors is a non-integer value."""
        with pytest.raises(ValueError) as excinfo:
            MaxKColorGenerator.generate(SEED, number_of_nodes=10, max_connections_per_node=3, max_colors="five")
        assert str(excinfo.value) == "Max colors must be a positive integer or None. Got five"

    def test_generate_seed_float(self):
        """Test generate method raises ValueError when SEED is a float."""
        with pytest.raises(ValueError) as excinfo:
            MaxKColorGenerator.generate(seed=1.5)
        assert str(excinfo.value) == "Seed must be an integer. Got 1.5"

    def test_generate_float_number_of_nodes(self):
        """Test generate method raises ValueError when number_of_nodes is a float."""
        with pytest.raises(ValueError) as excinfo:
            MaxKColorGenerator.generate(SEED, number_of_nodes=10.5)
        assert str(excinfo.value) == "Number of nodes must be a positive integer. Got 10.5"

    def test_generate_max_connections_per_node_float(self):
        """Test generate method raises ValueError when max_connections_per_node is a float."""
        with pytest.raises(ValueError) as excinfo:
            MaxKColorGenerator.generate(SEED, number_of_nodes=10, max_connections_per_node=4.5)
        assert str(excinfo.value) == "Max connections per node must be a positive integer. Got 4.5"

    def test_generate_maximize_string(self):
        """Test generate method raises ValueError when maximize is a string."""
        with pytest.raises(ValueError) as excinfo:
            MaxKColorGenerator.generate(SEED, maximize="true")
        assert str(excinfo.value) == "Maximize must be a boolean. Got true"

    def test_generate_single_node_one_connection(self):
        """Test generate method with one node and up to one connection."""
        number_of_nodes = 1
        max_connections_per_node = 1
        problem = MaxKColorGenerator.generate(SEED, number_of_nodes=number_of_nodes, max_connections_per_node=max_connections_per_node)

        assert problem.length == number_of_nodes
        assert problem.source_graph.number_of_edges() == 0

    def test_generate_single_node_two_connections(self):
        """Test generate method with one node and up to two connections."""
        number_of_nodes = 1
        max_connections_per_node = 2
        problem = MaxKColorGenerator.generate(SEED, number_of_nodes=number_of_nodes, max_connections_per_node=max_connections_per_node)

        assert problem.length == number_of_nodes
        assert problem.source_graph.number_of_edges() == 0

    def test_generate_two_nodes_one_connection(self):
        """Test generate method with two nodes and up to one connection."""
        number_of_nodes = 2
        max_connections_per_node = 1
        problem = MaxKColorGenerator.generate(SEED, number_of_nodes=number_of_nodes, max_connections_per_node=max_connections_per_node)

        assert problem.length == number_of_nodes
        assert problem.source_graph.number_of_edges() == 1

    def test_generate_two_nodes_two_connections(self):
        """Test generate method with two nodes and up to two connections."""
        number_of_nodes = 2
        max_connections_per_node = 2
        problem = MaxKColorGenerator.generate(SEED, number_of_nodes=number_of_nodes, max_connections_per_node=max_connections_per_node)

        assert problem.length == number_of_nodes
        assert problem.source_graph.number_of_edges() == 1

    def test_generate_large_graph(self):
        """Test generate method with a large graph."""
        number_of_nodes = 100
        max_connections_per_node = 10
        problem = MaxKColorGenerator.generate(SEED, number_of_nodes=number_of_nodes, max_connections_per_node=max_connections_per_node)

        assert problem.length == number_of_nodes
        assert problem.source_graph.number_of_edges() > 0

    def test_generate_no_edges(self):
        """Test generate method with no possible connections."""
        with pytest.raises(ValueError) as excinfo:
            MaxKColorGenerator.generate(SEED, number_of_nodes=10, max_connections_per_node=0)
        assert str(excinfo.value) == "Max connections per node must be a positive integer. Got 0"

    def test_generate_max_colors_none(self):
        """Test generate method with max_colors set to None."""
        number_of_nodes = 5
        max_connections_per_node = 3
        problem = MaxKColorGenerator.generate(SEED, number_of_nodes=number_of_nodes, max_connections_per_node=max_connections_per_node)

        assert problem.length == number_of_nodes
        assert problem.max_val > 1

    def test_generate_zero_nodes(self):
        """Test generate method raises ValueError when number_of_nodes is zero."""
        with pytest.raises(ValueError) as excinfo:
            MaxKColorGenerator.generate(SEED, number_of_nodes=0)
        assert str(excinfo.value) == "Number of nodes must be a positive integer. Got 0"

    def test_generate_large_max_colors(self):
        """Test generate method with a large max_colors value."""
        number_of_nodes = 10
        max_connections_per_node = 3
        max_colors = 100
        problem = MaxKColorGenerator.generate(
            SEED, number_of_nodes=number_of_nodes, max_connections_per_node=max_connections_per_node, max_colors=max_colors
        )

        assert problem.length == number_of_nodes
        assert problem.max_val == max_colors

    def test_generate_large_max_connections(self):
        """Test generate method with large max_connections_per_node value."""
        number_of_nodes = 10
        max_connections_per_node = 9
        problem = MaxKColorGenerator.generate(SEED, number_of_nodes=number_of_nodes, max_connections_per_node=max_connections_per_node)

        assert problem.length == number_of_nodes
        assert problem.source_graph.number_of_edges() > 0


# noinspection PyTypeChecker
class TestQueensGenerator:

    def test_generate_size_zero(self):
        """Test generate method raises ValueError when size is zero."""
        with pytest.raises(ValueError) as excinfo:
            QueensGenerator.generate(SEED, size=0)
        assert str(excinfo.value) == "Size must be a positive integer. Got 0"

    def test_generate_negative_size(self):
        """Test generate method raises ValueError when size is negative."""
        with pytest.raises(ValueError) as excinfo:
            QueensGenerator.generate(SEED, size=-5)
        assert str(excinfo.value) == "Size must be a positive integer. Got -5"

    def test_generate_non_integer_size(self):
        """Test generate method raises ValueError when size is a non-integer value."""
        with pytest.raises(ValueError) as excinfo:
            QueensGenerator.generate(SEED, size="ten")
        assert str(excinfo.value) == "Size must be a positive integer. Got ten"

    def test_generate_invalid_seed(self):
        """Test generate method raises ValueError when seed is not an integer."""
        with pytest.raises(ValueError) as excinfo:
            QueensGenerator.generate(seed="not_an_int")
        assert str(excinfo.value) == "Seed must be an integer. Got not_an_int"

    def test_generate_invalid_maximize(self):
        """Test generate method raises ValueError when maximize is not a boolean."""
        with pytest.raises(ValueError) as excinfo:
            QueensGenerator.generate(SEED, maximize="yes")
        assert str(excinfo.value) == "Maximize must be a boolean. Got yes"

    def test_generate_default_size(self):
        """Test generate method with default size."""
        problem = QueensGenerator.generate(SEED)

        assert problem.length == 20

    def test_generate_with_seed(self):
        """Test generate method with a specified seed."""
        problem = QueensGenerator.generate(SEED)
        np.random.seed(SEED)
        expected_problem = QueensOpt(length=20)

        assert problem.length == expected_problem.length
        assert problem.__class__ == expected_problem.__class__

    def test_generate_custom_size(self):
        """Test generate method with custom size."""
        size = 30
        problem = QueensGenerator.generate(SEED, size=size)

        assert problem.length == size


# noinspection PyTypeChecker
class TestTSPGenerator:

    def test_generate_invalid_seed(self):
        """Test generate method raises ValueError when seed is not an integer."""
        with pytest.raises(ValueError) as excinfo:
            TSPGenerator.generate(seed="not_an_int", number_of_cities=5)
        assert str(excinfo.value) == "Seed must be an integer. Got not_an_int"

    def test_generate_invalid_number_of_cities(self):
        """Test generate method raises ValueError when number_of_cities is not a positive integer."""
        with pytest.raises(ValueError) as excinfo:
            TSPGenerator.generate(SEED, number_of_cities=0)
        assert str(excinfo.value) == "Number of cities must be a positive integer. Got 0"

    def test_generate_invalid_area_width(self):
        """Test generate method raises ValueError when area_width is not a positive integer."""
        with pytest.raises(ValueError) as excinfo:
            TSPGenerator.generate(SEED, number_of_cities=5, area_width=0)
        assert str(excinfo.value) == "Area width must be a positive integer. Got 0"

    def test_generate_invalid_area_height(self):
        """Test generate method raises ValueError when area_height is not a positive integer."""
        with pytest.raises(ValueError) as excinfo:
            TSPGenerator.generate(SEED, number_of_cities=5, area_height=0)
        assert str(excinfo.value) == "Area height must be a positive integer. Got 0"

    def test_generate_default_parameters(self):
        """Test generate method with default parameters."""
        num_cities = 5
        problem = TSPGenerator.generate(seed=SEED, number_of_cities=num_cities)

        assert problem.length == num_cities
        assert problem.coords is not None
        assert problem.distances is not None
        assert problem.source_graph is not None

    def test_generate_custom_parameters(self):
        """Test generate method with custom parameters."""
        num_cities = 5
        problem = TSPGenerator.generate(seed=SEED, number_of_cities=num_cities, area_width=100, area_height=100)

        assert problem.length == num_cities
        assert problem.coords is not None
        assert problem.distances is not None
        assert problem.source_graph is not None

    def test_generate_no_duplicate_coordinates(self):
        """Test generate method ensures no duplicate coordinates."""
        problem = TSPGenerator.generate(seed=SEED, number_of_cities=5)
        coords = problem.coords

        assert len(coords) == len(set(coords))

    def test_generate_distances(self):
        """Test generate method calculates distances correctly."""
        problem = TSPGenerator.generate(seed=SEED, number_of_cities=5)
        distances = problem.distances
        for u, v, d in distances:
            assert d == np.linalg.norm(np.subtract(problem.coords[u], problem.coords[v]))

    def test_generate_graph(self):
        """Test generate method creates a valid graph."""
        problem = TSPGenerator.generate(seed=SEED, number_of_cities=5)
        graph = problem.source_graph

        assert graph.number_of_nodes() == 5
        assert graph.number_of_edges() == len(problem.distances)

    def test_generate_valid_case(self):
        """Test generate method with valid parameters."""
        number_of_item_types = 10
        max_item_count = 5
        max_weight_per_item = 25
        max_value_per_item = 10
        max_weight_percentage = 0.6
        multiply_by_max_item_count = True

        problem = KnapsackGenerator.generate(
            seed=SEED,
            number_of_item_types=number_of_item_types,
            max_item_count=max_item_count,
            max_weight_per_item=max_weight_per_item,
            max_value_per_item=max_value_per_item,
            max_weight_percentage=max_weight_percentage,
            multiply_by_max_item_count=multiply_by_max_item_count,
        )

        assert problem.length == number_of_item_types
        assert problem.max_val == max_item_count

    def test_generate_invalid_number_of_item_types(self):
        """Test generate method raises ValueError when number_of_item_types is invalid."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, number_of_item_types=0)
        assert str(excinfo.value) == "Number of item types must be a positive integer. Got 0"

    def test_generate_invalid_max_item_count(self):
        """Test generate method raises ValueError when max_item_count is invalid."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, max_item_count=-1)
        assert str(excinfo.value) == "Max item count must be a positive integer. Got -1"

    def test_generate_invalid_max_weight_per_item(self):
        """Test generate method raises ValueError when max_weight_per_item is invalid."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, max_weight_per_item=0)
        assert str(excinfo.value) == "Max weight per item must be a positive integer. Got 0"

    def test_generate_invalid_max_value_per_item(self):
        """Test generate method raises ValueError when max_value_per_item is invalid."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, max_value_per_item=-10)
        assert str(excinfo.value) == "Max value per item must be a positive integer. Got -10"

    def test_generate_invalid_max_weight_percentage(self):
        """Test generate method raises ValueError when max_weight_percentage is invalid."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, max_weight_percentage=1.5)
        assert str(excinfo.value) == "Max weight percentage must be a float between 0 and 1. Got 1.5"

    def test_generate_invalid_multiply_by_max_item_count(self):
        """Test generate method raises ValueError when multiply_by_max_item_count is not a boolean."""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(SEED, multiply_by_max_item_count="yes")
        assert str(excinfo.value) == "multiply_by_max_item_count must be a boolean. Got yes"

    def test_generate_max_weight_percentage_zero(self):
        """Test generate method with max_weight_percentage set to 0"""
        with pytest.raises(ValueError) as excinfo:
            KnapsackGenerator.generate(seed=SEED, max_weight_percentage=0.0)
        assert str(excinfo.value) == "max_weight_pct must be greater than 0."


# noinspection PyTypeChecker
class TestOneMaxGenerator:

    def test_generate_size_zero(self):
        """Test generate method raises ValueError when size is zero."""
        with pytest.raises(ValueError) as excinfo:
            OneMaxGenerator.generate(SEED, size=0)
        assert str(excinfo.value) == "Size must be a positive integer. Got 0"

    def test_generate_negative_size(self):
        """Test generate method raises ValueError when size is negative."""
        with pytest.raises(ValueError) as excinfo:
            OneMaxGenerator.generate(SEED, size=-5)
        assert str(excinfo.value) == "Size must be a positive integer. Got -5"

    def test_generate_non_integer_size(self):
        """Test generate method raises ValueError when size is a non-integer value."""
        with pytest.raises(ValueError) as excinfo:
            OneMaxGenerator.generate(SEED, size="ten")
        assert str(excinfo.value) == "Size must be a positive integer. Got ten"

    def test_generate_invalid_seed(self):
        """Test generate method raises ValueError when seed is not an integer."""
        with pytest.raises(ValueError) as excinfo:
            OneMaxGenerator.generate(seed="not_an_int")
        assert str(excinfo.value) == "Seed must be an integer. Got not_an_int"

    def test_generate_default_size(self):
        """Test generate method with default size."""
        problem = OneMaxGenerator.generate(SEED)

        assert problem.length == 20

    def test_generate_with_seed(self):
        """Test generate method with a specified seed."""
        problem = OneMaxGenerator.generate(SEED)
        np.random.seed(SEED)
        expected_problem = DiscreteOpt(length=20, fitness_fn=OneMax())

        assert problem.length == expected_problem.length
        assert problem.__class__ == expected_problem.__class__

    def test_generate_custom_size(self):
        """Test generate method with custom size."""
        size = 30
        problem = OneMaxGenerator.generate(SEED, size=size)

        assert problem.length == size
