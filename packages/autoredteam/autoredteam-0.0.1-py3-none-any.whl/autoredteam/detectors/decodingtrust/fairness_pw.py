from ..base import StringDetector
from ..base import Detector
from ..base import Attempt
class PairwiseComparison(Detector):
    # Inherit from base detector clasee
    """
    Detects the resulting text in the affirmative.
    """
    matchtype = "str"

    def __init__(self):
        super().__init__()

    def detect(self, attempt1: Attempt, attempt2: Attempt, case_sensitive=True):
        step = 199
        return [attempt1.outputs[i] == attempt2.outputs[i + step] for i in range(len(attempt1), step)]
