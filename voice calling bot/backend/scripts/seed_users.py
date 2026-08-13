"""
Seed default user accounts for the Enterprise AI Calling Platform.
Creates default Admin and Demo user credentials in PostgreSQL.
"""

import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database.connection import SessionLocal
from app.models.organization import Organization
from app.models.user import User, Role
from app.authentication.security import hash_password

DEFAULT_USERS = [
    {
        "email": "admin@voxera.ai",
        "password": "Password123!",
        "first_name": "Voxera",
        "last_name": "Admin",
        "role_slug": "super_admin",
    },
    {
        "email": "andrew.ui@uisocial.com",
        "password": "Password123!",
        "first_name": "Andrew",
        "last_name": "User",
        "role_slug": "org_admin",
    },
    {
        "email": "sarah@voxera.ai",
        "password": "Password123!",
        "first_name": "Sarah",
        "last_name": "SDR",
        "role_slug": "manager",
    },
]


def seed_users():
    """Seed user accounts into database synchronously."""
    print("=== Seeding Default User Accounts ===")

    with SessionLocal() as db:
        # Get or create default organization
        org_id = "00000000-0000-0000-0000-000000000000"
        org = db.query(Organization).filter_by(id=org_id).first()
        if not org:
            org = Organization(
                id=org_id,
                name="Voxera AI Platform",
                slug="voxera-ai",
                is_active=True,
            )
            db.add(org)
            db.commit()
            db.refresh(org)

        # Seed roles if not present
        admin_role = db.query(Role).filter_by(slug="super_admin").first()
        if not admin_role:
            admin_role = Role(
                name="Super Admin",
                slug="super_admin",
                description="Platform super administrator",
                permissions='["*"]',
                is_system=True,
            )
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)

        org_admin_role = db.query(Role).filter_by(slug="org_admin").first()
        if not org_admin_role:
            org_admin_role = Role(
                name="Organization Admin",
                slug="org_admin",
                description="Organization administrator",
                permissions='["manage_organization", "manage_users", "manage_agents"]',
                is_system=False,
            )
            db.add(org_admin_role)
            db.commit()
            db.refresh(org_admin_role)

        manager_role = db.query(Role).filter_by(slug="manager").first()
        if not manager_role:
            manager_role = Role(
                name="Manager",
                slug="manager",
                description="Manager access",
                permissions='["manage_agents", "view_analytics"]',
                is_system=False,
            )
            db.add(manager_role)
            db.commit()
            db.refresh(manager_role)

        role_map = {
            "super_admin": admin_role,
            "org_admin": org_admin_role,
            "manager": manager_role,
        }

        # Create user accounts
        for udata in DEFAULT_USERS:
            existing_user = db.query(User).filter_by(email=udata["email"]).first()
            role_obj = role_map.get(udata["role_slug"], org_admin_role)

            if not existing_user:
                hashed_pw = hash_password(udata["password"])
                new_user = User(
                    organization_id=org.id,
                    role_id=role_obj.id,
                    email=udata["email"],
                    first_name=udata["first_name"],
                    last_name=udata["last_name"],
                    password_hash=hashed_pw,
                    is_active=True,
                    is_verified=True,
                    timezone="UTC",
                    locale="en-US",
                )
                db.add(new_user)
                db.commit()
                print(f"Created Seed User: {udata['email']} (Password: {udata['password']})")
            else:
                existing_user.password_hash = hash_password(udata["password"])
                db.commit()
                print(f"User {udata['email']} already exists - Password updated to {udata['password']}")

    print("=== User Seeding Complete ===")


if __name__ == "__main__":
    seed_users()
