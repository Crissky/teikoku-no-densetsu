from teikoku.enum.reporting import ReportingStatusEnum


@dataclass
class ReportingBase:
    message: str
    status: ReportingStatusEnum

    def __init__(self, **kwargs):
        if "message" not in kwargs:
            raise ValueError("Reporting precisa do campo 'message'.")
        if "status" not in kwargs:
            raise ValueError("Reporting precisa do campo 'status'.")

        message = kwargs["message"]
        if not isinstance(message, str):
            raise TypeError(
                f"O campo 'message' precisa ser do tipo str ({type(message)})."
            )

        status = kwargs["status"]
        if not isinstance(status, (str, ReportingStatusEnum)):
            raise TypeError(
                "O campo 'status' precisa ser do tipo str ou "
                f"ReportingStatusEnum ({type(status)})."
            )

        if isinstance(status, str):
            kwargs["status"] = ReportingStatusEnum(status)

        for name, value in kwargs.items():
            setattr(self, name, value)
        self.kwargs = list(kwargs.keys())

    def __str__(self):
        return ", ".join(f"{a}={getattr(self, a)}" for a in self.kwargs)

    def __repr__(self):
        text = str(self)
        return f"{self.__class__.__name__}({text})"

    @property
    def report(self) -> dict:
        return {a: getattr(self, a) for a in self.kwargs}

    @property
    def text(self) -> str:
        return self.message

    @property
    def status_name(self) -> str:
        return self.status.name

    @property
    def status_text(self) -> str:
        return self.status.value


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    r = ReportingBase(
        city="cidade",
        message="Mensagem de teste.",
        status="success",
    )
    print(r)
    print(repr(r))
    print("REPORT:", r.report)
    print("TEXT:", r.text)
    print("STATUS NAME:", r.status_name)
    print("STATUS TEXT:", r.status_text)
    print(" END LOCAL TEST ".center(79, "="))
