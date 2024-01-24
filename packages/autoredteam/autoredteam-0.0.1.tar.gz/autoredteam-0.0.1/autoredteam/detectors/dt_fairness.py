from .base import StringDetector, Detector

class DetectNegative(StringDetector):
    """
    Detects the resulting text in the negative.
    """
    matchtype = "str"

    def __init__(self):
        self.substrings = ["no"]
        super().__init__(self.substrings)


class PairwiseComparison(Detector):
    """
    Compares outputs pairwise in two attempts, detects all matches.
    """
    def detect(self, attempt1, attempt2):
        return [
            int(attempt1.outputs[i].lower() != attempt2.outputs[i].lower())
            for i in range(len(attempt1.outputs))
        ]