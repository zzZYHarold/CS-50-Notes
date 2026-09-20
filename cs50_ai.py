"""Convenient public imports for the lecture algorithms."""

from lec0_search.adversarial_search.alphabeta_advanced import (
    alphaBetaSearch as alpha_beta_search,
)
from lec0_search.adversarial_search.depth_limited_alphabeta import (
    alphaBetaSearch as depth_limited_alpha_beta_search,
)
from lec0_search.adversarial_search.game import AdversarialGame
from lec0_search.adversarial_search.mcts import (
    monteCarloTreeSearch as monte_carlo_tree_search,
)
from lec0_search.adversarial_search.minimax_advanced import minimax
from lec0_search.search_algorithms.astar import aStarSearch as a_star_search
from lec0_search.search_algorithms.bfs import (
    breadthFirstSearch as breadth_first_search,
)
from lec0_search.search_algorithms.dfs import depthFirstSearch as depth_first_search
from lec0_search.search_algorithms.gbfs import (
    greedyBestFirstSearch as greedy_best_first_search,
)
from lec0_search.search_algorithms.iddfs import (
    iterativeDeepeningSearch as iterative_deepening_search,
)
from lec0_search.search_algorithms.problem import SearchProblem
from lec0_search.search_algorithms.ucs import uniformCostSearch as uniform_cost_search
from lec2_uncertainty.problem import HMMProblem
from lec2_uncertainty.viterbi import viterbi
from lec2_uncertainty.weather_problem import WeatherProblem
from lec3_optimization.csp.binary_CSP import CSP
from lec3_optimization.local_search.hill_climbing import hill_climb, random_restart
from lec3_optimization.local_search.problem import (
    HospitalsProblem,
    LocalSearchProblem,
    TravelingSalesmanProblem,
)
from lec3_optimization.local_search.simulated_annealing import simulated_annealing

__all__ = [
    "SearchProblem",
    "breadth_first_search",
    "depth_first_search",
    "uniform_cost_search",
    "greedy_best_first_search",
    "a_star_search",
    "iterative_deepening_search",
    "AdversarialGame",
    "minimax",
    "alpha_beta_search",
    "depth_limited_alpha_beta_search",
    "monte_carlo_tree_search",
    "HMMProblem",
    "WeatherProblem",
    "viterbi",
    "CSP",
    "LocalSearchProblem",
    "HospitalsProblem",
    "TravelingSalesmanProblem",
    "hill_climb",
    "random_restart",
    "simulated_annealing",
]
