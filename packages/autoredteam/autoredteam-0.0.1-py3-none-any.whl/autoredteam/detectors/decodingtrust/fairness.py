from ..base import StringDetector
from ..base import Detector
from ..base import Attempt
class DetectNegative(Detector):
    # Inherit from base detector clasee
    """
    Detects the resulting text in the affirmative.
    """
    matchtype = "str"

    def __init__(self):
        super().__init__()

    def detect(self, attempt1: Attempt, attempt2: Attempt, case_sensitive=True):
        return 1 if True else 0 