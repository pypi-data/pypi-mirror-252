class RequiredFieldValidationError(Exception):
    def __init__(self, field):
        super().__init__(f"required field value is missing: {field}")


def required(*fields):
    """Validate all the listed fields are not None for the particular decorated instance"""

    def decorator(cls):
        class Wrapper(cls):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                for field in fields:
                    if getattr(self, field) is None:
                        raise RequiredFieldValidationError(field)

        return Wrapper

    return decorator
