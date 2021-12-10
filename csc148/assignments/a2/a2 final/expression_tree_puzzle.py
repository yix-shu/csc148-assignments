"""
CSC148, Winter 2021
Assignment 2: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Jonathan Calver, Sophia Huynh,
         Maryam Majedi, and Jaisie Sin.

All of the files in this directory are:
Copyright (c) 2021 Diane Horton, Jonathan Calver, Sophia Huynh,
                   Maryam Majedi, and Jaisie Sin.

=== Module Description ===

This module contains the ExpressionTreePuzzle class.
"""

from __future__ import annotations

from typing import List, Dict

from expression_tree import ExprTree
from puzzle import Puzzle


class ExpressionTreePuzzle(Puzzle):
    """"
    An expression tree puzzle.

    === Public Attributes ===
    variables: the dictionary of variable name (str) - value (int) pairs
               A variable is considered "unassigned" unless it has a
               non-zero value.
    target: the target value for the expression tree to evaluate to

    === Private Attributes ===
    _tree: the expression tree

    === Representation Invariants ===
    - variables contains a key for each variable appearing in _tree

    - all values stored in variables are single digit integers (0-9).
    """
    _tree: ExprTree
    variables: Dict[str, int]
    target: int

    def __init__(self, tree: ExprTree, target: int) -> None:
        """
        Create a new expression tree puzzle given the provided
        expression tree and the target value. The variables are initialized
        using the tree's populate_lookup method.

        >>> puz = ExpressionTreePuzzle(ExprTree('a', []), 4)
        >>> puz.variables == {'a': 0}
        True
        >>> puz.target
        4
        """

        self.variables = {}
        tree.populate_lookup(self.variables)
        self._tree = tree
        self.target = target

    def is_solved(self) -> bool:
        """
        Return True iff ExpressionTreePuzzle self is solved.

        The puzzle is solved if all variables have been assigned a non-zero
        value and the expression tree evaluates to the target value.

        >>> exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
        >>> puz = ExpressionTreePuzzle(exp_t, 7)
        >>> puz.is_solved()
        False
        >>> puz.variables['a'] = 7
        >>> puz.is_solved()
        False
        >>> puz.variables['a'] = 5
        >>> puz.variables['b'] = 2
        >>> puz.is_solved()
        True
        """
        # Iterate through dictionary values and check for a 0 value.
        for key in self.variables:
            # If there is a 0 value, return False (by precondition).
            if self.variables[key] == 0:
                return False
        # Check if the tree evaluates to the target int, and return the bool.
        return self._tree.eval(self.variables) == self.target

    def __str__(self) -> str:
        """
        Return a string representation of this ExpressionTreePuzzle.

        The first line should show the dictionary of variables and the
        second line should show the string representation of the algebraic
        equation represented by the puzzle.

        >>> exprt = ExprTree('+', [ExprTree('*', \
                                            [ExprTree('a', []), \
                                             ExprTree('+', [ExprTree('b', []), \
                                                            ExprTree(6, []), \
                                                            ExprTree(6, []), \
                                                           ])]), \
                                   ExprTree(5, [])])
        >>> puz = ExpressionTreePuzzle(exprt, 61)
        >>> print(puz)
        {'a': 0, 'b': 0}
        ((a * (b + 6 + 6)) + 5) = 61
        """
        # Just f-stringing it up. Thankfully __str__ actually worked. :)
        return f'{self.variables}\n{self._tree} = {self.target}'

    def extensions(self) -> List[ExpressionTreePuzzle]:
        """
        Return the list of legal extensions of this ExpressionTreePuzzle.

        A legal extension is a new ExpressionTreePuzzle equal to this
        ExpressionTreePuzzle, except that it assigns a single currently
        unassigned variable a value in the range 1-9.

        A variable is "unassigned" if it has a value of 0.

        A copy of the expression tree and variables dictionary should be
        used in each extension made, so as to avoid unintended aliasing.

        >>> exp_t = ExprTree('a', [])
        >>> puz = ExpressionTreePuzzle(exp_t, 7)
        >>> exts_of_puz = puz.extensions()
        >>> len(exts_of_puz) == 9
        True
        >>> exts_of_an_ext = exts_of_puz[0].extensions()
        >>> len(exts_of_an_ext) == 0
        True
        >>> exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
        >>> puz = ExpressionTreePuzzle(exp_t, 8)
        >>> exts_of_puz = puz.extensions()
        >>> len(exts_of_puz) == 18
        True
        """
        # Create the return list, and a change-able variable list.
        final = []
        var_lst = []
        # Find all 0-valued keys, and save them. We will extend on these.
        for key in self.variables:
            if self.variables[key] == 0:
                var_lst.append(key)
        # Check if var_lst is empty. If it is, then every variable is already
        # assigned, so we can just return an empty list.
        if not var_lst:
            return []
        # This runs the whole show. Loop 9 times for each unassigned variable.
        for v in var_lst:
            for k in range(1, 10):
                # Create a copy of variables and mutate it to show updated var.
                variables_copy = self.variables.copy()
                variables_copy[v] = k
                # Create a copy of the tree and substitute the required var.
                tree_copy = self._tree.copy()
                tree_copy.substitute(variables_copy)
                # Create a puzzle with modified tree copy and same target.
                puzzle = ExpressionTreePuzzle(tree_copy, self.target)
                # Update puzzle's variable list by assigning it the copy.
                puzzle.variables = variables_copy
                # Finally, append puzzle to the return list.
                final.append(puzzle)
        return final

    # The specifics of how you implement this are up to you.
    # Hint 1: remember that a puzzle can only be extended by assigning a value
    #         to an unassigned variable.
    # Hint 2: remember that our expression tree only supports addition,
    #         multiplication, and non-negative integers.
    def fail_fast(self) -> bool:
        """
        Return True if this ExpressionTreePuzzle can be quickly determined to
        have no solution, False otherwise.

        """
        # Check if there is a value in <variables> that is greater than the
        # target. If so, then the tree is unsolvable due to the reasoning below.
        for key1 in self.variables:
            if self.variables[key1] > self.target:
                return True
        # If the tree evaluates to more than the target, it cannot be reduced
        # by addition or multiplication since all numbers are positive integers.
        if self._tree.eval(self.variables) > self.target:
            return True
        # Else, if the tree evaluates to less than the target, and there is an
        # unassigned variable in variables, then there could be a solution.
        elif self._tree.eval(self.variables) < self.target:
            if 0 in [self.variables[key2] for key2 in self.variables]:
                return False
            # If there are no unassigned variables, then a solution cannot
            # possibly exist, so it does indeed fail_fast. :)
            else:
                return True
        # Return False, because we checked the surface-level cases, and now
        # we will rely on the solvers.
        return False


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={'pyta-reporter': 'ColorReporter',
                                'allowed-io': [],
                                'allowed-import-modules': ['doctest',
                                                           'python_ta',
                                                           'typing',
                                                           '__future__',
                                                           'expression_tree',
                                                           'puzzle'],
                                'disable': ['E1136'],
                                'max-attributes': 15}
                        )
