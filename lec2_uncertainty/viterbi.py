try:
    from .problem import HMMProblem
except ImportError:  # Keep `python viterbi.py` working from this directory.
    from problem import HMMProblem


def viterbi(problem: HMMProblem):
    """
    使用 Viterbi Algorithm 找到最可能的隐藏状态序列。

    返回：
       best_path:
           最可能的 hidden-state sequence

       best_score:
           这条路径与全部 observations 的联合概率
    """
    states = problem.states
    observations = problem.observations

    if not observations:
        return [], 0.0

    # m[state]
    # 当前时刻：以 state 结束的最佳路径的概率
    previous_scores = {}

    # backpointers[t][state]
    # 到达时间 t 的 state 时，最佳路径是从哪个 previous_state 过来的
    backpointers = []

    # --------------------------------------------------
    # Day 1: Initialization
    # m_1(x) = P(x) * P(e_1 | x)
    # --------------------------------------------------
    first_observation = observations[0]

    for state in states:
        previous_scores[state] = (problem.initial_probability(state) *
                                  problem.emission_probability(state, first_observation))

    # --------------------------------------------------
    # Day 2 ... Day T
    # m_t(x) = P(e_t | x) * max_x' [m_{t-1}(x') * P(x | x')]
    # --------------------------------------------------
    for observation in observations[1:]:
        current_scores = {}
        current_backpointer = {}

        # 尝试当前状态 current_state
        # states = ["Rain", "Sun"]
        for current_state in states:
            best_previous_state = None
            best_previous_score = -1.0

            # 枚举所有可能的上一状态
            # states = ["Rain", "Sun"]
            for previous_state in states:
                score = (previous_scores[previous_state] *
                         problem.transition_probability(previous_state, current_state))

                if score > best_previous_score:
                    best_previous_score = score
                    best_previous_state = previous_state

            # 再乘当前 observation 的 emission probability
            current_scores[current_state] = (problem.emission_probability(current_state, observation) *
                                             best_previous_score)
            # 保存 argmax，也就是最佳前驱
            current_backpointer[current_state] = best_previous_state

        previous_scores = current_scores
        backpointers.append(current_backpointer)

    # --------------------------------------------------
    # Termination
    # x_T = argmax_x [m_T(x)]
    # --------------------------------------------------
    best_final_state = max(states, key=lambda state: previous_scores[state])
    best_score = previous_scores[best_final_state]

    # --------------------------------------------------
    # Backtracking
    # --------------------------------------------------
    best_path = [best_final_state]
    current_state = best_final_state

    for pointer in reversed(backpointers):
        current_state = pointer[current_state]
        best_path.append(current_state)

    best_path.reverse()

    return best_path, best_score


if __name__ == "__main__":
    try:
        from .weather_problem import WeatherProblem
    except ImportError:
        from weather_problem import WeatherProblem

    problem = WeatherProblem()
    path, score = viterbi(problem)

    print("Observations:")
    print(" -> ".join(problem.observations))
    print()

    print("Most likely hidden states:")
    print(" -> ".join(path))
    print()

    print("Best path score:")
    print(score)
