import asyncio
from src.db.main import async_session_maker
from src.db.models import User,Role,Permission,RolePermission
from sqlmodel import select
from src.auth.utils import generate_password_hash

PERMISSIONS = [
    
    "users.read",
    "users.update",

    "categories.create",
    "categories.read",
    "categories.update",
    "categories.delete",

    "datasources.create",
    "datasources.read",
    "datasources.update",
    "datasources.delete",

    "scan.run",
    "scan.read",

    "dataset.read",
    "dataset.submit",
    "dataset.approve",
    "dataset.reject",

    "tags.create",
    "tags.read",
    "tags.update",
    "tags.delete",

    "audit.read",

    "sensitive.unmasked",
]


ROLE_PERMISSIONS = {
    "admin": PERMISSIONS,

    "editor": [
        "categories.read",

        "datasources.create",
        "datasources.read",
        "datasources.update",

        "scan.run",
        "scan.read",

        "dataset.read",
        "dataset.submit",

        "tags.read",

        "audit.read",
    ],

    "viewer": [
        "categories.read",

        "datasources.read",

        "scan.read",

        "dataset.read",

        "tags.read",
    ]
}


async def seed_rbac():
    print("SEED STARTED")
    async with async_session_maker() as session:

        roles = {}

        for role_name in ROLE_PERMISSIONS.keys():

            role = await session.scalar(
                select(Role).where(Role.name == role_name)
            )

            if not role:
                role = Role(
                    name=role_name,
                    description=f"{role_name} role"
                )
                session.add(role)
                await session.flush()

            roles[role_name] = role

        permissions = {}

        for permission_name in PERMISSIONS:

            permission = await session.scalar(
                select(Permission).where(
                    Permission.name == permission_name
                )
            )

            if not permission:
                permission = Permission(
                    name=permission_name
                )
                session.add(permission)
                await session.flush()

            permissions[permission_name] = permission

        await session.commit()

        for role_name, perms in ROLE_PERMISSIONS.items():

            role = roles[role_name]

            for perm_name in perms:

                permission = permissions[perm_name]

                exists = await session.scalar(
                    select(RolePermission).where(
                        RolePermission.role_id == role.id,
                        RolePermission.permission_id == permission.id
                    )
                )

                if not exists:
                    session.add(
                        RolePermission(
                            role_id=role.id,
                            permission_id=permission.id
                        )
                    )

        await session.commit()
        
        admin = User(
                username="admin",
                email="admin@test.com",
                hashed_password=generate_password_hash("password123"),
                role_id=roles['admin'].id,

            )
        session.add(admin)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_rbac())