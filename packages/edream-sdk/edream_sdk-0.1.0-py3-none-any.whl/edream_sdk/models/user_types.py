from typing import Optional
from dataclasses import dataclass
from enum import Enum

# from .dream_types import Dream


# Enum for RoleType
class RoleType(Enum):
    ADMIN_GROUP = "admin-group"
    USER_GROUP = "user-group"
    CREATOR_GROUP = "creator-group"


# Data class for Token
@dataclass
class Token:
    AccessToken: str
    ExpiresIn: int
    IdToken: str
    RefreshToken: str
    TokenType: str


# Data class for Role
@dataclass
class Role:
    id: int
    name: RoleType


# Data class for User
@dataclass
class User:
    id: int
    email: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    avatar: Optional[str] = None
    cognitoId: Optional[str] = None
    role: Optional[Role] = None
    # currentDream: Optional[Dream] = None
    # currentPlaylist: Optional[Playlist] = None
    nsfw: Optional[bool] = None
    enableMarketingEmails: Optional[bool] = None
    # signupInvite: Optional[Invite] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    last_login_at: Optional[str] = None


# Data class for UserWithToken
@dataclass
class UserWithToken(User):
    token: Optional[Token] = None


@dataclass
class UserResponseWrapper:
    user: Optional[User]
