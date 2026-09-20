try:
    from .problem import HMMProblem
except ImportError:  # Keep direct execution/import from this directory working.
    from problem import HMMProblem


class WeatherProblem(HMMProblem):
    def __init__(self):
        # Hidden states
        self._states = ["Rain", "Sun"]

        # 已经实际观察到的 evidence
        self._observations = ["Umbrella", "No Umbrella", "Umbrella"]

        # P(X_1)
        self.initial = {"Rain": 0.5, "Sun": 0.5}

        # P(X_t | X_{t-1})
        self.transition = {
            "Rain": {
                "Rain": 0.95,
                "Sun": 0.05
            },
            "Sun": {
                "Rain": 0.05,
                "Sun": 0.95
            }
        }

        # P(E_t | X_t)
        self.emission = {
            "Rain": {
                "Umbrella": 0.9,
                "No Umbrella": 0.1
            },
            "Sun": {
                "Umbrella": 0.2,
                "No Umbrella": 0.8
            }
        }

    @property
    def states(self):
        return self._states

    @property
    def observations(self):
        return self._observations

    def initial_probability(self, state):
        return self.initial[state]

    def transition_probability(self, previous_state, current_state):
        return self.transition[previous_state][current_state]

    def emission_probability(self, state, observation):
        return self.emission[state][observation]
