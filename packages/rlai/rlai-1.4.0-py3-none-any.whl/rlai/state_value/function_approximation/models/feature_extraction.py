from abc import ABC, abstractmethod
from itertools import product
from typing import List, Optional, Dict, Callable, Any

import numpy as np

from rlai.core import MdpState
from rlai.meta import rl_text
from rlai.models.feature_extraction import FeatureExtractor, OneHotCategory, OneHotCategoricalFeatureInteracter


@rl_text(chapter='Feature Extractors', page=1)
class StateFeatureExtractor(FeatureExtractor, ABC):
    """
    Feature extractor for states.
    """

    @abstractmethod
    def extract(
            self,
            state: MdpState,
            refit_scaler: bool
    ) -> np.ndarray:
        """
        Extract state features.

        :param state: State.
        :param refit_scaler: Whether to refit the feature scaler before scaling the extracted features. This is
        only appropriate in settings where nonstationarity is desired (e.g., during training). During evaluation, the
        scaler should remain fixed, which means this should be False.
        :return: State-feature vector.
        """


class StateDimensionIndicator(ABC):
    """
    Abstract state-dimension indicator.
    """

    def __init__(
            self,
            dimension: Optional[int]
    ):
        """
        Initialize the indicator.

        :param dimension: Dimension, or None for an indicator that is not based on a value of the state vector.
        """

        self.dimension = dimension

    @abstractmethod
    def __str__(
            self
    ) -> str:
        """
        Get string.

        :return: String.
        """

    @abstractmethod
    def get_range(
            self
    ) -> List[Any]:
        """
        Get the range (possible values) of the current indicator.

        :return: Range of values.
        """

    @abstractmethod
    def get_value(
            self,
            state: np.ndarray
    ) -> Any:
        """
        Get the value of the current indicator for a state.

        :param state: State vector.
        :return: Value.
        """


class StateDimensionSegment(StateDimensionIndicator):
    """
    Segment of a state dimension.
    """

    @staticmethod
    def get_segments(
            dimension_breakpoints: Dict[int, List[float]]
    ) -> List['StateDimensionIndicator']:
        """
        Get segments for a dictionary of breakpoints

        :param dimension_breakpoints: Breakpoints keyed on dimensions with breakpoints as values.
        """

        return [
            StateDimensionSegment(dimension, low, high)
            for dimension, breakpoints in dimension_breakpoints.items()
            for low, high in zip([None] + breakpoints[:-1], breakpoints)  # type: ignore[operator]
        ]

    def __init__(
            self,
            dimension: int,
            low: Optional[float],
            high: Optional[float]
    ):
        """
        Initialize the segment.

        :param dimension: Dimension index.
        :param low: Low value (inclusive) of the segment.
        :param high: High value (exclusive) of the segment.
        """

        super().__init__(dimension)

        self.low = low
        self.high = high

    def __str__(
            self
    ) -> str:
        """
        Get string.

        :return: String.
        """

        return f'd{self.dimension}:  {"(" if self.low is None else "["}{self.low}, {self.high})'

    def get_range(
            self
    ) -> List[Any]:
        """
        Get the range (possible values) of the current indicator.

        :return: Range of values.
        """

        return [True, False]

    def get_value(
            self,
            state: np.ndarray
    ) -> Any:
        """
        Get the value of the current indicator for a state.

        :param state: State vector.
        :return: Value.
        """

        assert self.dimension is not None

        dimension_value = float(state[self.dimension])
        above_low = self.low is None or dimension_value >= self.low
        below_high = self.high is None or dimension_value < self.high

        return above_low and below_high


class StateDimensionLambda(StateDimensionIndicator):
    """
    Lambda applied to a state dimension.
    """

    def __init__(
            self,
            dimension: Optional[int],
            function: Callable[[Optional[float]], Any],
            function_range: List[Any]
    ):
        """
        Initialize the segment.

        :param dimension: Dimension, or None for an indicator that is not based on a value of the state vector.
        :param function: Function to apply to values in the given dimension.
        :param function_range: Range of function.
        """

        super().__init__(dimension)

        self.function = function
        self.function_range = function_range

    def __str__(
            self
    ) -> str:
        """
        Get string.

        :return: String.
        """

        return f'd{self.dimension}:  <function>'

    def get_range(self) -> List[Any]:
        """
        Get the range (possible values) of the current indicator.

        :return: Range of values.
        """

        return self.function_range

    def get_value(
            self,
            state: np.ndarray
    ) -> Any:
        """
        Get the value of the current indicator for a state.

        :param state: State vector.
        :return: Value.
        """

        if self.dimension is None:
            dimension_value = None
        else:
            dimension_value = float(state[self.dimension])

        return self.function(dimension_value)


class OneHotStateIndicatorFeatureInteracter:
    """
    One-hot state indicator feature interacter.
    """

    def interact(
            self,
            state_matrix: np.ndarray,
            state_feature_matrix: np.ndarray
    ) -> np.ndarray:
        """
        Interact a state-feature matrix with its one-hot state-indicator encoding.

        :param state_matrix: State matrix (#obs, #state_dimensionality), from which to derive indicators.
        :param state_feature_matrix: State-feature matrix (#obs, #features).
        :return: Interacted state-feature matrix (#obs, #features * #joint_indicators).
        """

        # interact feature vectors per state category, where the category indicates the joint indicator of the state.
        state_categories = [
            OneHotCategory(*[
                indicator.get_value(state_vector)
                for indicator in self.indicators
            ])
            for state_vector in state_matrix
        ]

        interacted_state_feature_matrix = self.interacter.interact(
            feature_matrix=state_feature_matrix,
            categorical_values=state_categories
        )

        return interacted_state_feature_matrix

    def __init__(
            self,
            indicators: List[StateDimensionIndicator]
    ):
        """
        Initialize the interacter.

        :param indicators: State-dimension indicators.
        """

        self.indicators = indicators

        self.interacter = OneHotCategoricalFeatureInteracter([
            OneHotCategory(*args)
            for args in product(*[
                indicator.get_range()
                for indicator in self.indicators
            ])
        ])
