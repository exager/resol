from enum import Enum


class RetrievalDecision(str, Enum):
    ANSWERABLE = "answerable"
    REFUSE_EMPTY = "refuse_empty"
    REFUSE_WEAK = "refuse_weak"
