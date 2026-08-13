import sys
import os
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config.settings import get_settings
from app.models.base import Base
import app.models  # Ensures all SQLAlchemy models are imported and registered with Base

def init_database():
    settings = get_settings()
    
    print("=== Voxera PostgreSQL Database Initialization ===")
    print(f"Target DB Host: {settings.db_host}:{settings.db_port}")
    print(f"Target DB Name: {settings.db_name}")

    encoded_pass = quote_plus(settings.db_password)
    admin_url = f"postgresql+psycopg://{settings.db_user}:{encoded_pass}@{settings.db_host}:{settings.db_port}/postgres"
    
    # 1. Connect to PostgreSQL server to create target database if needed
    try:
        admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
        with admin_engine.connect() as conn:
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{settings.db_name}'"))
            if not result.scalar():
                print(f"Creating PostgreSQL Database '{settings.db_name}'...")
                conn.execute(text(f"CREATE DATABASE {settings.db_name}"))
                print(f"Database '{settings.db_name}' created successfully!")
            else:
                print(f"PostgreSQL Database '{settings.db_name}' already exists.")
    except Exception as e:
        print(f"Failed to check/create PostgreSQL database '{settings.db_name}': {e}")
        raise e

    # 2. Connect to actual PostgreSQL target database
    db_url = f"postgresql+psycopg://{settings.db_user}:{encoded_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    engine = create_engine(db_url)
    print("Connected to PostgreSQL database successfully.")

    # 3. Create All Tables in PostgreSQL
    print("Creating database tables in PostgreSQL...")
    try:
        with engine.connect() as conn:
            conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
            conn.commit()
    except Exception as e:
        print(f"Schema drop info: {e}")

    Base.metadata.create_all(engine)
    print("All PostgreSQL database tables created successfully!")

    # 4. Seed Default Records in PostgreSQL
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        from app.models.organization import Organization
        from app.models.agent import Agent
        from app.models.phone_number import PhoneNumber
        from app.models.lead import Lead

        org_id = "00000000-0000-0000-0000-000000000000"
        org = session.query(Organization).filter_by(id=org_id).first()
        if not org:
            org = Organization(
                id=org_id,
                name="Voxera AI Platform",
                slug="voxera-ai",
                is_active=True
            )
            session.add(org)
            session.commit()
            print("Seeded Organization: Voxera AI Platform")

            # Seed Default Organization Settings
            from app.models.organization import OrganizationSettings
            # get_settings is already imported globally, use it directly
            app_settings = settings # 'settings' is already defined at the top of the function
            
            org_settings = OrganizationSettings(
                organization_id=org.id,
                twilio_account_sid=app_settings.twilio_account_sid or "",
                twilio_auth_token=app_settings.twilio_auth_token or ""
            )
            session.add(org_settings)
            session.commit()
            print("Seeded Organization Settings")

        # Seed Default Agent
        agent = session.query(Agent).filter_by(organization_id=org_id).first()
        if not agent:
            agent = Agent(
                organization_id=org_id,
                name="Sarah - Sales SDR",
                description="Outbound SDR agent specializing in tech product qualification.",
                system_prompt="You are Sarah, an outbound SDR calling potential clients.",
                default_language="en-US",
                status="active"
            )
            session.add(agent)
            session.commit()
            print("Seeded Agent: Sarah - Sales SDR")

        # Seed Default Phone Number
        phone = session.query(PhoneNumber).filter_by(organization_id=org_id).first()
        if not phone:
            phone = PhoneNumber(
                organization_id=org_id,
                number="+17372212163",
                provider="Twilio",
                status="active"
            )
            session.add(phone)
            session.commit()
            print("Seeded Phone Number: +17372212163")

        # Seed Default Lead
        lead = session.query(Lead).filter_by(organization_id=org_id).first()
        if not lead:
            lead = Lead(
                organization_id=org_id,
                name="Harsh Shirsath",
                phone_number="+917039015196",
                email="harsh@example.com",
                status="pending"
            )
            session.add(lead)
            session.commit()
            print("Seeded Lead: Harsh Shirsath (+917039015196)")

        # Seed Default Knowledge Base Script
        from app.models.knowledge_base import KnowledgeBase, KnowledgeDocument
        kb = session.query(KnowledgeBase).filter_by(organization_id=org_id).first()
        if not kb:
            kb = KnowledgeBase(
                organization_id=org_id,
                name="Sales & Product FAQ Script",
                description="Voxera AI Platform sales qualifying questions, pricing, and latency details.",
                document_count=1,
            )
            session.add(kb)
            session.commit()

            doc = KnowledgeDocument(
                knowledge_base_id=kb.id,
                title="Voxera Sales Script & Product Guide",
                file_name="voxera_sales_script.txt",
                file_path="/documents/voxera_sales_script.txt",
                file_size=1024,
                file_type="txt",
                embedding_status="completed",
                chunk_count=1,
            )

            session.add(doc)
            session.commit()
            print("Seeded Knowledge Base & Script Document!")

    except Exception as e:
        print(f"Error seeding default PostgreSQL records: {e}")
    finally:
        session.close()

    print("=== PostgreSQL Database Initialization Complete ===")

if __name__ == "__main__":
    init_database()
