"""
Unit tests for TalentSphere Vector Embedding Engine, Candidate 360, and Semantic Search
"""

import pytest
import uuid
from unittest.mock import AsyncMock, Mock, patch

from app.core.embeddings import EmbeddingEngine, embedding_engine, VECTOR_DIMENSION
from app.modules.candidates.service import CandidateService
from app.modules.candidates.schemas import CandidateCreate, CandidateSemanticSearchRequest


class TestVectorEmbeddingEngine:
    """Test suite for Vector Embedding Engine"""

    def test_deterministic_embedding_dimension_and_norm(self):
        engine = EmbeddingEngine()
        text = "Senior Python Developer with LangGraph and PostgreSQL experience"
        vec = engine._generate_deterministic_vector(text)
        
        assert len(vec) == VECTOR_DIMENSION
        # Check L2 normalization (sum of squares should equal ~1.0)
        norm = sum(x * x for x in vec)
        assert abs(norm - 1.0) < 0.001

    def test_deterministic_embedding_empty_text(self):
        engine = EmbeddingEngine()
        vec = engine._generate_deterministic_vector("")
        assert len(vec) == VECTOR_DIMENSION
        assert all(x == 0.0 for x in vec)

    def test_cosine_similarity_identical_vectors(self):
        engine = EmbeddingEngine()
        v1 = engine._generate_deterministic_vector("Senior Full Stack Engineer")
        score = engine.cosine_similarity(v1, v1)
        assert abs(score - 1.0) < 0.001

    def test_cosine_similarity_semantic_relevance(self):
        engine = EmbeddingEngine()
        v1 = engine._generate_deterministic_vector("Python FastAPI PostgreSQL Backend Developer")
        v2 = engine._generate_deterministic_vector("Python Django PostgreSQL Backend Engineer")
        v3 = engine._generate_deterministic_vector("Certified Nurse Practitioner Healthcare")

        sim_related = engine.cosine_similarity(v1, v2)
        sim_unrelated = engine.cosine_similarity(v1, v3)

        assert sim_related > sim_unrelated

    @pytest.mark.asyncio
    async def test_get_embeddings_batch(self):
        engine = EmbeddingEngine()
        texts = ["Machine Learning Specialist", "DevOps Kubernetes Engineer"]
        embeddings = await engine.get_embeddings_batch(texts)
        
        assert len(embeddings) == 2
        assert len(embeddings[0]) == VECTOR_DIMENSION
        assert len(embeddings[1]) == VECTOR_DIMENSION


class TestCandidate360AndSemanticSearch:
    """Test suite for Candidate 360 and Semantic Search Service"""

    @pytest.mark.asyncio
    async def test_get_candidate_360_success(self):
        mock_db = AsyncMock()
        service = CandidateService(mock_db)
        
        test_org_id = uuid.uuid4()
        test_cand_id = uuid.uuid4()
        
        mock_cand = Mock(
            id=test_cand_id,
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            phone="+1-555-0199",
            profile_status="Active",
            is_blacklisted=False
        )
        
        service.cand_repo.get_by_id = AsyncMock(return_value=mock_cand)
        service.details_repo.get_profile = AsyncMock(return_value=Mock(summary="Experienced architect", total_experience_years=8.0, notice_period_days=15, current_salary=160000, expected_salary=190000))
        service.details_repo.get_education = AsyncMock(return_value=[])
        service.details_repo.get_experience = AsyncMock(return_value=[Mock(id=uuid.uuid4(), company_name="Tech Corp", designation_name="Principal Engineer", start_date=None, end_date=None, is_current=True, responsibilities="Architecture")])
        service.details_repo.get_skills = AsyncMock(return_value=[Mock(id=uuid.uuid4(), skill_name="Python", proficiency_level="Expert")])
        service.details_repo.get_certifications = AsyncMock(return_value=[])
        service.resume_repo.get_resumes = AsyncMock(return_value=[])
        service.details_repo.get_ai_profile = AsyncMock(return_value=Mock(ai_profile_completeness=90, ai_calculated_experience_years=8.0, ai_top_skills="Python, Architecture"))
        service.timeline_repo.get_timeline = AsyncMock(return_value=[])

        result = await service.get_candidate_360(test_org_id, test_cand_id)

        assert result["status"] == "success"
        cand_360 = result["candidate_360"]
        assert cand_360["first_name"] == "Jane"
        assert cand_360["current_role"] == "Principal Engineer"
        assert len(cand_360["skills"]) == 1
        assert cand_360["skills"][0]["name"] == "Python"

    @pytest.mark.asyncio
    async def test_semantic_search_success(self):
        mock_db = AsyncMock()
        service = CandidateService(mock_db)
        
        test_org_id = uuid.uuid4()
        cand1_id = uuid.uuid4()
        cand2_id = uuid.uuid4()

        mock_candidates = [
            {
                "id": cand1_id,
                "first_name": "Alice",
                "last_name": "Engineer",
                "email": "alice@example.com",
                "current_role": "Senior Python Backend Developer",
                "current_company": "AI Labs",
                "summary": "Expert in FastAPI, pgvector, and distributed systems",
                "skills": ["Python", "FastAPI", "PostgreSQL"]
            },
            {
                "id": cand2_id,
                "first_name": "Bob",
                "last_name": "Accountant",
                "email": "bob@example.com",
                "current_role": "Financial Auditor",
                "current_company": "Finance Corp",
                "summary": "Tax preparation and financial auditing",
                "skills": ["Accounting", "Tax", "Auditing"]
            }
        ]

        service.cand_repo.get_all_enriched = AsyncMock(return_value=mock_candidates)
        
        # Mock embedding vectors
        v1 = embedding_engine._generate_deterministic_vector("Alice Engineer Senior Python Backend Developer FastAPI pgvector Python FastAPI PostgreSQL")
        v2 = embedding_engine._generate_deterministic_vector("Bob Accountant Financial Auditor Tax Accounting")
        
        service.embedding_repo.get_all_embeddings = AsyncMock(return_value=[
            Mock(candidate_id=cand1_id, embedding=v1),
            Mock(candidate_id=cand2_id, embedding=v2)
        ])

        results = await service.semantic_search(
            org_id=test_org_id,
            query_text="Looking for a Senior Python Developer with FastAPI and Postgres skills",
            top_k=5,
            threshold=0.3
        )

        assert len(results) >= 1
        # Top match should be Alice Engineer
        assert results[0]["candidate_id"] == str(cand1_id)
        assert results[0]["candidate_name"] == "Alice Engineer"
        assert results[0]["match_score"] > 0
