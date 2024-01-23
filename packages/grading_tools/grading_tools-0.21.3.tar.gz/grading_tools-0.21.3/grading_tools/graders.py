"""The ``graders`` module contains all the grader classes."""

import pprint
import random
import re
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass
from math import isclose, isnan
from typing import Literal, Union

import markdown
import matplotlib
import numpy as np
import pandas as pd
from PIL import Image
from PIL.PngImagePlugin import PngImageFile
from rapidfuzz import fuzz
from scipy import ndimage
from sklearn.base import is_classifier, is_regressor
from sklearn.exceptions import NotFittedError
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.pipeline import Pipeline
from sklearn.utils.validation import check_is_fitted

from .feedback.english import Feedback


class BaseGrader(object):
    """
    Base class for all graders.

    Attributes
    ----------
    submission :
        Student's submission object.
    answer :
        Correct answer object.
    points : int or float, default=1
        Total point value awarded if submission is correct.
    score : int or float, default=0
        Student's current ``score``. Default is ``0`` because submission has yet to
        be graded.
    passed : bool
        Whether student's ``score`` is equal to or greater than possible ``points``.
        Default is ``False`` because submission has yet to be graded.
    comment : str
        Feedback one student's submission. Default is empty string because
        submission has yet to be graded. Note that you can use
        [Markdown syntax](https://daringfireball.net/projects/markdown/).

    """

    def __init__(
        self, submission, answer, points=1, score=0, passed=False, comment=""
    ):
        self.answer = answer
        self.comment = comment
        self.passed = passed
        self.points = points
        self.score = score
        self.submission = submission

        if not isinstance(
            self.submission, type(self.answer)
        ) and not isinstance(self.submission, tempfile._TemporaryFileWrapper):
            raise TypeError(
                f"Your submission needs to be type {type(self.answer).__name__}, "
                f"not type {type(self.submission).__name__}."
            )

    def __repr__(self) -> str:
        """Pretty dictionary representation of grader object."""
        rep_dict = {
            "points": self.points,
            "submission dtype": type(self.submission),
            "answer dtype": type(self.answer),
            "current score": self.score,
            "passed": self.passed,
            "comment": self.comment,
        }

        return pprint.pformat(rep_dict, indent=2, sort_dicts=False)

    def positive_comment(self) -> None:
        """Generate positive comment.

        Assigns a randomly-chosen comment to the ``comment`` attribute of grader object.

        Returns
        -------
        None

        """
        comments = [
            "🥳",
            "Awesome work.",
            "Boom! You got it.",
            "Correct.",
            "Excellent work.",
            "Excellent! Keep going.",
            "Good work!",
            "Party time! 🎉🎉🎉",
            "Python master 😁",
            "Yes! Keep on rockin'. 🎸" "That's right.",
            "That's the right answer. Keep it up!",
            "Very impressive.",
            "Way to go!",
            "Wow, you're making great progress.",
            "Yes! Great problem solving.",
            "Yes! Your hard work is paying off.",
            "You = coding 🥷",
            "You got it. Dance party time! 🕺💃🕺💃",
            "You're making this look easy. 😉",
            "Yup. You got it.",
        ]

        self.comment = random.choice(comments)

    def add_to_score(self, points=1) -> None:
        """Increment score.

        This method adds points to grader's `score` attribute, then checks if `score`
        meets `points` theshold. If threshold met, a positive comment is added to
        `comment` attribute.

        Parameters
        ----------
        points : int or float, default=1
            Number of points to add to `score` attribute.

        Returns
        -------
        None

        """
        self.score += points
        self.passed = self.score >= self.points
        if self.passed:
            self.positive_comment()

    def update_comment(self, new_comment, *args):
        """Change grader ``comment``.

        Parameters
        ----------
        new_comment : str
            Text of new comment. Note that you can use
            [Markdown syntax](https://daringfireball.net/projects/markdown/).

        *args : str
            Additional comments to add to ``new_comment`` string. This allows you to
            break up long strings into multiple args for pretty formatting. :)

        """
        new_comment = " ".join([new_comment] + list(args))
        self.comment = new_comment

    def return_feedback(self, html=True) -> dict:
        """Return feedback to student.

        Parameters
        ----------
        html : bool, default=True
            If ``True`` converts comment text to HTML. This is only important is you
            the comment has been written using
            [Markdown syntax](https://daringfireball.net/projects/markdown/).

        Returns
        -------
        feedback_dict : dict
            Dictionary has three keys:
            ``{"score": self.score, "passed": self.passed, "comment": comment}``

        """
        if html:
            comment = markdown.markdown(self.comment)
        else:
            comment = self.comment
        feedback_dict = {
            "score": self.score,
            "passed": self.passed,
            "comment": comment,
        }

        if hasattr(self, "diff_path"):
            feedback_dict["image"] = self.diff_path

        return feedback_dict


class PythonGrader(BaseGrader):
    """Evaluate data types from the Python standard library."""

    def __init__(self, submission, answer, points=1):
        super().__init__(submission, answer, points)

    def grade_list(self, match_order=True, tolerance=0.0, return_bool=False):
        """Evaluate student's submitted list.

        Evaluate whether ``submission`` list matches ``answer``. Depending on parameter
        settings, submission can be in different order, and there is tolerance if
        numerical items don't exactly match answer. Note that, in most cases, you
        will have to allow for some tolerance when a submission has floating-point
        numbers.

        Parameters
        ----------
        match_order : bool, default=True
            Do the items in the submitted list need to be in the same order as those in
            the answer list?

        tolerance : float, default=0.0
            What is the maximum allowed difference between
            ``submission`` and ``answer``? For example, if ``tolerance=0.0``, values
            must be identical. With numerical items, for example, a ``tolerance=0.1``
            means values must be within 10% of each other (relative to the larger absolute
            value of the two). Uses `math.isclose() <https://docs.python.org/3/library/math.html#math.isclose>`_.
            For strings, uses the normalized Indel distance from `rapidfuzz https://maxbachmann.github.io/RapidFuzz/Usage/fuzz.html`_.

        return_bool : bool, default=False
            Whether to return ``self.passed`` once grading is complete. You'll need this if
            you want to design your own grading workflow beyond the default.

        Examples
        --------
        If values must match, but order isn't important.

        >>> g = PythonGrader(submission=[1, 0], answer=[0, 1])
        >>> g.grade_list(match_order=False, tolerance=0.0, return_bool=True)
        True

        If order must match, and numerical values must be exact match.

        >>> g = PythonGrader(submission=[1.1, 2.2], answer=[1, 2])
        >>> g.grade_list(match_order=True, tolerance=0.0, return_bool=True)
        False

        If order must match, but numerical values don't need to be exact match.

        >>> g = PythonGrader(submission=[1.1, 2.2], answer=[1, 2])
        >>> g.grade_list(match_order=True, tolerance=0.1, return_bool=True)
        True

        """
        if not isinstance(self.submission, list):
            raise TypeError(
                f"grade_list method can only be used with list submissions, not {type(self.submission).__name__}."
            )

        if len(self.submission) != len(self.answer):
            self.update_comment(
                f"Your submission should have `{len(self.answer)}` items, not `{len(self.submission)}`."
            )
            return

        if match_order is False:
            # For dealing with records
            if isinstance(self.submission[0], dict):
                sort_key = list(self.submission[0].keys())[0]
                self.submission.sort(key=lambda x: x[sort_key])
                self.answer.sort(key=lambda x: x[sort_key])
            else:
                self.submission.sort()
                self.answer.sort()

        if not tolerance and self.submission == self.answer:
            self.add_to_score()

        # If tolerance is included and list items match dtypes with each other
        if tolerance:
            for a, b in zip(self.submission, self.answer):
                # Check numbers using relative tolerance
                if (
                    isinstance(a, (float, int))
                    and isinstance(b, (float, int))
                    and isclose(a, b, rel_tol=tolerance)
                ):
                    pass
                # Check strings using Levenshtein distance
                elif (
                    (isinstance(a, str))
                    and (isinstance(b, str))
                    and (1 - fuzz.ratio(a, b) / 100 < tolerance)
                ):
                    pass
                # Return fail at first mismatch
                else:
                    self.update_comment(
                        f"Your list contains the item `{a}`, which doesn't match the expected result."
                    )
                    if return_bool:
                        return self.passed
                    else:
                        return
            self.add_to_score()

        if return_bool:
            return self.passed
        else:
            return

    def grade_dict(self, tolerance=0.0, return_bool=False):
        """Evaluate student's submitted dict.

        Evaluate whether ``submission`` dict matches ``answer``. Depending on parameter
        settings, there is tolerance if numerical items don't exactly match answer.
        Note that, in most cases, you will have to allow for some tolerance when a
        submission has floating-point numbers.

        Parameters
        ----------
        tolerance : float, default=0.0
            For numerical values (not keys, just values), what is the maximum allowed
            difference between ``submission`` and ``answer``? If ``tolerance=0.1``, values must be
            identical. If ``tolerance=0.1``, values must be within 10% of each
            other (relative to the larger absolute value of the two). Uses
            `math.isclose() <https://docs.python.org/3/library/math.html#math.isclose>`_.

        return_bool : bool, default=False
            Whether to return ``self.passed`` once grading is complete. You'll need this if
            you want to design your own grading workflow beyond the default.

        Examples
        --------
        Check if dictionaries match. (Note that key order doesn't matter for
        dictionaries in Python 3.9.)

        >>> g = PythonGrader(submission={"a": 1, "b": 2}, answer={"a": 1, "b": 2})
        >>> g.grade_dict(tolerance=0.0, return_bool=True)
        True

        Check if dictionaries match, allowing for approximate value matches.

        >>> g = PythonGrader(submission={"a": 1, "b": 2.2}, answer={"a": 1, "b": 2})
        >>> g.grade_dict(tolerance=0.1, return_bool=True)
        True

        When submission keys don't match answer, grader alerts student.

        >>> g = PythonGrader(submission={"a": 1, "z": 2}, answer={"a": 1, "b": 2})
        >>> g.grade_dict(tolerance=0.0, return_bool=False)
        >>> print(g.comment)
        One or more of the keys in your dictionary doesn't match the expected result.

        When submission keys match answer but values don't, grader tells student which
        key-value pair is wrong.

        >>> g = PythonGrader(submission={"a": 1, "b": 2.2}, answer={"a": 1, "b": 2})
        >>> g.grade_dict(tolerance=0.0, return_bool=False)
        >>> print(g.comment)
        The value for key `b` doesn't match the expected result.

        """
        if not isinstance(self.submission, dict):
            raise TypeError(
                f"grade_dict method can only be used with dict submissions, not {type(self.submission).__name__}."
            )

        # Exact match, give point and done
        if self.submission == self.answer:
            self.add_to_score()
            if return_bool:
                return self.passed
            else:
                return

        # Is it the keys that don't match?
        if self.submission.keys() != self.answer.keys():
            self.update_comment(
                "One or more of the keys in your dictionary doesn't match the expected result."
            )
            if return_bool:
                return self.passed
            else:
                return

        # If keys match, iteratate through keys and check values
        for k in self.submission.keys():
            # Flag set to True when vals don't match or not w/in tolerance
            break_flag = False
            sub = self.submission[k]
            ans = self.answer[k]
            sub_is_num = isinstance(sub, (int, float))
            key_val_comment = f"The value for the key `{k}` doesn't match the expected result."

            # For numerical values
            if sub_is_num and sub != ans:
                if isnan(sub) and isnan(ans):
                    self.passed = True
                elif (tolerance > 0) and isclose(sub, ans, rel_tol=tolerance):
                    # This will continue to be True as long as all vals are w/in tolerance
                    self.passed = True
                else:
                    self.update_comment(key_val_comment)
                    self.passed = False
                    break_flag = True

            # For non-numerical values
            if not sub_is_num and sub != ans:
                self.update_comment(key_val_comment)
                self.passed = False
                break_flag = True

            if break_flag:
                break

        # If submission got through loop with self.passed==True, all vals are w/in tolerance
        if self.passed:
            self.add_to_score()

        if return_bool:
            return self.passed
        else:
            return

    def grade_number(self, tolerance=0, return_bool=False):
        """Evaluate student's submitted number (int or float).

        Parameters
        ----------
        tolerance: int or float, default=0.0
            For numerical values, what is the maximum allowed
            difference between ``submission`` and ``answer``? If ``tolerance=0.1``, values must be
            identical. If ``tolerance=0.1``, values must be within 10% of each
            other (relative to the larger absolute value of the two).

        return_bool : bool, default=False
            Whether to return ``self.passed`` once grading is complete. You'll need this if
            you want to design your own grading workflow beyond the default.
        """
        if not isclose(self.submission, self.answer, rel_tol=tolerance):
            self.update_comment(
                f"Your submission `{self.submission}` doesn't match the expected result."
            )
            return False if return_bool else self.return_feedback()

        self.add_to_score()
        return True if return_bool else self.return_feedback()

    def grade_bool(self, return_bool=False):
        """Evaluate student's submitted number (int or float).

        Parameters
        ----------
        return_bool : bool, default=False
            Whether to return ``self.passed`` once grading is complete. You'll need this if
            you want to design your own grading workflow beyond the default.
        """
        if self.submission != self.answer:
            self.update_comment(
                f"Your submission `{self.submission}` doesn't match the expected result."
            )
            return False if return_bool else self.return_feedback()

        self.add_to_score()
        return True if return_bool else self.return_feedback()

    def grade_string(
        self, ignore_case=False, contains=None, return_bool=False
    ):
        """Evaluate student's submitted string.

        By default, evaluates for an exact match. If ``contains`` is specified, method
        will only match for that term (or terms).

        Parameters
        ----------
        ignore_case: bool, default=False
            Whether or not to ignore case when evaluating submission.

        contains: str or list, default=None
            If ``None``, submission will be evaluated for an exact match. If ``str``,
            will only match that substring. If ``list``, will match all items.

        return_bool : bool, default=False
            Whether to return ``self.passed`` once grading is complete. You'll need this if
            you want to design your own grading workflow beyond the default.

        Examples
        --------
        >>> g = PythonGrader(submission="Hello world", answer="Hello world")
        >>> g.grade_string(ignore_case=False, return_bool=True)
        True

        >>> g = PythonGrader(submission="Hello world", answer="")
        >>> g.grade_string(contains="WORLD", ignore_case=True, return_bool=True)
        True

        Note that when you specify ``contains``, the answer can be an empty string.

        >>> g = PythonGrader(submission="Hello world", answer="")
        >>> g.grade_string(contains=["Hello", "monkey"], ignore_case=False, return_bool=True)
        False
        >>> print(g.comment)
        Your submission is missing an important term: `'monkey'`.

        """
        if not isinstance(self.submission, str):
            raise TypeError(
                f"grade_string method can only be used with str submissions, not {type(self.submission).__name__}."
            )

        if ignore_case:
            self.submission = self.submission.lower()
            self.answer = self.answer.lower()
            if isinstance(contains, str):
                contains = contains.lower()
            if isinstance(contains, Iterable):
                contains = [str(s).lower() for s in list(contains)]

        if (not contains) and (self.submission != self.answer):
            self.update_comment(
                "Your submission doesn't match the expected result"
            )
            return False if return_bool else self.return_feedback()

        if (isinstance(contains, str)) and contains not in self.submission:
            self.update_comment(
                f"Your submission is missing an important term: `'{contains}'`."
            )
            return False if return_bool else self.return_feedback()

        if isinstance(contains, Iterable):
            for s in list(contains):
                if str(s) not in self.submission:
                    self.update_comment(
                        f"Your submission is missing an important term: `'{s}'`."
                    )
                    return False if return_bool else self.return_feedback()

        self.add_to_score()
        return True if return_bool else self.return_feedback()


class PandasGrader(BaseGrader):
    """Grader for evaluating objects from `pandas <https://pandas.pydata.org/docs/index.html>`_. library."""

    def __init__(self, submission, answer, points=1):
        super().__init__(submission, answer, points)

    # https://tinyurl.com/y3sg2umv
    @staticmethod
    def _clean_assert_message(message: AssertionError) -> str:
        """Make feedback student-friendly.

        Helper function used by ``grade_df`` and ``grade_series``.
        """
        message = str(message)
        s = ""

        if "DataFrame" in message:
            if 'Attribute "names"' in message:
                s = "The index name of your DataFrame doesn't"
            elif "index values" in message:
                s = "The index values of your DataFrame don't"
            elif "index classes" in message:
                s = "The class type of your DataFrame index doesn't"
            # These last two clauses look wrong, but they're right
            elif "columns values" in message:
                s = "The column names of your DataFrame don't"
            elif "column name" in message:
                p = re.compile(r'name=(".+?")')
                col = p.search(message).group(1)
                s = f"The values in the `{col}` column in your DataFrame don't"

        if "Series.index" in message:
            if 'Attribute "names"' in message:
                s = "The index name of your Series doesn't"
            elif "index values" in message:
                s = "The index values of your Series don't"
            elif "dtype" in message:
                s = "The dtype of your Series index doesn't"

        if message.startswith("Series are"):
            if 'Attribute "name"' in message:
                s = "The name of your Series doesn't"
            if "Series values" in message:
                s = "The values in your Series don't"

        if s == "":
            raise ValueError(
                "Pandas Assertion error doesn't have parseable text."
            )

        return s + " match the expected result."

    def grade_df(
        self,
        sort_values_by=None,
        match_index=True,
        match_index_col_order=False,
        match_colnames_only=False,
        tolerance=0.01,
        return_bool=False,
    ):
        """Evaluate submitted DataFrame.

        Parameters
        ----------
        sort_values_by : str, list, default=None
            If specified, submission and answer will be sorted by that column (or list
            of columns) before evaluation. If ``"all_cols"``, DataFrame will be sorted
            by a list of all columns (ordered alphabetically).

        match_index : bool, default=True
            Whether or not to consider the index of the submitted DataFrame. If
            ``False``, index is reset before it's evaluated.

        match_index_col_order : bool, default=False
            Whether or not to consider the order of the index and columns in the
            submitted DataFrame.

        match_colnames_only : bool, default=False
            If ``True`` only column names will be evaluated, not index labels or
            DataFrame values. Note that the index and column order will always be ignored.

        tolerance: int or float, default=0.01
            For numerical values, what is the maximum allowed
            difference between ``submission`` and ``answer``? If ``tolerance=0.1``, values must be
            identical. If ``tolerance=0.1``, values must be within 10% of each
            other (relative to the larger absolute value of the two).

        return_bool : bool, default=False
            Whether to return ``self.passed`` once grading is complete. You'll need this if
            you want to design your own grading workflow beyond the default.

        Examples
        --------
        Here are two DataFrames. The first ``ans_df`` is the expected answer, and the second
        ``sub_df`` is the student submission. Note that both have the same values, but order of the
        indices and columns is different.

        >>> import pandas as pd
        >>> ans_df = pd.DataFrame(
        ...     {"city": ["Puhi", "Napa", "Derby"], "pop": [3, 79, 13]}, index=[16, 14, 4]
        ... )
        >>> sub_df = pd.DataFrame(
        ...     {"pop": [79, 3, 13], "city": ["Napa", "Puhi", "Derby"]}, index=[14, 16, 4]
        ... )
        >>> print(ans_df)
             city  pop
        16   Puhi    3
        14   Napa   79
        4   Derby   13
        >>> print(sub_df)
            pop   city
        14   79   Napa
        16    3   Puhi
        4    13  Derby
        >>> g = PandasGrader(submission=sub_df, answer=ans_df)
        >>> g.grade_df(match_index_col_order=False, return_bool=True)
        True
        >>> g.grade_df(match_index_col_order=True, return_bool=True)
        False
        >>> print(g.comment)
        DataFrame.index are different
        DataFrame.index values are different (66.66667 %)
        [submission]:  Int64Index([14, 16, 4], dtype='int64')
        [answer]: Int64Index([16, 14, 4], dtype='int64')
        """
        if not isinstance(self.submission, pd.DataFrame):
            raise TypeError(
                f"grade_df method can only be used with DataFrames submissions, not {type(self.submission).__name__}."
            )

        if sort_values_by:
            try:
                if sort_values_by == "all_cols":
                    # Sorts df cols alphabetically and then sorts rows by all cols
                    self.submission = self.submission.sort_index(axis=1)
                    self.submission = self.submission.sort_values(
                        by=self.submission.columns.tolist(), axis=0
                    )
                    self.answer = self.answer.sort_index(axis=1)
                    self.answer = self.answer.sort_values(
                        by=self.answer.columns.tolist(), axis=0
                    )
                else:
                    self.submission.sort_values(sort_values_by, inplace=True)
                    self.answer.sort_values(sort_values_by, inplace=True)
            except KeyError:
                raise KeyError(
                    f"Either the submission or answer does not have column(s) {sort_values_by}."
                )

        if not match_index:
            self.submission = self.submission.reset_index(drop=True)
            self.answer = self.answer.reset_index(drop=True)

        if match_colnames_only:
            for c in self.answer.columns:
                if c not in self.submission.columns:
                    self.update_comment(
                        f"Your submission is missing a `'{c}'` column."
                    )
                    return False if return_bool else self.return_feedback()
            self.add_to_score()
            return True if return_bool else self.return_feedback()

        # Check shape
        if self.submission.shape != self.answer.shape:
            self.update_comment(
                f"The shape of your {type(self.submission).__name__} should be `{self.answer.shape}`,"
                f"not `{self.submission.shape}`."
            )
            if return_bool:
                return self.passed
            else:
                return None

        try:
            pd.testing.assert_frame_equal(
                self.submission,
                self.answer,
                check_like=not match_index_col_order,
                check_exact=not bool(tolerance),
                rtol=tolerance,
            )
            self.add_to_score()
            if return_bool:
                return self.passed
            else:
                return None

        except AssertionError as e:
            comment = self._clean_assert_message(e)
            self.update_comment(comment)
            if return_bool:
                return self.passed
            else:
                return None

    def grade_series(
        self,
        match_index=True,
        match_index_order=False,
        sort_values=False,
        match_names=True,
        tolerance=0.01,
        return_bool=False,
    ):
        """Evaluate submitted Series.

        Parameters
        ----------
        match_index : bool, default=True
            Whether to consider the submission's index when evaluating against
            answer.

        match_index_order : bool, default=False
            Whether to consider the submission's index order when evaluating
            against answer. If ``False``, both submission and answer are sorted
            ascending.

        sort_values : bool, default=False
            If true, submission and answer will be sorted ascending before being
            compared. This will override any option for ``match_index_order``.

        match_names : bool, default=True
            Whether to consider the submission's Series and Index names attributes.

        tolerance : int or float, default=0.01
            For numerical values, what is the maximum allowed
            difference between ``submission`` and ``answer``? If ``tolerance=0.0``,
            values must be identical. If ``tolerance=0.1``, values must be within 10%
            of each other (relative to the larger absolute value of the two).

        return_bool : bool, default=False
            Whether to return ``self.passed`` once grading is complete. You'll need
            this if you want to design your own grading workflow beyond the default.

        Examples
        --------
        >>> from grading_tools.graders import PandasGrader
        >>> import pandas as pd

        Let's create two Series: the ``ans`` and the ``sub``. The latter is in a
        different order, has a different name; its values are close to the answer but
        not exactly the same.

        >>> ans = pd.Series([10, 20, 30], name="pop", index=[1, 2, 3])
        >>> ans
        1    10
        2    20
        3    30
        Name: pop, dtype: int64
        >>> sub = pd.Series([22, 11, 33], name="wrong_name", index=[2, 1, 3])
        >>> sub
        2    22
        1    11
        3    33
        Name: wrong_name, dtype: int64

        If the Series are put into a ``PandasGrader`` and then ``grade_series`` is
        used with default arguments, the submission is evaluated as ``False``, and an
        informative comment is created.

        >>> g = PandasGrader(submission=sub, answer=ans)
        >>> g.grade_series(
        ...     match_index=True,
        ...     match_index_order=True,
        ...     match_names=True,
        ...     tolerance=0.0,
        ...     return_bool=True,
        ... )
        False
        >>> print(g.comment)
        The values in your Series don't match the expected result.

        If we add tolerance and remove requirements for index order and name
        matching, the submission is evaluated at passing.

        >>> g.grade_series(
        ...     match_index=True,
        ...     match_index_order=False,
        ...     match_names=False,
        ...     tolerance=0.1,
        ...     return_bool=True,
        ... )
        True
        >>> print(g.comment)
        Python master 😁

        """
        if not isinstance(self.submission, pd.Series):
            raise TypeError(
                f"grade_series method can only be used with Series submissions, not {type(self.submission).__name__}."
            )

        if not match_index_order:
            self.submission = self.submission.sort_index()
            self.answer = self.answer.sort_index()

        if sort_values:
            self.submission = self.submission.sort_values()
            self.answer = self.answer.sort_values()

        # Check shape
        if self.submission.shape != self.answer.shape:
            self.update_comment(
                f"The shape of your Series should be `{self.answer.shape}`,"
                f"not `{self.submission.shape}`."
            )
            if return_bool:
                return self.passed
            else:
                return None

        try:
            pd.testing.assert_series_equal(
                self.submission,
                self.answer,
                check_index=match_index,
                check_names=match_names,
                check_exact=not bool(tolerance),
                rtol=tolerance,
            )
            self.add_to_score()
            if return_bool:
                return self.passed
            else:
                return None
        except AssertionError as e:
            comment = self._clean_assert_message(e)
            self.update_comment(comment)
            if return_bool:
                return self.passed
            else:
                return None


class SklearnGrader(BaseGrader):
    """Grader for evaluating objects from `sckit-learn <https://scikit-learn.org/stable/>`_."""

    def __init__(self, submission, answer, points=1):
        super().__init__(submission, answer, points)

    def grade_model_params(
        self,
        match_steps=False,
        match_hyperparameters=False,
        prune_hyperparameters=False,
        match_fitted=True,
        tolerance=0.0,
        return_bool=False,
    ):
        """Evaluate model parameters.

        Parameters
        ----------
        match_steps : bool, default=False
            For models that are type `sklearn.pipeline.Pipeline <https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html>`_.
            Whether to consider the steps of a Pipeline when evaluating submission.

        match_hyperparameters : bool, default=False
            Whether to consider the hyper parameter values when evaluating submission.

        prune_hyperparameters : bool, default=False
            When you pull hyperparameters out a a model, it can be a seriously messy
            dictionary, especially if there's some sort of encoder mapping. So when you
            set ``match_hyperparameters`` to ``True``, save yourself a headache and set
            this to ``True``, too.

        match_fitted : bool, default=True
            Whether to consider if the submission has or has not been fitted to
            training data.

        tolerance : int or float, default=0.0
            For numerical hyperparameter values, what is the maximum allowed
            difference between ``submission`` and ``answer``? If ``tolerance=0.0``,
            values must be identical. If ``tolerance=0.1``, values must be within 10%
            of each other (relative to the larger absolute value of the two).

        return_bool : bool, default=False
            Whether to return ``self.passed`` once grading is complete. You'll need this if
            you want to design your own grading workflow beyond the default.

        Examples
        --------
        Let's create two linear models that use different scalers. We'll then fit only
        the answer model to the California housing dataset.

        >>> from sklearn.datasets import fetch_california_housing
        >>> from sklearn.linear_model import LinearRegression
        >>> from sklearn.pipeline import make_pipeline
        >>> from sklearn.preprocessing import MinMaxScaler, StandardScaler
        >>> X, y = fetch_california_housing(return_X_y=True, as_frame=True)
        >>> sub_model = make_pipeline(MinMaxScaler(), LinearRegression())
        >>> ans_model = make_pipeline(StandardScaler(), LinearRegression())
        >>> ans_model.fit(X, y)
        Pipeline(steps=[('standardscaler', StandardScaler()),
                        ('linearregression', LinearRegression())])

        Next, we'll grade the submission.

        >>> from grading_tools.graders import SklearnGrader
        >>> g = SklearnGrader(sub_model, ans_model)
        >>> g.grade_model_params(return_bool=True)
        False
        >>> g.comment
        "Your model hasn't been trained. Fit it to the training data and resubmit it."

        If we train and re-grade the model, it passes.

        >>> sub_model.fit(X, y)
        Pipeline(steps=[('minmaxscaler', MinMaxScaler()),
                        ('linearregression', LinearRegression())])
        >>> g.grade_model_params(return_bool=True)
        True
        >>> g.comment
        'Good work!'

        Finally, if we re-grade the model, requiring that the steps match,
        the submission fails.

        >>> g.grade_model_params(match_steps=True, return_bool=True)
        False
        >>> g.comment
        "Step 1 in your model Pipeline doesn't match the expected result.
        Expected: `StandardScaler`. Received: `MinMaxScaler`."
        """
        # Is the answer model fitted?
        try:
            check_is_fitted(self.answer)
            ans_fitted = True
        except NotFittedError:
            ans_fitted = False

        if match_fitted and not ans_fitted:
            raise NotFittedError(
                "`match_fitted` cannot be set to `True` if answer model is not fitted."
            )

        # Do we need to check if the submission is fitted?
        if match_fitted and ans_fitted:
            try:
                check_is_fitted(self.submission)
            except NotFittedError:
                self.update_comment(
                    "Your model hasn't been trained. Fit it to the training data and resubmit it."
                )
                if return_bool:
                    return False
                else:
                    return

        # Is the model a pipeline (rather than just an estimator)?
        if isinstance(self.answer, Pipeline):
            is_pipeline = True
        else:
            is_pipeline = False

        if match_steps and not is_pipeline:
            raise ValueError(
                f"`match_steps` can only be `True` when answer Pipeline, not {type(self.answer).__name__}."
            )
        # Checking steps in pipeline models
        if match_steps and is_pipeline:
            sub_steps = [s for s in self.submission]
            ans_steps = [s for s in self.answer]

            # Wrong number of steps
            if len(sub_steps) != len(ans_steps):
                self.update_comment(
                    f"Your model Pipeline should have {len(ans_steps)} steps,",
                    f"not {len(sub_steps)}.",
                )
                if return_bool:
                    return False
                else:
                    return None

            # Wrong type of steps
            for idx, (sub, ans) in enumerate(
                zip(sub_steps, ans_steps), start=1
            ):
                if not isinstance(sub, type(ans)):
                    self.update_comment(
                        f"Step {idx} in your model Pipeline doesn't match the expected",
                        f"result. Expected: `{type(ans).__name__}`. Received:",
                        f"`{type(sub).__name__}`.",
                    )
                    if return_bool:
                        return False
                    else:
                        return None

        if match_hyperparameters:
            sub_params = self.submission.get_params()
            ans_params = self.answer.get_params()

            if prune_hyperparameters:
                sub_params = {
                    k: v
                    for k, v in sub_params.items()
                    if isinstance(v, (str, bool, float, int))
                }
                ans_params = {
                    k: v
                    for k, v in ans_params.items()
                    if isinstance(v, (str, bool, float, int))
                }

            g = PythonGrader(submission=sub_params, answer=ans_params)
            if not g.grade_dict(
                tolerance=tolerance,
                return_bool=True,
            ):
                self.update_comment(g.comment.replace("key", "hyperparameter"))
                if return_bool:
                    return False
                else:
                    return None

        self.add_to_score()
        if return_bool:
            return True
        else:
            return None

    def grade_model_performance(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        metric: str,
        round_to=3,
        tolerance=0.0,
        return_bool=False,
    ):
        """Evaluate model's performance using the model itself.

        Parameters
        ----------
        X_test: pd.DataFrame
            The test data feature matrix.

        y_test: pd.Series
            The test data target vector.

        metric: str {"accuracy_score", "precision_score", "recall_score", "f1_score", "r2_score", "mean_absolute_error", "mean_squared_error"}
            Metric to use when evaluating model performance.

        round_to: int, default=3
            Number of decimal places to round metric to before comparing
            submission and answer model performance.

        tolerance : int or float, default=0.0
            What is the maximum allowed difference between submission and answer
            model performance. If ``tolerance=0.0``, submission and answer metrics
            must be identical. If ``tolerance=0.1``, values must be within 10%
            of each other (relative to the larger absolute value of the two).

        return_bool : bool, default=False
            Whether to return ``self.passed`` once grading is complete. You'll need this if
            you want to design your own grading workflow beyond the default.

        Examples
        --------
        Let's start by creating a dataset, and splitting it into train and test.

        >>> from sklearn.datasets import fetch_california_housing
        >>> from sklearn.dummy import DummyRegressor
        >>> from sklearn.model_selection import train_test_split
        >>> X, y = fetch_california_housing(return_X_y=True, as_frame=True)
        >>> X_train, X_test, y_train, y_test = train_test_split(
        ...     X, y, test_size=0.2, random_state=42
        ... )

        Next, we create an answer and submission model, and put them into a grader.

        >>> ans = DummyRegressor(strategy="constant", constant=2).fit(X_train, y_train)
        >>> sub = DummyRegressor(strategy="constant", constant=1).fit(X_train, y_train)
        >>> g = SklearnGrader(sub, ans)

        Finally, we grade model performance looking at MSE.

        >>> g.grade_model_performance(
        ...     X_test=X_test,
        ...     y_test=y_test,
        ...     metric="mean_absolute_error",
        ...     return_bool=True,
        ... )
        False
        >>> print(g.comment)
        Your model's mean absolute error is `1.141`. You can do better. Try to
        beat `0.893`.

        If we allow for some tolerance, the model will pass.

        >>> g.grade_model_performance(
        ...     X_test=X_test,
        ...     y_test=y_test,
        ...     metric="mean_absolute_error",
        ...     tolerance=0.5,
        ...     return_bool=True,
        ... )
        True
        >>> print(g.comment)
        Your model's mean absolute error is `1.141`. Very impressive.

        """
        if not isinstance(X_test, pd.DataFrame):
            raise AttributeError(
                f"X_test must be a DataFrame, not {type(X_test)}."
            )

        if not isinstance(y_test, pd.Series):
            raise AttributeError(
                f"y_test must be a Series, not {type(y_test)}."
            )
        # Whether submission model outperforms answer
        sub_beats_ans = False

        # Grouping metrics into scores (higher is better) or errors (lower is better)
        score_metrics = [
            "accuracy_score",
            "precision_score",
            "recall_score",
            "f1_score",
            "r2_score",
        ]
        error_metrics = ["mean_absolute_error", "mean_squared_error"]

        if metric not in score_metrics + error_metrics:
            raise ValueError(
                f"'{metric}' is not a valid argument for `metric`. "
                f"Your options are {score_metrics + error_metrics}."
            )

        try:
            check_is_fitted(self.submission)
        except NotFittedError:
            self.update_comment(
                "In order to evaluate your model, it needs to be fitted to the "
                "training data first."
            )
            if return_bool:
                return False
            else:
                return None

        # Check that you use regression metrics for regression models
        if (metric in error_metrics + ["r2_score"]) and not is_regressor(
            self.submission
        ):
            raise ValueError(
                f"The metric {metric} can only be used to evaluate regression models."
            )

        # Check that you use classification metrics for classification models
        if metric in score_metrics[:-1] and not is_classifier(self.submission):
            raise ValueError(
                f"The metric {metric} can only be used to evaluate classification "
                "models."
            )

        # Generate submission and answer model predictions
        y_pred_sub = self.submission.predict(X_test)
        y_pred_ans = self.answer.predict(X_test)

        # Calculate training metrics for submission and answer
        if metric == "mean_absolute_error":
            sub_score = round(
                mean_absolute_error(y_test, y_pred_sub), round_to
            )
            ans_score = round(
                mean_absolute_error(y_test, y_pred_ans), round_to
            )

        if metric == "mean_squared_error":
            sub_score = round(mean_squared_error(y_test, y_pred_sub), round_to)
            ans_score = round(mean_squared_error(y_test, y_pred_ans), round_to)

        if metric == "r2_score":
            sub_score = round(r2_score(y_test, y_pred_sub), round_to)
            ans_score = round(r2_score(y_test, y_pred_ans), round_to)

        if metric == "accuracy_score":
            sub_score = round(accuracy_score(y_test, y_pred_sub), round_to)
            ans_score = round(accuracy_score(y_test, y_pred_ans), round_to)

        if metric == "precision_score":
            sub_score = round(precision_score(y_test, y_pred_sub), round_to)
            ans_score = round(precision_score(y_test, y_pred_ans), round_to)

        if metric == "recall_score":
            sub_score = round(recall_score(y_test, y_pred_sub), round_to)
            ans_score = round(recall_score(y_test, y_pred_ans), round_to)

        if metric == "f1_score":
            sub_score = round(f1_score(y_test, y_pred_sub), round_to)
            ans_score = round(f1_score(y_test, y_pred_ans), round_to)

        # Determine if submission beats answer
        if metric in error_metrics:
            # With error, smaller is better
            sub_beats_ans = (sub_score < ans_score) or isclose(
                sub_score, ans_score, rel_tol=tolerance
            )

        if metric in score_metrics:
            # With score, bigger is better
            sub_beats_ans = (sub_score > ans_score) or isclose(
                sub_score, ans_score, rel_tol=tolerance
            )

        # Update grader score and comment
        metric_verbose = metric.replace("_", " ")
        if sub_beats_ans:
            self.add_to_score()
            self.comment = (
                f"Your model's {metric_verbose} is `{sub_score}`. "
                + self.comment
            )

        else:
            self.update_comment(
                f"Your model's {metric_verbose} is `{sub_score}`. You can do better. "
                f"Try to beat `{ans_score}`."
            )

        if return_bool:
            return self.passed
        else:
            return None

    def grade_model_predictions(
        self,
        metric: str,
        threshold: float,
        round_to=3,
        tolerance=0.0,
        return_bool=False,
    ):
        """Evaluate model's performance using the predicitons itself.

        Submission and answer must be ``pd.Series``.

        Parameters
        ----------
        metric: str {"accuracy_score", "precision_score", "recall_score", "f1_score", "r2_score", "mean_absolute_error", "mean_squared_error"}
            Metric to use when evaluating predicitons.

        threshold: float
            Score that predictions must beat.

        round_to: int, default=3
            Number of decimal places to round metric to before comparing
            predictions score to threshold.

        tolerance : int or float, default=0.0
            What is the maximum allowed difference between prediction score
            and threshold. If ``tolerance=0.0``, predictions must beat threshold.
            If ``tolerance=0.1``, values must be within 10% of each other (relative to
            the larger absolute value of the two).

        Examples
        --------
        Let's start by creating a dataset.

        >>> from sklearn.datasets import fetch_california_housing
        >>> from sklearn.dummy import DummyRegressor
        >>> from sklearn.model_selection import train_test_split
        >>> import pandas as pd
        >>> from grading_tools.graders import SklearnGrader
        >>> X, y = fetch_california_housing(return_X_y=True, as_frame=True)
        >>> X_train, X_test, y_train, y_test = train_test_split(
        ...     X, y, test_size=0.2, random_state=42
        ... )

        Next, we'll train a model and generate a Series of predictions

        >>> model = DummyRegressor(strategy="constant", constant=2).fit(X_train, y_train)
        >>> y_pred = pd.Series(model.predict(X_test))

        Finally, we'll put the predictions and true values in a grader.

        >>> g = SklearnGrader(y_pred, y_test)

        The submission will pass as long as the metric score beats the threshold.

        >>> g.grade_model_predictions(
        ... metric="mean_absolute_error",
        ... threshold=0.9,
        ... return_bool=True,
        ... )
        >>> print(g.comment)
        Your model's mean absolute error is `0.893`. Boom! You got it.

        """
        # Whether submission model outperforms answer
        sub_beats_threshold = False

        # Grouping metrics into scores (higher is better) or errors (lower is better)
        score_metrics = [
            "accuracy_score",
            "precision_score",
            "recall_score",
            "f1_score",
            "r2_score",
        ]
        error_metrics = ["mean_absolute_error", "mean_squared_error"]

        if not isinstance(self.submission, pd.Series):
            raise TypeError(
                f"grade_model_predictions can only be used if submission is Series, "
                f"not {type(self.submission).__name__}."
            )

        if metric not in score_metrics + error_metrics:
            raise ValueError(
                f"'{metric}' is not a valid argument for `metric`. "
                f"Your options are {score_metrics + error_metrics}."
            )

        # Student's answer doesn't has wrong number of predicitions
        if len(self.submission) != len(self.answer):
            self.update_comment(
                f"Your submission should have length {len(self.answer)},"
                f"not {len(self.submission)}."
            )
            if return_bool:
                return False
            else:
                return None

        # Calculate training metrics for submission and answer
        if metric == "mean_absolute_error":
            sub_score = round(
                mean_absolute_error(self.answer, self.submission), round_to
            )

        if metric == "mean_squared_error":
            sub_score = round(
                mean_squared_error(self.answer, self.submission), round_to
            )

        if metric == "r2_score":
            sub_score = round(r2_score(self.answer, self.submission), round_to)

        if metric == "accuracy_score":
            sub_score = round(
                accuracy_score(self.answer, self.submission), round_to
            )

        if metric == "precision_score":
            sub_score = round(
                precision_score(self.answer, self.submission), round_to
            )

        if metric == "recall_score":
            sub_score = round(
                recall_score(self.answer, self.submission), round_to
            )

        if metric == "f1_score":
            sub_score = round(f1_score(self.answer, self.submission), round_to)

        # Determine if submission beats answer
        if metric in error_metrics:
            # With error, smaller is better
            sub_beats_threshold = (sub_score < threshold) or isclose(
                sub_score, threshold, rel_tol=tolerance
            )

        if metric in score_metrics:
            # With score, bigger is better
            sub_beats_threshold = (sub_score > threshold) or isclose(
                sub_score, threshold, rel_tol=tolerance
            )

        # Update grader score and comment
        metric_verbose = metric.replace("_", " ")
        if sub_beats_threshold:
            self.add_to_score()
            self.comment = (
                f"Your model's {metric_verbose} is `{sub_score}`. "
                + self.comment
            )

        else:
            self.update_comment(
                f"Your model's {metric_verbose} is `{sub_score}`. You can do better. "
                f"Try to beat `{threshold}`."
            )

        if return_bool:
            return self.passed
        else:
            return None


class PlotGrader(BaseGrader):
    """Grader for evaluating images."""

    def __init__(self, submission, answer, points=1):
        if isinstance(submission, tempfile._TemporaryFileWrapper):
            submission = Image.open(submission)
        super().__init__(submission, answer, points)

    def grade_plot_image(
        self,
        threshold=0.0,
        return_diff=True,
        diff_path="./diff.png",
        highlight_size=50,
        return_bool=False,
    ):
        """Compare two images.

        Evaluates how similar two images are by calculating the root mean square error
        between their pixels.

        Inspired by Matplotlib's `compare_images <https://matplotlib.org/devdocs/api/testing_api.html#matplotlib.testing.compare.compare_images>`_.

        Parameters
        ----------
        threshold: float, default=0.0
            The RMSE under which the submitted image needs to score in order to still
            be considered correct.

        return_diff: bool, default=True
            Whether to generate a file highlighting difference between submission and
            answer. If ``True``, file is saved to ``diff_path``.

        diff_path: str, default="./diff.png"
            Location to which the diff image will be saved.

        highlight_size: int, default=50
            How large the overlayed highlights in the diff image should be.

        return_bool : bool, default=False
            Whether to return ``self.passed`` once grading is complete. You'll need this if
            you want to design your own grading workflow beyond the default.

        """
        # Check that submission type is correct
        if not isinstance(self.submission, PngImageFile):
            raise TypeError(
                "grade_plot_image method can only be used on `PIL.Image` objects, "
                f"not {type(self.submission).__name__} objects."
            )

        # The submission needs to be the same size as answer
        if self.submission.size != self.answer.size:
            self.update_comment(
                "Your submission plot is not the same size as the expected result."
                "Make sure your plot has the fig size specified in the instructions"
                "and that you're saving the plot with the correct `dpi`."
            )
            if return_bool:
                return self.passed
            else:
                return None

        # Turn images into B&W ndarrays
        sub_bw_array = np.asarray(self.submission.convert("1")).astype(
            np.int16
        )
        ans_bw_array = np.asarray(self.answer.convert("1")).astype(np.int16)

        # If arrays are equal, passed
        if threshold <= 0:
            if np.array_equal(sub_bw_array, ans_bw_array):
                self.add_to_score()
                if return_bool:
                    return self.passed
                else:
                    return None

        # Calculate the per-pixel errors, then compute the root mean square error.
        rmse = np.sqrt(
            ((sub_bw_array - ans_bw_array).astype(float) ** 2).mean()
        )

        # If RMSE below threshold, passed
        if rmse < threshold:
            self.add_to_score()
            if return_bool:
                return self.passed
            else:
                return None

        # If RMSE is above threshold and you want a diff image
        if rmse > threshold and return_diff:
            # If it's not below threshold, make diff image
            # Step 1: Create diff array
            diff_bw_array = np.abs(ans_bw_array - sub_bw_array)

            # Step 2. Create diff B&W highlights array
            s = np.ones((highlight_size, highlight_size))
            diff_hl_bw = ndimage.morphology.binary_dilation(
                diff_bw_array, structure=s
            ).astype(int)

            # Step 3. Create RGB version of diff
            # 3.1. Start with empty array. The `4` refers RBG + alpha channels
            diff_hl_rgb = np.zeros(list(diff_hl_bw.shape) + [4])
            # 3.2. Add red pixels
            diff_hl_rgb[:, :, 0] = diff_hl_bw * 255
            # 3.3. Add alpha
            diff_hl_rgb[:, :, -1] = 125
            # 3.4. Add white pixels
            diff_hl_rgb[
                np.where((diff_hl_rgb == [0, 0, 0, 125]).all(axis=2))
            ] = [
                255,
                255,
                255,
                0,
            ]
            diff_hl_rgb = diff_hl_rgb.astype(np.uint8)

            # Step 4: Create diff image
            diff_hl_img = Image.fromarray(diff_hl_rgb)
            self.diff = self.submission.copy()
            self.diff.paste(diff_hl_img, (0, 0), mask=diff_hl_img)

            # Step 5: Save diff image
            self.diff.save(diff_path, format="png")
            self.diff_path = diff_path

            # Step 6: Update feedback
            self.update_comment(
                "Your submission doesn't match the expected result. "
                "Check the image below to see where your plot differs from the answer."
            )

        if rmse > threshold and not return_diff:
            self.update_comment(
                "Your submission doesn't match the expected result."
            )

        if return_bool:
            return self.passed
        else:
            return None


@dataclass
class EvaluationContext:
    actual_object_val: str = ""
    expected_object_val: str = ""
    object_name: str = ""


class Evaluation:
    """Data class for managing feedback passed to student machine."""

    def __init__(
        self,
        eval_code: str,
        points_awarded: Union[int, float] = 0,
        eval_context: Union[EvaluationContext, None] = None,
    ) -> None:
        """Istantiate ``Evaluation class``

        Args:
            eval_code (str): Eight-character error code passed to feedback module. If ``0``, student passes.
            points_awarded (Union[int, float], optional): Points awarded to student submission. Defaults to 0.
            eval_context (Union[EvaluationContext, None], optional): Additional context needed to generate feedback. Defaults to None.
        """
        self.eval_code = str(eval_code)
        self.eval_context = eval_context
        self.points_awarded = points_awarded
        self.__feedback = Feedback(self)

    @property
    def student_feedback(self):
        return self.__feedback.__dict__


class MatplotGrader(BaseGrader):
    """Grader for evaluating plots made with Matplotlib, pandas, or seaborn.

    Feedback mechanism currently works differently that other classes in this module.
    Instead of English feedback being generated in class, uses ``Evaluation`` class.

    Borrows heavily from ``matplotcheck``: https://github.com/earthlab/matplotcheck.
    """

    def __is_scatter(self) -> bool:
        """Boolean expressing if ax contains scatter points.

        If plot contains scatter points as well as lines, functions will return
        true. From ``matplotcheck``.

        Returns
        -------
        is_scatter : boolean
            True if Axes ax is a scatter plot, False if not
        """
        if self.submission.collections:
            return True
        elif self.submission.lines:
            for line in self.submission.lines:
                if (
                    line.get_linestyle() == "None"
                    or line.get_linewidth() == "None"
                    or line.get_linewidth() == 0
                ):
                    return True
        return False

    def __is_line(self) -> bool:
        """Boolean expressing if ax contains scatter points.

        If plot contains scatter points and lines return True.
        From ``matplotcheck``.

        Returns
        -------
        is_line : boolean
            True if Axes ax is a line plot, False if not
        """
        if self.submission.lines:
            for line in self.submission.lines:
                if (
                    not line.get_linestyle()
                    or not line.get_linewidth()
                    or line.get_linewidth() > 0
                ):
                    return True

    def __is_bar(self) -> bool:
        """Boolean expressing if ax contains bar containers.

        Returns
        -------
        is_bar : boolean
            True id Axes ax is a bar chart or histogram, False if not
        """
        return self.submission.containers

    def get_xy(
        self, ax=Literal["submission", "answer"], points_only=False
    ) -> pd.DataFrame:
        """Get (x, y) data from plot.

        Returns a pandas dataframe with columns "x" and "y" holding the x
        and y coords on the axis. From ``matplotcheck``.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Matplotlib Axes object to be tested
        points_only : boolean
            Set ``True`` to check only points, set ``False`` to check all data
            on plot.

        Returns
        -------
        df : pandas.DataFrame
            Pandas dataframe with columns "x" and "y" containing the x and y
            coords of each point on the axis.
        """
        if ax == "submission":
            ax = self.submission
        else:
            ax = self.answer

        if points_only:
            xy_coords = [
                val
                for line in ax.lines
                if (
                    line.get_linestyle() == "None"
                    or line.get_linewidth() == "None"
                )
                for val in line.get_xydata()
            ]  # .plot()
            xy_coords += [
                val
                for c in ax.collections
                if not isinstance(c, matplotlib.collections.PolyCollection)
                for val in c.get_offsets()
            ]  # .scatter()

        else:
            xy_coords = [
                val for line in ax.lines for val in line.get_xydata()
            ]  # .plot()
            xy_coords += [
                val for c in ax.collections for val in c.get_offsets()
            ]  # .scatter()
            xy_coords += [
                [(p.get_x() + (p.get_width() / 2)), p.get_height()]
                for p in ax.patches
            ]  # .bar()

        xy_data = pd.DataFrame(data=xy_coords, columns=["x", "y"]).dropna()

        # crop to limits
        lims = ax.get_xlim()
        xy_data = xy_data[xy_data["x"] >= lims[0]]
        xy_data = xy_data[xy_data["x"] <= lims[1]].reset_index(drop=True)

        # sort
        xy_data.sort_values(by=["x", "y"], inplace=True)

        return xy_data

    def grade_plot(
        self,
        plot_type: Literal[
            "acf", "bar", "barh", "box", "hist", "line", "pacf", "scatter"
        ],
        check_title=True,
        check_xlabel=True,
        check_ylabel=True,
        check_xticks=False,
        check_yticks=False,
        match_data=True,
        tolerance=0.01,
        data_source: Union[Literal["answer"], pd.DataFrame] = "answer",
    ):
        """Grade submitted plot (axis) against answer.

        Args:
            plot_type (Literal[ "acf", "bar", "barh", "box", "hist", "line", "pacf", "scatter" ]): Plot type that submission should be.
            check_title (bool, optional): Whether to check submission axis title against answer. Defaults to True.
            check_xlabel (bool, optional): Whether to check submission x-axis label against answer. Defaults to True.
            check_ylabel (bool, optional): Whether to check submission y-axis label against answer. Defaults to True.
            check_xticks (bool, optional): Whether to check submission x-axis ticks against answer. Defaults to False.
            check_yticks (bool, optional): Whether to check submission y-axis ticks against answer. Defaults to False.
            match_data (bool, optional): Whether to check submission data points against answer. Defaults to True.
            tolerance (float, optional): Tolerance when checking submission data points or data source against answer. Defaults to 0.01.
            data_source (Union[Literal["answer"], pd.DataFrame], optional): If ``match_data`` set to ``True``, you can either set this parameter to ``"answer"`` to check submission against answer plot. Otherwise, you can supply a DataFrame to match against submission. Defaults to "answer".

        Returns:
            dict : Feedback dict to be passed to student machine.
        """
        if plot_type == "scatter" and not self.__is_scatter():
            self.evaluation = Evaluation(
                eval_code="MPA01E02",
                eval_context=EvaluationContext(object_name="scatter plot"),
            )
            return self.evaluation.student_feedback

        # Box plots in matplotlib consist of lines
        if plot_type in ("line", "box") and not self.__is_line():
            plot_type_dict = {"line": "line plot", "box": "boxplot"}
            plot_type_name = plot_type_dict.get(plot_type, "")
            self.evaluation = Evaluation(
                eval_code="MPA01E02",
                eval_context=EvaluationContext(object_name=plot_type_name),
            )
            return self.evaluation.student_feedback

        if plot_type in ("bar", "hist") and not self.__is_bar():
            plot_type_dict = {
                "bar": "bar chart",
                "barh": "horizontal bar chart",
                "hist": "histogram",
            }
            plot_type_name = plot_type_dict.get(plot_type, "")
            self.evaluation = Evaluation(
                eval_code="MPA01E02",
                eval_context=EvaluationContext(object_name=plot_type_name),
            )
            return self.evaluation.student_feedback

        if plot_type in ("acf", "pacf") and not (
            self.__is_scatter() and self.__is_line()
        ):
            plot_type_dict = {
                "acf": "ACF",
                "pacf": "PACF",
            }
            plot_type_name = plot_type_dict.get(plot_type, "")
            self.evaluation = Evaluation(
                eval_code="MPA01E02",
                eval_context=EvaluationContext(object_name=plot_type_name),
            )
            return self.evaluation.student_feedback

        if check_title:
            # Missing title
            if not self.submission.get_title() and self.answer.get_title():
                self.evaluation = Evaluation(eval_code="MPA02E01")
                return self.evaluation.student_feedback
            # Incorrect title
            if self.submission.get_title() != self.answer.get_title():
                self.evaluation = Evaluation(
                    eval_code="MPA02E03",
                    eval_context=EvaluationContext(
                        actual_object_val=self.submission.get_title(),
                        expected_object_val=self.answer.get_title(),
                    ),
                )
                return self.evaluation.student_feedback

        if check_xlabel:
            # Missing x-axis label
            if not self.submission.get_xlabel() and self.answer.get_xlabel():
                self.evaluation = Evaluation(eval_code="MPA03E01")
                return self.evaluation.student_feedback
            # Incorrect x-axis label
            if self.submission.get_xlabel() != self.answer.get_xlabel():
                self.evaluation = Evaluation(
                    eval_code="MPA03E03",
                    eval_context=EvaluationContext(
                        actual_object_val=self.submission.get_xlabel(),
                        expected_object_val=self.answer.get_xlabel(),
                    ),
                )
                return self.evaluation.student_feedback

        if check_ylabel:
            # Missing x-axis label
            if not self.submission.get_ylabel() and self.answer.get_ylabel():
                self.evaluation = Evaluation(eval_code="MPA04E01")
                return self.evaluation.student_feedback
            # Incorrect x-axis label
            if self.submission.get_ylabel() != self.answer.get_ylabel():
                self.evaluation = Evaluation(
                    eval_code="MPA04E03",
                    eval_context=EvaluationContext(
                        actual_object_val=self.submission.get_ylabel(),
                        expected_object_val=self.answer.get_ylabel(),
                    ),
                )
                return self.evaluation.student_feedback

        if match_data and data_source == "answer":
            pdg = PandasGrader(
                submission=self.get_xy(ax="submission").astype(float),
                answer=self.get_xy(ax="answer").astype(float),
            )
            if not pdg.grade_df(tolerance=tolerance, return_bool=True):
                self.evaluation = Evaluation(eval_code="MPA05E04")
                return self.evaluation.student_feedback

        # Everything is correct
        self.evaluation = Evaluation(eval_code="0", points_awarded=self.points)
        return self.evaluation.student_feedback
