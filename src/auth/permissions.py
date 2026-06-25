from fastapi import Depends, HTTPException, status
from sqlmodel import select

from src.auth.dependencies import get_current_user
from src.db.main import get_session
from src.db.models import (
    User,
    RolePermission,
    Permission
)

class PermissionChecker:

    def __init__(self, permission: str):
        self.permission = permission

    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
        session = Depends(get_session)
    ):
        permission = await session.scalar(
            select(Permission)
            .where(
                Permission.name == self.permission
            )
        )

        if not permission:
            raise HTTPException(
                status_code=500,
                detail="Permission not found"
            )
        role_permission = await session.scalar(
            select(RolePermission)
            .where(
                RolePermission.role_id == current_user.role_id,
                RolePermission.permission_id == permission.id
            )
        )

        if not role_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return current_user