from dataclasses import dataclass


@dataclass
class ReportingBase:
    message: str

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.kwargs = list(kwargs.keys())
