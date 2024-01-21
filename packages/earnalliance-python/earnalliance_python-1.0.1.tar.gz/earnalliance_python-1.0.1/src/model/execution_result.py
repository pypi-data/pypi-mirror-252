class ExecutionResult:
    def __init__(self, message: str) -> None:
        self.message = message


class Success(ExecutionResult):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Failure(ExecutionResult):
    def __init__(self, message: str) -> None:
        super().__init__(message)


@staticmethod
def exception_result(ex: Exception) -> Failure:
    return Failure(str(ex))


@staticmethod
def error_result(message: str) -> Failure:
    return Failure(message)


@staticmethod
def success_result(message: str) -> Success:
    return Success(message)
