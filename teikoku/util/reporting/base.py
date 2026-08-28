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
