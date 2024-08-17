from typing import List


class SubqueryResult:
    def __init__(self, follow_up: List[str], subquery: List[str]):
        self.follow_up = follow_up
        self.subquery = subquery


class SubqueryGenerator:
    def generate(self, question: str) -> SubqueryResult:
        raise NotImplementedError("Subclasses must implement this method")