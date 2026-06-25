from fastapi import Request,FastAPI,status
from typing import Any,Callable
from fastapi.responses import JSONResponse
class GovernException(Exception):
    pass
class UserAlreadyExists(GovernException):
    """User has provided an email for a user who exists during sign up."""
    pass
class InvalidCredentials(GovernException):
    """User has provided wrong email or password during log in."""
    pass

class InvalidToken(GovernException):
    """User has provided an invalid or expired token"""
    pass
class AccountNotActive(GovernException):
    """"account is not active"""
    pass

class AccessTokenRequired(GovernException):
    """User has provided a refresh token when an access token is needed"""
    pass

class CategoryAlreadyExists(GovernException):
    """Category with this name already exists"""
    pass

class CategoryNotFound(GovernException):
    """Category with this id not found"""
    pass
class InsufficientPermission(GovernException):
    """User does not have the necessary permissions to perform an action."""
    pass
class DataSourceNotFound(GovernException):
    """Category with this id not found"""
    pass

def create_exception_handler(
    status_code: int, initial_detail: Any

) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: GovernException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler

def register_error_handlers(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "User with this informations already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotActive,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account is not active",
                "error_code": "account_not_active",
            },
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )

    app.add_exception_handler(
        CategoryAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "Category with this name already exists",
                "error_code": "category_exists",
            },
        ),
    )

    app.add_exception_handler(
        CategoryNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Category with this id not exists",
                "error_code": "category_NotFound",
            },
        ),
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )

    app.add_exception_handler(
        DataSourceNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "datasource with this id not exists",
                "error_code": "DataSource_NotFound",
            },
        ),
    )