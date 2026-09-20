"""Student implementations for CS 4341 Assignment 2."""
from __future__ import annotations
import time

WIN = 1_000_000

class _Timeout(Exception):
    pass

# Import utilities
try:
    from .adversarial_search import (
        ActionT,
        AdversarialSearchProblem,
        PlayerT,
        StateT,
    )
except ImportError:
    from adversarial_search import (
        ActionT,
        AdversarialSearchProblem,
        PlayerT,
        StateT,
    )

from cylindrical_connect_four import WINDOWS
# Replace this with the name your group wants displayed in the tournament.
GROUP_NAME = "Bello"


def adversarial_search(
    problem: AdversarialSearchProblem[StateT, ActionT, PlayerT],
    state: StateT,
) -> ActionT | None:
    if problem.is_terminal(state):
        return None

    legal = tuple(problem.actions(state))
    if not legal:
        return None

    player = problem.to_move(state)
    deadline = time.perf_counter() + 4.0
    best_move = legal[0]

    for depth in range(1, 42 - state.ply + 1):
        try: 
            value, move = max_value(problem, state, depth, player, -float("inf"), float("inf"), deadline)
        except _Timeout:
            break
        if move is not None:
            best_move = move

        if abs(value) >= WIN - 100:
            break

    return best_move

def max_value(problem, state, depth, player, alpha, beta, deadline):
    if time.perf_counter() >= deadline:
        raise _Timeout
    if problem.is_terminal(state):
        return problem.utility(state, player) * (WIN - state.ply), None
    if depth == 0:
        return h(state, player), None # heuristic
    v, move = -float('inf'), None
    for a in problem.actions(state):
        v2, _ = min_value(problem, problem.result(state, a), depth - 1, player, alpha, beta, deadline)
        if v2 > v:
            v, move = v2, a
        alpha = max(alpha, v)
        if v >= beta:
            return v, move
    return v, move
        

def min_value(problem, state, depth, player, alpha, beta, deadline):
    if time.perf_counter() >= deadline:
        raise _Timeout
    if problem.is_terminal(state):
        return problem.utility(state, player) * (WIN - state.ply), None
    if depth == 0:
        return h(state, player), None # come up w heuristic
    v, move = float('inf'), None
    for a in problem.actions(state):
        v2, _ = max_value(problem, problem.result(state, a), depth - 1, player, alpha, beta, deadline)
        if v2 < v:
            v, move = v2, a
        beta = min(beta, v)
        if v <= alpha:
            return v, move
    return v, move

## REPLACE
def h(state, player):
    return 0