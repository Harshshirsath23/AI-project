"""
Seed default roles and permissions for the Enterprise AI Calling Platform.

This script creates the default roles with their associated permissions.
Run this after database migrations to set up the initial RBAC structure.
"""

import asyncio
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import AsyncSessionLocal, init_db
from app.models.user import Role
from app.core.logging import get_logger

logger = get_logger(__name__)


# Default roles with their permissions
DEFAULT_ROLES = [
    {
        "name": "Super Admin",
        "slug": "super_admin",
        "description": "Platform super administrator with full access to all organizations and features",
        "permissions": ["*"],  # Wildcard for all permissions
        "is_system": True,
    },
    {
        "name": "Organization Admin",
        "slug": "org_admin",
        "description": "Organization administrator with full access to organization resources",
        "permissions": [
            "manage_organization",
            "manage_users",
            "manage_agents",
            "manage_campaigns",
            "manage_leads",
            "manage_knowledge_base",
            "manage_prompts",
            "view_analytics",
            "export_reports",
            "manage_api_keys",
        ],
        "is_system": False,
    },
    {
        "name": "Manager",
        "slug": "manager",
        "description": "Manager with access to most features except user management",
        "permissions": [
            "manage_agents",
            "manage_campaigns",
            "manage_leads",
            "manage_knowledge_base",
            "manage_prompts",
            "view_analytics",
            "export_reports",
            "launch_campaigns",
        ],
        "is_system": False,
    },
    {
        "name": "Supervisor",
        "slug": "supervisor",
        "description": "Supervisor with campaign and lead management access",
        "permissions": [
            "manage_campaigns",
            "manage_leads",
            "upload_leads",
            "view_analytics",
            "launch_campaigns",
        ],
        "is_system": False,
    },
    {
        "name": "Agent Manager",
        "slug": "agent_manager",
        "description": "Manager focused on AI agent configuration",
        "permissions": [
            "manage_agents",
            "manage_knowledge_base",
            "manage_prompts",
            "view_analytics",
        ],
        "is_system": False,
    },
    {
        "name": "Campaign Manager",
        "slug": "campaign_manager",
        "description": "Manager focused on campaign execution",
        "permissions": [
            "manage_campaigns",
            "manage_leads",
            "upload_leads",
            "launch_campaigns",
            "view_analytics",
        ],
        "is_system": False,
    },
    {
        "name": "Analyst",
        "slug": "analyst",
        "description": "Analyst with read-only access to analytics and reports",
        "permissions": [
            "view_analytics",
            "export_reports",
            "view_campaigns",
            "view_leads",
        ],
        "is_system": False,
    },
    {
        "name": "Viewer",
        "slug": "viewer",
        "description": "Read-only access to organization resources",
        "permissions": [
            "view_agents",
            "view_campaigns",
            "view_leads",
            "view_knowledge_base",
            "view_prompts",
        ],
        "is_system": False,
    },
]


async def seed_roles(db: AsyncSession) -> None:
    """Seed default roles and permissions."""
    logger.info("Starting to seed default roles...")

    for role_data in DEFAULT_ROLES:
        # Check if role already exists
        result = await db.execute(
            select(Role).where(Role.slug == role_data["slug"])
        )
        existing_role = result.scalar_one_or_none()

        if existing_role:
            logger.info(f"Role '{role_data['slug']}' already exists, skipping")
            continue

        # Create role
        role = Role(
            name=role_data["name"],
            slug=role_data["slug"],
            description=role_data["description"],
            permissions=json.dumps(role_data["permissions"]),
            is_system=role_data["is_system"],
        )

        db.add(role)
        logger.info(f"Created role: {role_data['name']} ({role_data['slug']})")

    await db.commit()
    logger.info("Default roles seeded successfully")


async def main():
    """Main function to run the seeding."""
    logger.info("Initializing database connection...")
    await init_db()

    async with AsyncSessionLocal() as db:
        try:
            await seed_roles(db)
        except Exception as e:
            logger.error("Failed to seed roles", error=str(e))
            raise


if __name__ == "__main__":
    asyncio.run(main())
