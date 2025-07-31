from enum import Enum


class PromptType(str, Enum):
    SUMMARY = "summary"
    EVALUATION = "evaluation"
