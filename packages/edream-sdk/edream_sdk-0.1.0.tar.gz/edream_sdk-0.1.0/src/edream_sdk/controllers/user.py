from typing import Optional
from edream_sdk.client.api_client import ApiClient
from edream_sdk.models.api_types import ApiResponse
from edream_sdk.models.user_types import UserResponseWrapper
from edream_sdk.utils.api_utils import deserialize_api_response


def get_logged_user() -> Optional[ApiResponse[UserResponseWrapper]]:
    """
    Retrieves the logged user
    Returns:
        Optional[ApiResponse[UserResponseWrapper]]: An `ApiResponse` object containing a `UserResponseWrapper`
    """
    client = ApiClient.get_instance()
    data = client.get(f"/auth/user")
    response = deserialize_api_response(data, UserResponseWrapper)
    user = response.data.user
    return user
