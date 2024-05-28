"""
## Bayes Node

This module defines the BayesNode class for representing nodes in a Bayesian network.

Classes:
- BayesNode: Represents a node in a Bayesian network. Each node represents a random variable, 
  which can be either True or False.

Functions:
- probability: Returns True with a probability p.

The BayesNode class has methods for calculating conditional probabilities and sampling from the distribution.

University: University of Peloponnese, Department of Informatics and Telecommunications

Course: Artificial Intelligence

Authors: 
- Giannopoulos Georgios
- Giannopoulos Ioannis
"""
import random
from typing import Dict, List, Tuple, Union
from probability_distribution.probdist import event_values

def probability(p: float) -> bool:
    """Return true with probability p."""
    return p > random.uniform(0.0, 1.0)

class BayesNode:
    """A conditional probability distribution for a boolean variable,
    P(X | parents). Part of a BayesNet."""

    def __init__(self, X: str, parents: Union[str, List[str]], cpt: Union[float, Dict[Union[bool, Tuple[bool, ...]], float]]):
        """X is a variable name, and parents a sequence of variable
        names or a space-separated string. cpt, the conditional
        probability table, takes one of these forms:

        * A number, the unconditional probability P(X=true). You can
          use this form when there are no parents.

        * A dict {v: p, ...}, the conditional probability distribution
          P(X=true | parent=v) = p. When there's just one parent.

        * A dict {(v1, v2, ...): p, ...}, the distribution P(X=true |
          parent1=v1, parent2=v2, ...) = p. Each key must have as many
          values as there are parents. You can use this form always;
          the first two are just conveniences.

        In all cases the probability of X being false is left implicit,
        since it follows from P(X=true).

        >>> X = BayesNode('X', '', 0.2)
        >>> Y = BayesNode('Y', 'P', {T: 0.2, F: 0.7})
        >>> Z = BayesNode('Z', 'P Q',
        ...    {(T, T): 0.2, (T, F): 0.3, (F, T): 0.5, (F, F): 0.7})
        """
        if isinstance(parents, str):
            parents = parents.split()

        # We store the table always in the third form above.
        if isinstance(cpt, (float, int)):  # no parents, 0-tuple
            cpt = {(): cpt}
        elif isinstance(cpt, dict):
            # one parent, 1-tuple
            if cpt and isinstance(list(cpt.keys())[0], bool):
                cpt = {(v,): p for v, p in cpt.items()}

        assert isinstance(cpt, dict)
        for vs, p in cpt.items():
            assert isinstance(vs, tuple) and len(vs) == len(parents)
            assert all(isinstance(v, bool) for v in vs)
            assert 0 <= p <= 1

        self.variable: str = X
        self.parents: List[str] = parents
        self.cpt: Dict[Tuple[bool, ...], float] = cpt
        self.children: List = []

    def p(self, value: bool, event: Dict[str, bool]) -> float:
        """Return the conditional probability
        P(X=value | parents=parent_values), where parent_values
        are the values of parents in event. (event must assign each
        parent a value.)
        >>> bn = BayesNode('X', 'Burglary', {T: 0.2, F: 0.625})
        >>> bn.p(False, {'Burglary': False, 'Earthquake': True})
        0.375"""
        assert isinstance(value, bool)
        ptrue = self.cpt[event_values(event, self.parents)]
        return ptrue if value else 1 - ptrue

    def sample(self, event: Dict[str, bool]) -> bool:
        """Sample from the distribution for this variable conditioned
        on event's values for parent_variables. That is, return True/False
        at random according with the conditional probability given the
        parents."""
        return probability(self.p(True, event))

    def __repr__(self) -> str:
        return repr((self.variable, ' '.join(self.parents)))