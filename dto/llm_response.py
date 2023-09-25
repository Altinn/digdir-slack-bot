from dataclasses import dataclass

@dataclass
class LLMResponse:
    answer: str
    time_elapsed_sec: float
    data: dict
