from http import HTTPStatus


class CustomException(Exception):
    """Base exception for all application-level errors.

    Class-level attributes define the default HTTP response contract.
    Instances may override ``message`` via the constructor.

    Attributes:
        status_code: HTTP status code included in the response.
        error_code: Machine-readable error identifier.
        message: Human-readable error description.
    """

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR.value
    error_code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None) -> None:
        """Initialise with an optional custom message.

        Args:
            message: Overrides the class-level default when provided.
        """
        self.message = message or self.__class__.message
        super().__init__(self.message)


class BadRequestException(CustomException):
    """Raised when the request is malformed or contains invalid input."""

    status_code = HTTPStatus.BAD_REQUEST.value
    error_code = "BAD_REQUEST"
    message = "Bad request."


class NotFoundException(CustomException):
    """Raised when a requested resource does not exist or has been soft-deleted."""

    status_code = HTTPStatus.NOT_FOUND.value
    error_code = "NOT_FOUND"
    message = "Resource not found."


class WeightLimitExceededException(CustomException):
    """Raised when total package weight exceeds the vehicle's maximum capacity.

    Always results in HTTP 422 Unprocessable Entity.

    Attributes:
        total_weight: Actual total weight of the requested packages (kg).
        max_weight: Vehicle's maximum allowed payload (kg).
    """

    status_code = HTTPStatus.UNPROCESSABLE_ENTITY.value
    error_code = "WEIGHT_LIMIT_EXCEEDED"
    message = "Total weight exceeds vehicle capacity."

    def __init__(self, total_weight: float, max_weight: float) -> None:
        """Initialise with actual and maximum weights.

        Args:
            total_weight: Sum of all package weights in the routing request.
            max_weight: Vehicle's declared weight capacity.
        """
        message = (
            f"Total weight {total_weight:.2f}kg exceeds "
            f"vehicle capacity of {max_weight:.2f}kg."
        )
        super().__init__(message)
        self.total_weight = total_weight
        self.max_weight = max_weight


class InsufficientPackagesException(CustomException):
    """Raised when the routing request contains no package IDs."""

    status_code = HTTPStatus.BAD_REQUEST.value
    error_code = "INSUFFICIENT_PACKAGES"
    message = "At least one package ID is required."
