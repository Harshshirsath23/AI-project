--
-- PostgreSQL database dump
--

\restrict AY9XsZWxTwcWFJksnJr14dbjN3fFSHxiUHHkH6AT5cqKzbxMWQYgs6FjzMfoGzI

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity_feed; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_feed (
    organization_id uuid NOT NULL,
    feed_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: activity_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activity_logs (
    user_id uuid NOT NULL,
    module character varying(50) NOT NULL,
    action character varying(100) NOT NULL,
    entity_type character varying(100),
    entity_id uuid,
    "timestamp" timestamp with time zone NOT NULL,
    ip_address character varying(45),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_agent_capabilities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_agent_capabilities (
    agent_id uuid NOT NULL,
    capability_name character varying(150) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_agents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_agents (
    agent_code character varying(50) NOT NULL,
    agent_name character varying(150) NOT NULL,
    description text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_audit_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_audit_logs (
    organization_id uuid NOT NULL,
    details text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_behavior_analysis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_behavior_analysis (
    interview_id uuid NOT NULL,
    trait_scores json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_candidate_feedback; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_candidate_feedback (
    interview_id uuid NOT NULL,
    feedback_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_candidate_rankings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_candidate_rankings (
    job_id uuid NOT NULL,
    application_id uuid NOT NULL,
    ranking_score double precision NOT NULL,
    rank_position integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_conversations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_conversations (
    user_id uuid NOT NULL,
    title character varying(200) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_cost_tracking; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_cost_tracking (
    execution_id uuid NOT NULL,
    cost_usd double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_decision_support; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_decision_support (
    recommendation_id uuid NOT NULL,
    explanation_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_execution_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_execution_logs (
    execution_id uuid NOT NULL,
    log_level character varying(20) NOT NULL,
    log_message text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_executions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_executions (
    request_id uuid NOT NULL,
    model_version_id uuid,
    tokens_used integer NOT NULL,
    latency_ms integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_feedback; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_feedback (
    execution_id uuid NOT NULL,
    rating integer NOT NULL,
    feedback_text text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_interview_analysis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_interview_analysis (
    interview_id uuid NOT NULL,
    analysis_text text NOT NULL,
    confidence_score double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_interview_scores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_interview_scores (
    interview_id uuid NOT NULL,
    overall_score double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_interview_summary; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_interview_summary (
    interview_id uuid NOT NULL,
    summary_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_job_recommendations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_job_recommendations (
    candidate_id uuid NOT NULL,
    job_id uuid NOT NULL,
    recommendation_strength double precision NOT NULL,
    justification text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_memory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_memory (
    user_id uuid NOT NULL,
    memory_key character varying(100) NOT NULL,
    memory_value text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_messages (
    conversation_id uuid NOT NULL,
    role character varying(20) NOT NULL,
    message_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_metrics; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_metrics (
    organization_id uuid NOT NULL,
    metric_name character varying(100) NOT NULL,
    metric_value double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_model_configurations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_model_configurations (
    model_version_id uuid NOT NULL,
    temperature double precision NOT NULL,
    max_tokens integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_model_providers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_model_providers (
    provider_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_model_versions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_model_versions (
    model_id uuid NOT NULL,
    version_code character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_models; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_models (
    provider_id uuid NOT NULL,
    model_code character varying(100) NOT NULL,
    model_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_recommendations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_recommendations (
    candidate_id uuid NOT NULL,
    recommended_job_id uuid NOT NULL,
    recommendation_score double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_recruitment_insights; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_recruitment_insights (
    organization_id uuid NOT NULL,
    insight_type character varying(100) NOT NULL,
    insight_text text NOT NULL,
    generated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_requests (
    user_id uuid NOT NULL,
    request_type character varying(100) NOT NULL,
    request_payload json,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_responses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_responses (
    execution_id uuid NOT NULL,
    response_payload json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_screening_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_screening_results (
    application_id uuid NOT NULL,
    calculated_match_score double precision NOT NULL,
    bias_score double precision,
    screening_summary text,
    analyzed_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_summaries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_summaries (
    conversation_id uuid NOT NULL,
    summary_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_tool_executions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_tool_executions (
    execution_id uuid NOT NULL,
    tool_id uuid NOT NULL,
    tool_payload json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_tool_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_tool_permissions (
    tool_id uuid NOT NULL,
    role_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_tools; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_tools (
    tool_code character varying(100) NOT NULL,
    tool_name character varying(150) NOT NULL,
    description text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_workflow_steps; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_workflow_steps (
    workflow_id uuid NOT NULL,
    step_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: ai_workflows; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_workflows (
    workflow_name character varying(150) NOT NULL,
    description text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: announcements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.announcements (
    organization_id uuid NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: api_credentials; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.api_credentials (
    organization_id uuid NOT NULL,
    credential_name character varying(150) NOT NULL,
    credential_value text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: api_keys; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.api_keys (
    organization_id uuid NOT NULL,
    key_name character varying(100) NOT NULL,
    key_hash character varying(255) NOT NULL,
    permissions text,
    expires_at timestamp with time zone,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: application_documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.application_documents (
    application_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: application_notes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.application_notes (
    application_id uuid NOT NULL,
    recruiter_id uuid NOT NULL,
    note_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: application_screening; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.application_screening (
    application_id uuid NOT NULL,
    screening_score double precision,
    screening_status character varying(50) NOT NULL,
    comments text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: application_stage_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.application_stage_history (
    application_id uuid NOT NULL,
    from_stage_id uuid,
    to_stage_id uuid NOT NULL,
    entered_at timestamp with time zone NOT NULL,
    left_at timestamp with time zone,
    changed_by uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: application_tags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.application_tags (
    application_id uuid NOT NULL,
    tag_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: approval_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.approval_history (
    hiring_request_id uuid NOT NULL,
    action_by uuid NOT NULL,
    action_type character varying(50) NOT NULL,
    action_at timestamp with time zone NOT NULL,
    comments text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: assessment_answers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assessment_answers (
    attempt_id uuid NOT NULL,
    question_id uuid NOT NULL,
    answer_text text NOT NULL,
    is_correct boolean NOT NULL,
    score double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: assessment_attempts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assessment_attempts (
    assessment_id uuid NOT NULL,
    candidate_id uuid NOT NULL,
    attempt_number integer NOT NULL,
    started_at timestamp with time zone NOT NULL,
    submitted_at timestamp with time zone,
    score double precision,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: assessment_questions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assessment_questions (
    assessment_template_id uuid NOT NULL,
    question_text text NOT NULL,
    question_type character varying(50) NOT NULL,
    points double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: assessment_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assessment_templates (
    organization_id uuid NOT NULL,
    template_name character varying(150) NOT NULL,
    content json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: assessments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assessments (
    job_id uuid NOT NULL,
    assessment_template_id uuid,
    assessment_name character varying(150) NOT NULL,
    description text,
    duration_minutes integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: assignment_submissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assignment_submissions (
    attempt_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    submitted_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_logs (
    user_id uuid,
    entity_type character varying(100) NOT NULL,
    entity_id uuid NOT NULL,
    action character varying(50) NOT NULL,
    previous_values json,
    new_values json,
    "timestamp" timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: background_check_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.background_check_items (
    bg_verification_id uuid NOT NULL,
    item_type character varying(50) NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: background_jobs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.background_jobs (
    job_type character varying(100) NOT NULL,
    status character varying(30) NOT NULL,
    payload json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: background_verifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.background_verifications (
    candidate_id uuid NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: benchmark_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.benchmark_results (
    dataset_id uuid NOT NULL,
    model_version_id uuid NOT NULL,
    score double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: branches; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.branches (
    organization_id uuid NOT NULL,
    branch_code character varying(30) NOT NULL,
    branch_name character varying(150) NOT NULL,
    location_id uuid,
    email character varying(255),
    phone character varying(30),
    manager_id uuid,
    is_head_office boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: broadcast_messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.broadcast_messages (
    organization_id uuid NOT NULL,
    message_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: business_units; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_units (
    organization_id uuid NOT NULL,
    unit_code character varying(30) NOT NULL,
    unit_name character varying(150) NOT NULL,
    description character varying(500),
    head_employee_id uuid,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: calendar_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.calendar_events (
    organization_id uuid NOT NULL,
    event_title character varying(200) NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: calendar_integrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.calendar_integrations (
    user_id uuid NOT NULL,
    provider_name character varying(50) NOT NULL,
    access_token text NOT NULL,
    refresh_token text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_achievements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_achievements (
    candidate_id uuid NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    issued_by character varying(255),
    issued_date date,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_activities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_activities (
    candidate_id uuid NOT NULL,
    action_by uuid NOT NULL,
    action_type character varying(100) NOT NULL,
    action_timestamp timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_addresses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_addresses (
    candidate_id uuid NOT NULL,
    address_type character varying(30) NOT NULL,
    address_line_1 character varying(255) NOT NULL,
    address_line_2 character varying(255),
    city_id uuid,
    state_id uuid,
    country_id uuid,
    postal_code character varying(30),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_ai_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_ai_profiles (
    candidate_id uuid NOT NULL,
    ai_calculated_experience_years double precision,
    ai_top_skills text,
    ai_profile_completeness double precision,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_ai_recommendations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_ai_recommendations (
    candidate_id uuid NOT NULL,
    recommended_job_id uuid NOT NULL,
    match_score double precision NOT NULL,
    explanation text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_ai_summaries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_ai_summaries (
    candidate_id uuid NOT NULL,
    summary_text text NOT NULL,
    key_highlights text,
    potential_risks text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_applications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_applications (
    job_id uuid NOT NULL,
    candidate_id uuid NOT NULL,
    application_status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_audit_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_audit_logs (
    candidate_id uuid NOT NULL,
    changed_by uuid NOT NULL,
    changed_at timestamp with time zone NOT NULL,
    field_name character varying(100) NOT NULL,
    old_value text,
    new_value text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_availability; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_availability (
    candidate_id uuid NOT NULL,
    availability_status character varying(50) NOT NULL,
    last_checked_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_blacklist; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_blacklist (
    organization_id uuid NOT NULL,
    candidate_id uuid NOT NULL,
    reason text NOT NULL,
    blacklisted_by uuid NOT NULL,
    blacklisted_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_certifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_certifications (
    candidate_id uuid NOT NULL,
    certification_id uuid,
    certification_name character varying(255) NOT NULL,
    issuing_organization character varying(255) NOT NULL,
    issue_date date,
    expiry_date date,
    credential_id character varying(100),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_consents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_consents (
    candidate_id uuid NOT NULL,
    consent_given boolean NOT NULL,
    consent_purpose character varying(255) NOT NULL,
    given_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_document_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_document_types (
    type_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_documents (
    candidate_id uuid NOT NULL,
    document_type_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    uploaded_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_education; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_education (
    candidate_id uuid NOT NULL,
    degree_id uuid,
    degree_name character varying(150) NOT NULL,
    field_of_study character varying(150),
    university_id uuid,
    university_name character varying(255) NOT NULL,
    start_year integer NOT NULL,
    end_year integer,
    grade character varying(30),
    is_completed boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_embeddings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_embeddings (
    candidate_id uuid NOT NULL,
    resume_id uuid,
    embedding public.vector(1536) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_emergency_contacts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_emergency_contacts (
    candidate_id uuid NOT NULL,
    contact_name character varying(150) NOT NULL,
    relationship character varying(50) NOT NULL,
    phone character varying(30) NOT NULL,
    email character varying(255),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_experience; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_experience (
    candidate_id uuid NOT NULL,
    company_name character varying(255) NOT NULL,
    designation_name character varying(150) NOT NULL,
    start_date date NOT NULL,
    end_date date,
    is_current boolean NOT NULL,
    description text,
    location character varying(150),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_languages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_languages (
    candidate_id uuid NOT NULL,
    language_id uuid NOT NULL,
    language_name character varying(100) NOT NULL,
    proficiency character varying(50),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_merge_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_merge_history (
    organization_id uuid NOT NULL,
    master_candidate_id uuid NOT NULL,
    merged_candidate_id uuid NOT NULL,
    merged_by uuid NOT NULL,
    merged_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_notes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_notes (
    candidate_id uuid NOT NULL,
    recruiter_id uuid NOT NULL,
    note_content text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_ownership; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_ownership (
    candidate_id uuid NOT NULL,
    recruiter_id uuid NOT NULL,
    assigned_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_patents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_patents (
    candidate_id uuid NOT NULL,
    title character varying(255) NOT NULL,
    patent_number character varying(100) NOT NULL,
    status character varying(50) NOT NULL,
    filed_date date,
    issued_date date,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_portfolios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_portfolios (
    candidate_id uuid NOT NULL,
    portfolio_name character varying(150) NOT NULL,
    portfolio_url character varying(255) NOT NULL,
    description text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_preferences; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_preferences (
    candidate_id uuid NOT NULL,
    notice_period_days integer NOT NULL,
    preferred_locations text,
    work_mode_id uuid,
    employment_type_id uuid,
    is_open_to_relocate boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_profiles (
    candidate_id uuid NOT NULL,
    gender character varying(20),
    date_of_birth date,
    marital_status character varying(30),
    nationality character varying(100),
    profile_photo character varying(500),
    summary text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_projects; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_projects (
    candidate_id uuid NOT NULL,
    project_name character varying(255) NOT NULL,
    role_in_project character varying(150),
    description text,
    project_url character varying(255),
    start_date date,
    end_date date,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_publications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_publications (
    candidate_id uuid NOT NULL,
    title character varying(255) NOT NULL,
    publisher character varying(255),
    publication_date date,
    publication_url character varying(255),
    description text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_references; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_references (
    candidate_id uuid NOT NULL,
    ref_name character varying(150) NOT NULL,
    relationship character varying(100) NOT NULL,
    company character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(30),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_resumes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_resumes (
    candidate_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_salary_expectations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_salary_expectations (
    candidate_id uuid NOT NULL,
    expected_salary double precision NOT NULL,
    currency_id uuid,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_skills; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_skills (
    candidate_id uuid NOT NULL,
    skill_id uuid NOT NULL,
    proficiency_level character varying(50),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_social_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_social_profiles (
    candidate_id uuid NOT NULL,
    social_platform character varying(50) NOT NULL,
    profile_url character varying(255) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_source_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_source_history (
    candidate_id uuid NOT NULL,
    source_id uuid NOT NULL,
    referrer_user_id uuid,
    captured_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_sources; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_sources (
    source_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_tags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_tags (
    candidate_id uuid NOT NULL,
    tag_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidate_timeline; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidate_timeline (
    candidate_id uuid NOT NULL,
    event_name character varying(150) NOT NULL,
    event_timestamp timestamp with time zone NOT NULL,
    details text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: candidates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidates (
    organization_id uuid NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(30),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: certifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.certifications (
    certification_name character varying(255) NOT NULL,
    issuing_organization character varying(255) NOT NULL,
    validity_period integer,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: cities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cities (
    state_id uuid NOT NULL,
    city_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: coding_tests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.coding_tests (
    assessment_id uuid NOT NULL,
    language character varying(50) NOT NULL,
    problem_statement text NOT NULL,
    test_cases json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: communication_audit_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.communication_audit_logs (
    organization_id uuid NOT NULL,
    details text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: communication_preferences; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.communication_preferences (
    user_id uuid NOT NULL,
    channel character varying(30) NOT NULL,
    is_enabled boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: compensation_revisions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.compensation_revisions (
    negotiation_id uuid NOT NULL,
    revised_base double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: conversation_messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.conversation_messages (
    thread_id uuid NOT NULL,
    sender_id uuid NOT NULL,
    message_text text NOT NULL,
    message_sequence integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: conversation_threads; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.conversation_threads (
    organization_id uuid NOT NULL,
    entity_type character varying(50) NOT NULL,
    entity_id uuid NOT NULL,
    subject character varying(200) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: countries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.countries (
    iso_code character varying(2) NOT NULL,
    country_name character varying(100) NOT NULL,
    currency_code character varying(3),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: currencies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.currencies (
    currency_code character varying(10) NOT NULL,
    currency_name character varying(100) NOT NULL,
    currency_symbol character varying(20),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: dashboard_layouts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dashboard_layouts (
    dashboard_id uuid NOT NULL,
    layout_json json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: dashboard_widgets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dashboard_widgets (
    dashboard_id uuid NOT NULL,
    widget_name character varying(150) NOT NULL,
    widget_type character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: dashboards; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dashboards (
    organization_id uuid NOT NULL,
    dashboard_name character varying(150) NOT NULL,
    description text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: degrees; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.degrees (
    degree_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: delivery_metrics; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.delivery_metrics (
    organization_id uuid NOT NULL,
    metric_name character varying(100) NOT NULL,
    metric_value double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: departments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.departments (
    organization_id uuid NOT NULL,
    department_code character varying(50) NOT NULL,
    department_name character varying(150) NOT NULL,
    parent_department_id uuid,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: designations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.designations (
    organization_id uuid NOT NULL,
    designation_code character varying(50) NOT NULL,
    designation_name character varying(150) NOT NULL,
    job_family_id uuid,
    level character varying(30),
    grade character varying(30),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: document_chunks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_chunks (
    document_id uuid NOT NULL,
    chunk_text text NOT NULL,
    chunk_sequence integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: document_embeddings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_embeddings (
    chunk_id uuid NOT NULL,
    embedding public.vector(1536) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: document_verifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_verifications (
    candidate_id uuid NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: duplicate_candidates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.duplicate_candidates (
    organization_id uuid NOT NULL,
    primary_candidate_id uuid NOT NULL,
    duplicate_candidate_id uuid NOT NULL,
    match_score double precision NOT NULL,
    detection_reason character varying(255),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: email_attachments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_attachments (
    email_queue_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: email_delivery_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_delivery_logs (
    email_queue_id uuid NOT NULL,
    delivered_at timestamp with time zone NOT NULL,
    status_message text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: email_queue; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_queue (
    recipient_email character varying(255) NOT NULL,
    subject character varying(255) NOT NULL,
    body_html text NOT NULL,
    status character varying(30) NOT NULL,
    scheduled_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: email_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_templates (
    organization_id uuid NOT NULL,
    template_name character varying(150) NOT NULL,
    subject character varying(255) NOT NULL,
    body_html text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: email_verifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_verifications (
    user_id uuid NOT NULL,
    verification_token character varying(255) NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    verified_at timestamp with time zone,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: employee_conversion_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employee_conversion_logs (
    candidate_id uuid NOT NULL,
    converted_by uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: employee_conversions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employee_conversions (
    candidate_id uuid NOT NULL,
    employee_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: employment_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employment_types (
    type_name character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: environment_variables; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.environment_variables (
    variable_key character varying(150) NOT NULL,
    variable_value text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: evaluation_criteria; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.evaluation_criteria (
    organization_id uuid NOT NULL,
    criterion_name character varying(150) NOT NULL,
    description text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: evaluation_datasets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.evaluation_datasets (
    dataset_name character varying(150) NOT NULL,
    description text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: evaluation_scores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.evaluation_scores (
    interview_feedback_id uuid NOT NULL,
    evaluation_criterion_id uuid NOT NULL,
    score double precision NOT NULL,
    comments text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: experience_levels; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.experience_levels (
    level_name character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: feature_flags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.feature_flags (
    flag_code character varying(100) NOT NULL,
    is_enabled boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: file_metadata; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.file_metadata (
    organization_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    file_size integer NOT NULL,
    mime_type character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: file_versions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.file_versions (
    file_id uuid NOT NULL,
    version_number integer NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: fine_tuning_datasets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fine_tuning_datasets (
    dataset_name character varying(150) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: hiring_completions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hiring_completions (
    candidate_id uuid NOT NULL,
    completed_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: hiring_plans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hiring_plans (
    organization_id uuid NOT NULL,
    plan_name character varying(150) NOT NULL,
    budget double precision NOT NULL,
    currency_id uuid,
    start_date date NOT NULL,
    end_date date NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: hiring_request_attachments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hiring_request_attachments (
    hiring_request_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: hiring_request_comments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hiring_request_comments (
    hiring_request_id uuid NOT NULL,
    commented_by uuid NOT NULL,
    comment_text text NOT NULL,
    commented_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: hiring_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hiring_requests (
    organization_id uuid NOT NULL,
    hiring_plan_id uuid,
    requisition_number character varying(50) NOT NULL,
    title character varying(200) NOT NULL,
    department_id uuid NOT NULL,
    designation_id uuid NOT NULL,
    requested_by uuid NOT NULL,
    open_positions integer NOT NULL,
    target_date date,
    status character varying(30) NOT NULL,
    justification text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: holiday_calendars; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.holiday_calendars (
    organization_id uuid NOT NULL,
    calendar_name character varying(150) NOT NULL,
    year integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: holidays; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.holidays (
    holiday_calendar_id uuid NOT NULL,
    holiday_date date NOT NULL,
    holiday_name character varying(150) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: human_reviews; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.human_reviews (
    execution_id uuid NOT NULL,
    reviewer_id uuid NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: industries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.industries (
    industry_code character varying(50) NOT NULL,
    industry_name character varying(150) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: integration_configurations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.integration_configurations (
    organization_id uuid NOT NULL,
    integration_id uuid NOT NULL,
    config_payload json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: integration_registries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.integration_registries (
    integration_name character varying(150) NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: internal_comments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.internal_comments (
    entity_type character varying(50) NOT NULL,
    entity_id uuid NOT NULL,
    author_id uuid NOT NULL,
    comment_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_analytics; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_analytics (
    organization_id uuid NOT NULL,
    metric_name character varying(100) NOT NULL,
    metric_value double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_attachments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_attachments (
    interview_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_audit_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_audit_logs (
    interview_id uuid NOT NULL,
    action character varying(100) NOT NULL,
    action_by uuid NOT NULL,
    action_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_calendar_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_calendar_events (
    interview_id uuid NOT NULL,
    calendar_provider character varying(50) NOT NULL,
    event_id character varying(255) NOT NULL,
    meeting_link character varying(500),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_cancellations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_cancellations (
    interview_id uuid NOT NULL,
    cancelled_by uuid NOT NULL,
    cancelled_at timestamp with time zone NOT NULL,
    reason text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_decisions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_decisions (
    interview_id uuid NOT NULL,
    decision character varying(50) NOT NULL,
    decision_by uuid NOT NULL,
    decision_at timestamp with time zone NOT NULL,
    comments text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_feedback; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_feedback (
    interview_id uuid NOT NULL,
    interviewer_id uuid NOT NULL,
    rating integer,
    comments text,
    submitted_at timestamp with time zone,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_notifications (
    interview_id uuid NOT NULL,
    notification_type character varying(50) NOT NULL,
    sent_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_panel_members; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_panel_members (
    panel_id uuid NOT NULL,
    panel_member_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_panels; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_panels (
    interview_id uuid NOT NULL,
    panel_name character varying(150) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_participants; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_participants (
    interview_id uuid NOT NULL,
    participant_type character varying(50) NOT NULL,
    user_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_plans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_plans (
    job_id uuid NOT NULL,
    plan_name character varying(150) NOT NULL,
    description text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_recordings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_recordings (
    interview_id uuid NOT NULL,
    recording_url character varying(500) NOT NULL,
    duration_seconds integer,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_reschedules; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_reschedules (
    interview_id uuid NOT NULL,
    rescheduled_by uuid NOT NULL,
    rescheduled_at timestamp with time zone NOT NULL,
    previous_start_time timestamp with time zone NOT NULL,
    new_start_time timestamp with time zone NOT NULL,
    reason text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_rounds; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_rounds (
    interview_plan_id uuid NOT NULL,
    round_name character varying(100) NOT NULL,
    sequence_number integer NOT NULL,
    duration_minutes integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_schedules; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_schedules (
    interview_id uuid NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL,
    timezone character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_scorecards; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_scorecards (
    interview_id uuid NOT NULL,
    overall_score double precision NOT NULL,
    recommendation character varying(50) NOT NULL,
    comments text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_stage_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_stage_templates (
    organization_id uuid NOT NULL,
    template_name character varying(100) NOT NULL,
    description text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_timelines; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_timelines (
    interview_id uuid NOT NULL,
    event_name character varying(150) NOT NULL,
    event_time timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interview_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interview_types (
    type_name character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interviewer_assignments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interviewer_assignments (
    job_id uuid NOT NULL,
    interviewer_id uuid NOT NULL,
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: interviews; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.interviews (
    candidate_application_id uuid NOT NULL,
    interview_round_id uuid NOT NULL,
    interview_type_id uuid NOT NULL,
    scheduled_start timestamp with time zone NOT NULL,
    scheduled_end timestamp with time zone NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_benefits; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_benefits (
    job_id uuid NOT NULL,
    benefit_text character varying(255) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_families; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_families (
    family_code character varying(50) NOT NULL,
    family_name character varying(150) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_hiring_managers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_hiring_managers (
    job_id uuid NOT NULL,
    hiring_manager_id uuid NOT NULL,
    is_primary boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_locations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_locations (
    job_id uuid NOT NULL,
    location_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_publications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_publications (
    job_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    external_job_id character varying(100),
    published_at timestamp with time zone NOT NULL,
    expires_at timestamp with time zone,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_qualifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_qualifications (
    job_id uuid NOT NULL,
    degree_id uuid,
    qualification_text character varying(255) NOT NULL,
    is_mandatory boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_queues; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_queues (
    queue_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_recruiters; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_recruiters (
    job_id uuid NOT NULL,
    recruiter_id uuid NOT NULL,
    is_primary boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_responsibilities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_responsibilities (
    job_id uuid NOT NULL,
    responsibility_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_salary_ranges; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_salary_ranges (
    job_id uuid NOT NULL,
    minimum_salary double precision NOT NULL,
    maximum_salary double precision NOT NULL,
    currency_id uuid,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_skills; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_skills (
    job_id uuid NOT NULL,
    skill_id uuid NOT NULL,
    is_mandatory boolean NOT NULL,
    proficiency_required character varying(50),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_templates (
    organization_id uuid NOT NULL,
    title character varying(200) NOT NULL,
    description text NOT NULL,
    requirements text,
    benefits text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: job_versions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_versions (
    job_id uuid NOT NULL,
    version_number integer NOT NULL,
    title character varying(200) NOT NULL,
    description text NOT NULL,
    changed_at timestamp with time zone NOT NULL,
    changed_by uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: jobs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.jobs (
    organization_id uuid NOT NULL,
    job_code character varying(50) NOT NULL,
    title character varying(200) NOT NULL,
    department_id uuid,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: joining_audits; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.joining_audits (
    candidate_id uuid NOT NULL,
    checks_passed boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: joining_confirmations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.joining_confirmations (
    offer_id uuid NOT NULL,
    expected_joining_date date NOT NULL,
    status character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: knowledge_bases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.knowledge_bases (
    kb_name character varying(150) NOT NULL,
    description text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: knowledge_collections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.knowledge_collections (
    kb_id uuid NOT NULL,
    collection_name character varying(150) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: knowledge_documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.knowledge_documents (
    collection_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: languages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.languages (
    language_code character varying(10) NOT NULL,
    language_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: locations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.locations (
    organization_id uuid NOT NULL,
    location_name character varying(150) NOT NULL,
    city_id uuid,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: login_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.login_history (
    user_id uuid NOT NULL,
    login_at timestamp with time zone NOT NULL,
    logout_at timestamp with time zone,
    ip_address character varying(45),
    browser character varying(100),
    operating_system character varying(100),
    login_status character varying(30) NOT NULL,
    failure_reason character varying(255),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: medical_verifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.medical_verifications (
    candidate_id uuid NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: meeting_invitations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.meeting_invitations (
    calendar_event_id uuid NOT NULL,
    invitee_email character varying(255) NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: mentions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mentions (
    comment_id uuid,
    message_id uuid,
    mentioned_user_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: message_attachments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.message_attachments (
    message_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: messaging_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.messaging_templates (
    organization_id uuid NOT NULL,
    template_name character varying(150) NOT NULL,
    body text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: mfa_configurations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mfa_configurations (
    user_id uuid NOT NULL,
    mfa_type character varying(30) NOT NULL,
    secret_key text NOT NULL,
    enabled_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: mfa_recovery_codes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mfa_recovery_codes (
    user_id uuid NOT NULL,
    recovery_code_hash character varying(255) NOT NULL,
    used_at timestamp with time zone,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: notification_delivery_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notification_delivery_logs (
    notification_id uuid NOT NULL,
    channel character varying(30) NOT NULL,
    delivered_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: notification_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notification_events (
    event_code character varying(100) NOT NULL,
    event_name character varying(150) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: notification_queue; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notification_queue (
    notification_id uuid NOT NULL,
    status character varying(30) NOT NULL,
    scheduled_at timestamp with time zone NOT NULL,
    retry_count integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: notification_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notification_templates (
    organization_id uuid NOT NULL,
    template_code character varying(50) NOT NULL,
    template_name character varying(150) NOT NULL,
    content text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    user_id uuid NOT NULL,
    status character varying(30) NOT NULL,
    title character varying(200) NOT NULL,
    body text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: object_storage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.object_storage (
    provider character varying(50) NOT NULL,
    bucket_name character varying(255) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offer_acceptance; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer_acceptance (
    offer_id uuid NOT NULL,
    accepted_at timestamp with time zone NOT NULL,
    ip_address character varying(45),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offer_approval_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer_approval_history (
    offer_id uuid NOT NULL,
    action_by uuid NOT NULL,
    action_type character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offer_approvals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer_approvals (
    offer_id uuid NOT NULL,
    approver_id uuid NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offer_attachments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer_attachments (
    offer_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offer_audits; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer_audits (
    offer_id uuid NOT NULL,
    details text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offer_compensation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer_compensation (
    offer_id uuid NOT NULL,
    base_salary double precision NOT NULL,
    allowances json,
    bonus_percentage double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offer_documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer_documents (
    offer_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offer_negotiations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer_negotiations (
    offer_id uuid NOT NULL,
    negotiator_type character varying(50) NOT NULL,
    comments text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offer_rejections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer_rejections (
    offer_id uuid NOT NULL,
    rejected_at timestamp with time zone NOT NULL,
    reason text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offer_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer_templates (
    organization_id uuid NOT NULL,
    template_name character varying(150) NOT NULL,
    content json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offer_versions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer_versions (
    offer_id uuid NOT NULL,
    version_number integer NOT NULL,
    details json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: offers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offers (
    candidate_application_id uuid NOT NULL,
    offered_designation_id uuid NOT NULL,
    issue_date date NOT NULL,
    expiry_date date NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: onboarding_checklists; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.onboarding_checklists (
    candidate_id uuid NOT NULL,
    task_count integer NOT NULL,
    completed_count integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: onboarding_document_reviews; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.onboarding_document_reviews (
    submission_id uuid NOT NULL,
    reviewed_by uuid NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: onboarding_document_submissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.onboarding_document_submissions (
    candidate_id uuid NOT NULL,
    onboarding_document_id uuid NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: onboarding_documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.onboarding_documents (
    organization_id uuid NOT NULL,
    document_name character varying(150) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: onboarding_plans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.onboarding_plans (
    organization_id uuid NOT NULL,
    plan_name character varying(150) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: onboarding_task_assignments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.onboarding_task_assignments (
    candidate_id uuid NOT NULL,
    onboarding_task_id uuid NOT NULL,
    owner_id uuid NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: onboarding_tasks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.onboarding_tasks (
    onboarding_plan_id uuid NOT NULL,
    task_name character varying(150) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: organization_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.organization_settings (
    organization_id uuid NOT NULL,
    setting_key character varying(150) NOT NULL,
    setting_value text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: organizations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.organizations (
    organization_code character varying(50) NOT NULL,
    legal_name character varying(255) NOT NULL,
    display_name character varying(255) NOT NULL,
    registration_number character varying(100),
    tax_number character varying(100),
    industry_id uuid NOT NULL,
    website character varying(255),
    email character varying(255),
    phone character varying(30),
    subscription_plan character varying(50) NOT NULL,
    subscription_status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: password_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.password_history (
    user_id uuid NOT NULL,
    password_hash text NOT NULL,
    changed_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.password_reset_tokens (
    user_id uuid NOT NULL,
    token_hash character varying(255) NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    used_at timestamp with time zone,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: permission_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permission_groups (
    group_name character varying(100) NOT NULL,
    description character varying(255),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permissions (
    permission_code character varying(100) NOT NULL,
    permission_name character varying(100) NOT NULL,
    module character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: pipeline_stage_mapping; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pipeline_stage_mapping (
    pipeline_id uuid NOT NULL,
    stage_id uuid NOT NULL,
    sequence_number integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: probation_setups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.probation_setups (
    candidate_id uuid NOT NULL,
    duration_months integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: prompt_evaluations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prompt_evaluations (
    version_id uuid NOT NULL,
    score double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: prompt_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prompt_templates (
    template_name character varying(150) NOT NULL,
    system_prompt text NOT NULL,
    user_prompt text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: prompt_variables; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prompt_variables (
    template_id uuid NOT NULL,
    variable_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: prompt_versions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prompt_versions (
    template_id uuid NOT NULL,
    version_number integer NOT NULL,
    system_prompt text NOT NULL,
    user_prompt text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: publication_channels; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publication_channels (
    channel_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: publication_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.publication_history (
    job_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    action character varying(50) NOT NULL,
    action_at timestamp with time zone NOT NULL,
    action_by uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: push_delivery_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.push_delivery_logs (
    push_notification_id uuid NOT NULL,
    delivered_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: push_notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.push_notifications (
    user_id uuid NOT NULL,
    title character varying(200) NOT NULL,
    body text NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: rag_citations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rag_citations (
    retrieval_result_id uuid NOT NULL,
    citation_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: rag_retrieval_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rag_retrieval_results (
    session_id uuid NOT NULL,
    chunk_id uuid NOT NULL,
    score double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: rag_sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rag_sessions (
    user_id uuid NOT NULL,
    session_query text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: recruiter_workloads; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recruiter_workloads (
    organization_id uuid NOT NULL,
    recruiter_id uuid NOT NULL,
    active_jobs_count integer NOT NULL,
    allocated_capacity integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: recruitment_audit_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recruitment_audit_logs (
    organization_id uuid NOT NULL,
    job_id uuid,
    application_id uuid,
    action character varying(100) NOT NULL,
    action_by uuid NOT NULL,
    action_at timestamp with time zone NOT NULL,
    details text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: recruitment_closures; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recruitment_closures (
    job_id uuid NOT NULL,
    closed_by uuid NOT NULL,
    closed_at timestamp with time zone NOT NULL,
    closure_reason character varying(255) NOT NULL,
    total_hires integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: recruitment_metrics; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recruitment_metrics (
    organization_id uuid NOT NULL,
    metric_name character varying(100) NOT NULL,
    metric_value double precision NOT NULL,
    calculated_date date NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: recruitment_pipelines; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recruitment_pipelines (
    organization_id uuid NOT NULL,
    pipeline_name character varying(150) NOT NULL,
    description character varying(500),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: recruitment_stages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recruitment_stages (
    organization_id uuid NOT NULL,
    stage_name character varying(100) NOT NULL,
    sequence_number integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: refresh_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.refresh_tokens (
    token_hash character varying(500) NOT NULL,
    session_id uuid NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    revoked boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: report_definitions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.report_definitions (
    organization_id uuid NOT NULL,
    report_name character varying(150) NOT NULL,
    query_template text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: report_execution_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.report_execution_logs (
    scheduled_report_id uuid NOT NULL,
    executed_at timestamp with time zone NOT NULL,
    status character varying(30) NOT NULL,
    file_path character varying(500),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: report_parameters; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.report_parameters (
    report_definition_id uuid NOT NULL,
    parameter_name character varying(100) NOT NULL,
    parameter_type character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: requisition_approvals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.requisition_approvals (
    hiring_request_id uuid NOT NULL,
    approver_id uuid NOT NULL,
    approval_level integer NOT NULL,
    status character varying(30) NOT NULL,
    comments text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: resume_parsing_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.resume_parsing_history (
    candidate_id uuid NOT NULL,
    resume_id uuid NOT NULL,
    parsed_at timestamp with time zone NOT NULL,
    parser_status character varying(30) NOT NULL,
    parsed_data json,
    error_message text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: resume_versions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.resume_versions (
    candidate_id uuid NOT NULL,
    resume_id uuid NOT NULL,
    version_number integer NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.role_permissions (
    role_id uuid NOT NULL,
    permission_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    organization_id uuid NOT NULL,
    role_code character varying(50) NOT NULL,
    role_name character varying(100) NOT NULL,
    is_system_role boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: salary_bands; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salary_bands (
    organization_id uuid NOT NULL,
    band_code character varying(50) NOT NULL,
    minimum_salary double precision NOT NULL,
    maximum_salary double precision NOT NULL,
    currency_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: scheduled_jobs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.scheduled_jobs (
    job_name character varying(150) NOT NULL,
    cron_expression character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: scheduled_reports; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.scheduled_reports (
    report_definition_id uuid NOT NULL,
    cron_expression character varying(50) NOT NULL,
    recipient_emails text NOT NULL,
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: scheduler_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.scheduler_history (
    scheduled_job_id uuid NOT NULL,
    run_at timestamp with time zone NOT NULL,
    status character varying(30) NOT NULL,
    error_log text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: security_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.security_events (
    user_id uuid,
    event_type character varying(100) NOT NULL,
    severity character varying(30) NOT NULL,
    description text NOT NULL,
    event_time timestamp with time zone NOT NULL,
    resolved_at timestamp with time zone,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sessions (
    session_token character varying(500) NOT NULL,
    user_id uuid NOT NULL,
    device_name character varying(255),
    device_type character varying(50),
    operating_system character varying(100),
    browser character varying(100),
    ip_address character varying(45),
    login_time timestamp with time zone NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    revoked_at timestamp with time zone,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: shifts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.shifts (
    organization_id uuid NOT NULL,
    shift_name character varying(100) NOT NULL,
    start_time character varying(30) NOT NULL,
    end_time character varying(30) NOT NULL,
    is_flexible boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: skills; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.skills (
    skill_name character varying(150) NOT NULL,
    category character varying(50),
    description character varying(500),
    is_ai_generated boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: sms_queue; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sms_queue (
    recipient_phone character varying(30) NOT NULL,
    message text NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: stage_sla; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stage_sla (
    pipeline_id uuid NOT NULL,
    stage_id uuid NOT NULL,
    max_days integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: states; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.states (
    country_id uuid NOT NULL,
    state_code character varying(10) NOT NULL,
    state_name character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: storage_quotas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.storage_quotas (
    organization_id uuid NOT NULL,
    max_bytes double precision NOT NULL,
    used_bytes double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: system_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.system_settings (
    setting_key character varying(150) NOT NULL,
    setting_value text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: tenant_preferences; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tenant_preferences (
    organization_id uuid NOT NULL,
    preference_key character varying(100) NOT NULL,
    preference_value text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: timezones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.timezones (
    timezone_code character varying(100) NOT NULL,
    display_name character varying(255) NOT NULL,
    utc_offset character varying(30),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: token_usage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.token_usage (
    execution_id uuid NOT NULL,
    prompt_tokens integer NOT NULL,
    completion_tokens integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: universities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.universities (
    university_name character varying(255) NOT NULL,
    country_id uuid,
    website character varying(255),
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: user_devices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_devices (
    user_id uuid NOT NULL,
    device_token character varying(255) NOT NULL,
    device_type character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: user_preferences; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_preferences (
    user_id uuid NOT NULL,
    language character varying(10),
    timezone character varying(100),
    theme character varying(30),
    notification_preferences json,
    dashboard_layout json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: user_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_profiles (
    user_id uuid NOT NULL,
    first_name character varying(100) NOT NULL,
    middle_name character varying(100),
    last_name character varying(100) NOT NULL,
    profile_photo character varying(500),
    gender character varying(20),
    date_of_birth timestamp with time zone,
    timezone_id uuid,
    language_id uuid,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_roles (
    user_id uuid NOT NULL,
    role_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    organization_id uuid NOT NULL,
    username character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(30),
    password_hash text NOT NULL,
    account_type character varying(30) NOT NULL,
    account_status character varying(30) NOT NULL,
    email_verified boolean NOT NULL,
    mfa_enabled boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: webhook_deliveries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.webhook_deliveries (
    subscription_id uuid NOT NULL,
    event_type character varying(100) NOT NULL,
    response_status integer NOT NULL,
    response_body text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: webhook_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.webhook_events (
    subscription_id uuid NOT NULL,
    event_type character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: webhook_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.webhook_logs (
    webhook_id uuid NOT NULL,
    response_code integer NOT NULL,
    response_body text,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: webhook_registries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.webhook_registries (
    organization_id uuid NOT NULL,
    target_url character varying(500) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: webhook_subscriptions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.webhook_subscriptions (
    organization_id uuid NOT NULL,
    target_url character varying(500) NOT NULL,
    secret_token character varying(255) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: welcome_kits; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.welcome_kits (
    candidate_id uuid NOT NULL,
    kit_type character varying(100) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: whatsapp_queue; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.whatsapp_queue (
    recipient_phone character varying(30) NOT NULL,
    message text NOT NULL,
    status character varying(30) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: widget_configurations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.widget_configurations (
    widget_id uuid NOT NULL,
    config_json json,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: widget_data_queries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.widget_data_queries (
    widget_id uuid NOT NULL,
    query_text text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: work_modes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.work_modes (
    mode_name character varying(50) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone NOT NULL,
    updated_by uuid,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    version integer NOT NULL
);


--
-- Name: activity_feed activity_feed_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_feed
    ADD CONSTRAINT activity_feed_pkey PRIMARY KEY (id);


--
-- Name: activity_logs activity_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_pkey PRIMARY KEY (id);


--
-- Name: ai_agent_capabilities ai_agent_capabilities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_agent_capabilities
    ADD CONSTRAINT ai_agent_capabilities_pkey PRIMARY KEY (id);


--
-- Name: ai_agents ai_agents_agent_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_agents
    ADD CONSTRAINT ai_agents_agent_code_key UNIQUE (agent_code);


--
-- Name: ai_agents ai_agents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_agents
    ADD CONSTRAINT ai_agents_pkey PRIMARY KEY (id);


--
-- Name: ai_audit_logs ai_audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_audit_logs
    ADD CONSTRAINT ai_audit_logs_pkey PRIMARY KEY (id);


--
-- Name: ai_behavior_analysis ai_behavior_analysis_interview_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_behavior_analysis
    ADD CONSTRAINT ai_behavior_analysis_interview_id_key UNIQUE (interview_id);


--
-- Name: ai_behavior_analysis ai_behavior_analysis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_behavior_analysis
    ADD CONSTRAINT ai_behavior_analysis_pkey PRIMARY KEY (id);


--
-- Name: ai_candidate_feedback ai_candidate_feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_candidate_feedback
    ADD CONSTRAINT ai_candidate_feedback_pkey PRIMARY KEY (id);


--
-- Name: ai_candidate_rankings ai_candidate_rankings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_candidate_rankings
    ADD CONSTRAINT ai_candidate_rankings_pkey PRIMARY KEY (id);


--
-- Name: ai_conversations ai_conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_conversations
    ADD CONSTRAINT ai_conversations_pkey PRIMARY KEY (id);


--
-- Name: ai_cost_tracking ai_cost_tracking_execution_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_cost_tracking
    ADD CONSTRAINT ai_cost_tracking_execution_id_key UNIQUE (execution_id);


--
-- Name: ai_cost_tracking ai_cost_tracking_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_cost_tracking
    ADD CONSTRAINT ai_cost_tracking_pkey PRIMARY KEY (id);


--
-- Name: ai_decision_support ai_decision_support_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_decision_support
    ADD CONSTRAINT ai_decision_support_pkey PRIMARY KEY (id);


--
-- Name: ai_decision_support ai_decision_support_recommendation_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_decision_support
    ADD CONSTRAINT ai_decision_support_recommendation_id_key UNIQUE (recommendation_id);


--
-- Name: ai_execution_logs ai_execution_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_execution_logs
    ADD CONSTRAINT ai_execution_logs_pkey PRIMARY KEY (id);


--
-- Name: ai_executions ai_executions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_executions
    ADD CONSTRAINT ai_executions_pkey PRIMARY KEY (id);


--
-- Name: ai_feedback ai_feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_feedback
    ADD CONSTRAINT ai_feedback_pkey PRIMARY KEY (id);


--
-- Name: ai_interview_analysis ai_interview_analysis_interview_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_interview_analysis
    ADD CONSTRAINT ai_interview_analysis_interview_id_key UNIQUE (interview_id);


--
-- Name: ai_interview_analysis ai_interview_analysis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_interview_analysis
    ADD CONSTRAINT ai_interview_analysis_pkey PRIMARY KEY (id);


--
-- Name: ai_interview_scores ai_interview_scores_interview_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_interview_scores
    ADD CONSTRAINT ai_interview_scores_interview_id_key UNIQUE (interview_id);


--
-- Name: ai_interview_scores ai_interview_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_interview_scores
    ADD CONSTRAINT ai_interview_scores_pkey PRIMARY KEY (id);


--
-- Name: ai_interview_summary ai_interview_summary_interview_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_interview_summary
    ADD CONSTRAINT ai_interview_summary_interview_id_key UNIQUE (interview_id);


--
-- Name: ai_interview_summary ai_interview_summary_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_interview_summary
    ADD CONSTRAINT ai_interview_summary_pkey PRIMARY KEY (id);


--
-- Name: ai_job_recommendations ai_job_recommendations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_job_recommendations
    ADD CONSTRAINT ai_job_recommendations_pkey PRIMARY KEY (id);


--
-- Name: ai_memory ai_memory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_memory
    ADD CONSTRAINT ai_memory_pkey PRIMARY KEY (id);


--
-- Name: ai_messages ai_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_messages
    ADD CONSTRAINT ai_messages_pkey PRIMARY KEY (id);


--
-- Name: ai_metrics ai_metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_metrics
    ADD CONSTRAINT ai_metrics_pkey PRIMARY KEY (id);


--
-- Name: ai_model_configurations ai_model_configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_model_configurations
    ADD CONSTRAINT ai_model_configurations_pkey PRIMARY KEY (id);


--
-- Name: ai_model_providers ai_model_providers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_model_providers
    ADD CONSTRAINT ai_model_providers_pkey PRIMARY KEY (id);


--
-- Name: ai_model_providers ai_model_providers_provider_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_model_providers
    ADD CONSTRAINT ai_model_providers_provider_name_key UNIQUE (provider_name);


--
-- Name: ai_model_versions ai_model_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_model_versions
    ADD CONSTRAINT ai_model_versions_pkey PRIMARY KEY (id);


--
-- Name: ai_models ai_models_model_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_models
    ADD CONSTRAINT ai_models_model_code_key UNIQUE (model_code);


--
-- Name: ai_models ai_models_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_models
    ADD CONSTRAINT ai_models_pkey PRIMARY KEY (id);


--
-- Name: ai_recommendations ai_recommendations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_recommendations
    ADD CONSTRAINT ai_recommendations_pkey PRIMARY KEY (id);


--
-- Name: ai_recruitment_insights ai_recruitment_insights_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_recruitment_insights
    ADD CONSTRAINT ai_recruitment_insights_pkey PRIMARY KEY (id);


--
-- Name: ai_requests ai_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_requests
    ADD CONSTRAINT ai_requests_pkey PRIMARY KEY (id);


--
-- Name: ai_responses ai_responses_execution_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_responses
    ADD CONSTRAINT ai_responses_execution_id_key UNIQUE (execution_id);


--
-- Name: ai_responses ai_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_responses
    ADD CONSTRAINT ai_responses_pkey PRIMARY KEY (id);


--
-- Name: ai_screening_results ai_screening_results_application_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_screening_results
    ADD CONSTRAINT ai_screening_results_application_id_key UNIQUE (application_id);


--
-- Name: ai_screening_results ai_screening_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_screening_results
    ADD CONSTRAINT ai_screening_results_pkey PRIMARY KEY (id);


--
-- Name: ai_summaries ai_summaries_conversation_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_summaries
    ADD CONSTRAINT ai_summaries_conversation_id_key UNIQUE (conversation_id);


--
-- Name: ai_summaries ai_summaries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_summaries
    ADD CONSTRAINT ai_summaries_pkey PRIMARY KEY (id);


--
-- Name: ai_tool_executions ai_tool_executions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_tool_executions
    ADD CONSTRAINT ai_tool_executions_pkey PRIMARY KEY (id);


--
-- Name: ai_tool_permissions ai_tool_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_tool_permissions
    ADD CONSTRAINT ai_tool_permissions_pkey PRIMARY KEY (id);


--
-- Name: ai_tools ai_tools_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_tools
    ADD CONSTRAINT ai_tools_pkey PRIMARY KEY (id);


--
-- Name: ai_tools ai_tools_tool_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_tools
    ADD CONSTRAINT ai_tools_tool_code_key UNIQUE (tool_code);


--
-- Name: ai_workflow_steps ai_workflow_steps_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_workflow_steps
    ADD CONSTRAINT ai_workflow_steps_pkey PRIMARY KEY (id);


--
-- Name: ai_workflows ai_workflows_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_workflows
    ADD CONSTRAINT ai_workflows_pkey PRIMARY KEY (id);


--
-- Name: ai_workflows ai_workflows_workflow_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_workflows
    ADD CONSTRAINT ai_workflows_workflow_name_key UNIQUE (workflow_name);


--
-- Name: announcements announcements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.announcements
    ADD CONSTRAINT announcements_pkey PRIMARY KEY (id);


--
-- Name: api_credentials api_credentials_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.api_credentials
    ADD CONSTRAINT api_credentials_pkey PRIMARY KEY (id);


--
-- Name: api_keys api_keys_key_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.api_keys
    ADD CONSTRAINT api_keys_key_hash_key UNIQUE (key_hash);


--
-- Name: api_keys api_keys_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.api_keys
    ADD CONSTRAINT api_keys_pkey PRIMARY KEY (id);


--
-- Name: application_documents application_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_documents
    ADD CONSTRAINT application_documents_pkey PRIMARY KEY (id);


--
-- Name: application_notes application_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_notes
    ADD CONSTRAINT application_notes_pkey PRIMARY KEY (id);


--
-- Name: application_screening application_screening_application_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_screening
    ADD CONSTRAINT application_screening_application_id_key UNIQUE (application_id);


--
-- Name: application_screening application_screening_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_screening
    ADD CONSTRAINT application_screening_pkey PRIMARY KEY (id);


--
-- Name: application_stage_history application_stage_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_stage_history
    ADD CONSTRAINT application_stage_history_pkey PRIMARY KEY (id);


--
-- Name: application_tags application_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_tags
    ADD CONSTRAINT application_tags_pkey PRIMARY KEY (id);


--
-- Name: approval_history approval_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.approval_history
    ADD CONSTRAINT approval_history_pkey PRIMARY KEY (id);


--
-- Name: assessment_answers assessment_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment_answers
    ADD CONSTRAINT assessment_answers_pkey PRIMARY KEY (id);


--
-- Name: assessment_attempts assessment_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment_attempts
    ADD CONSTRAINT assessment_attempts_pkey PRIMARY KEY (id);


--
-- Name: assessment_questions assessment_questions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment_questions
    ADD CONSTRAINT assessment_questions_pkey PRIMARY KEY (id);


--
-- Name: assessment_templates assessment_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment_templates
    ADD CONSTRAINT assessment_templates_pkey PRIMARY KEY (id);


--
-- Name: assessments assessments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessments
    ADD CONSTRAINT assessments_pkey PRIMARY KEY (id);


--
-- Name: assignment_submissions assignment_submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assignment_submissions
    ADD CONSTRAINT assignment_submissions_pkey PRIMARY KEY (id);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: background_check_items background_check_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.background_check_items
    ADD CONSTRAINT background_check_items_pkey PRIMARY KEY (id);


--
-- Name: background_jobs background_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.background_jobs
    ADD CONSTRAINT background_jobs_pkey PRIMARY KEY (id);


--
-- Name: background_verifications background_verifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.background_verifications
    ADD CONSTRAINT background_verifications_pkey PRIMARY KEY (id);


--
-- Name: benchmark_results benchmark_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.benchmark_results
    ADD CONSTRAINT benchmark_results_pkey PRIMARY KEY (id);


--
-- Name: branches branches_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.branches
    ADD CONSTRAINT branches_pkey PRIMARY KEY (id);


--
-- Name: broadcast_messages broadcast_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.broadcast_messages
    ADD CONSTRAINT broadcast_messages_pkey PRIMARY KEY (id);


--
-- Name: business_units business_units_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_units
    ADD CONSTRAINT business_units_pkey PRIMARY KEY (id);


--
-- Name: calendar_events calendar_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.calendar_events
    ADD CONSTRAINT calendar_events_pkey PRIMARY KEY (id);


--
-- Name: calendar_integrations calendar_integrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.calendar_integrations
    ADD CONSTRAINT calendar_integrations_pkey PRIMARY KEY (id);


--
-- Name: calendar_integrations calendar_integrations_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.calendar_integrations
    ADD CONSTRAINT calendar_integrations_user_id_key UNIQUE (user_id);


--
-- Name: candidate_achievements candidate_achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_achievements
    ADD CONSTRAINT candidate_achievements_pkey PRIMARY KEY (id);


--
-- Name: candidate_activities candidate_activities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_activities
    ADD CONSTRAINT candidate_activities_pkey PRIMARY KEY (id);


--
-- Name: candidate_addresses candidate_addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_addresses
    ADD CONSTRAINT candidate_addresses_pkey PRIMARY KEY (id);


--
-- Name: candidate_ai_profiles candidate_ai_profiles_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_ai_profiles
    ADD CONSTRAINT candidate_ai_profiles_candidate_id_key UNIQUE (candidate_id);


--
-- Name: candidate_ai_profiles candidate_ai_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_ai_profiles
    ADD CONSTRAINT candidate_ai_profiles_pkey PRIMARY KEY (id);


--
-- Name: candidate_ai_recommendations candidate_ai_recommendations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_ai_recommendations
    ADD CONSTRAINT candidate_ai_recommendations_pkey PRIMARY KEY (id);


--
-- Name: candidate_ai_summaries candidate_ai_summaries_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_ai_summaries
    ADD CONSTRAINT candidate_ai_summaries_candidate_id_key UNIQUE (candidate_id);


--
-- Name: candidate_ai_summaries candidate_ai_summaries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_ai_summaries
    ADD CONSTRAINT candidate_ai_summaries_pkey PRIMARY KEY (id);


--
-- Name: candidate_applications candidate_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_applications
    ADD CONSTRAINT candidate_applications_pkey PRIMARY KEY (id);


--
-- Name: candidate_audit_logs candidate_audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_audit_logs
    ADD CONSTRAINT candidate_audit_logs_pkey PRIMARY KEY (id);


--
-- Name: candidate_availability candidate_availability_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_availability
    ADD CONSTRAINT candidate_availability_candidate_id_key UNIQUE (candidate_id);


--
-- Name: candidate_availability candidate_availability_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_availability
    ADD CONSTRAINT candidate_availability_pkey PRIMARY KEY (id);


--
-- Name: candidate_blacklist candidate_blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_blacklist
    ADD CONSTRAINT candidate_blacklist_pkey PRIMARY KEY (id);


--
-- Name: candidate_certifications candidate_certifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_certifications
    ADD CONSTRAINT candidate_certifications_pkey PRIMARY KEY (id);


--
-- Name: candidate_consents candidate_consents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_consents
    ADD CONSTRAINT candidate_consents_pkey PRIMARY KEY (id);


--
-- Name: candidate_document_types candidate_document_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_document_types
    ADD CONSTRAINT candidate_document_types_pkey PRIMARY KEY (id);


--
-- Name: candidate_document_types candidate_document_types_type_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_document_types
    ADD CONSTRAINT candidate_document_types_type_name_key UNIQUE (type_name);


--
-- Name: candidate_documents candidate_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_documents
    ADD CONSTRAINT candidate_documents_pkey PRIMARY KEY (id);


--
-- Name: candidate_education candidate_education_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_education
    ADD CONSTRAINT candidate_education_pkey PRIMARY KEY (id);


--
-- Name: candidate_embeddings candidate_embeddings_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_embeddings
    ADD CONSTRAINT candidate_embeddings_candidate_id_key UNIQUE (candidate_id);


--
-- Name: candidate_embeddings candidate_embeddings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_embeddings
    ADD CONSTRAINT candidate_embeddings_pkey PRIMARY KEY (id);


--
-- Name: candidate_emergency_contacts candidate_emergency_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_emergency_contacts
    ADD CONSTRAINT candidate_emergency_contacts_pkey PRIMARY KEY (id);


--
-- Name: candidate_experience candidate_experience_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_experience
    ADD CONSTRAINT candidate_experience_pkey PRIMARY KEY (id);


--
-- Name: candidate_languages candidate_languages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_languages
    ADD CONSTRAINT candidate_languages_pkey PRIMARY KEY (id);


--
-- Name: candidate_merge_history candidate_merge_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_merge_history
    ADD CONSTRAINT candidate_merge_history_pkey PRIMARY KEY (id);


--
-- Name: candidate_notes candidate_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_notes
    ADD CONSTRAINT candidate_notes_pkey PRIMARY KEY (id);


--
-- Name: candidate_ownership candidate_ownership_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_ownership
    ADD CONSTRAINT candidate_ownership_pkey PRIMARY KEY (id);


--
-- Name: candidate_patents candidate_patents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_patents
    ADD CONSTRAINT candidate_patents_pkey PRIMARY KEY (id);


--
-- Name: candidate_portfolios candidate_portfolios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_portfolios
    ADD CONSTRAINT candidate_portfolios_pkey PRIMARY KEY (id);


--
-- Name: candidate_preferences candidate_preferences_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_preferences
    ADD CONSTRAINT candidate_preferences_candidate_id_key UNIQUE (candidate_id);


--
-- Name: candidate_preferences candidate_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_preferences
    ADD CONSTRAINT candidate_preferences_pkey PRIMARY KEY (id);


--
-- Name: candidate_profiles candidate_profiles_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_profiles
    ADD CONSTRAINT candidate_profiles_candidate_id_key UNIQUE (candidate_id);


--
-- Name: candidate_profiles candidate_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_profiles
    ADD CONSTRAINT candidate_profiles_pkey PRIMARY KEY (id);


--
-- Name: candidate_projects candidate_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_projects
    ADD CONSTRAINT candidate_projects_pkey PRIMARY KEY (id);


--
-- Name: candidate_publications candidate_publications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_publications
    ADD CONSTRAINT candidate_publications_pkey PRIMARY KEY (id);


--
-- Name: candidate_references candidate_references_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_references
    ADD CONSTRAINT candidate_references_pkey PRIMARY KEY (id);


--
-- Name: candidate_resumes candidate_resumes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_resumes
    ADD CONSTRAINT candidate_resumes_pkey PRIMARY KEY (id);


--
-- Name: candidate_salary_expectations candidate_salary_expectations_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_salary_expectations
    ADD CONSTRAINT candidate_salary_expectations_candidate_id_key UNIQUE (candidate_id);


--
-- Name: candidate_salary_expectations candidate_salary_expectations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_salary_expectations
    ADD CONSTRAINT candidate_salary_expectations_pkey PRIMARY KEY (id);


--
-- Name: candidate_skills candidate_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_skills
    ADD CONSTRAINT candidate_skills_pkey PRIMARY KEY (id);


--
-- Name: candidate_social_profiles candidate_social_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_social_profiles
    ADD CONSTRAINT candidate_social_profiles_pkey PRIMARY KEY (id);


--
-- Name: candidate_source_history candidate_source_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_source_history
    ADD CONSTRAINT candidate_source_history_pkey PRIMARY KEY (id);


--
-- Name: candidate_sources candidate_sources_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_sources
    ADD CONSTRAINT candidate_sources_pkey PRIMARY KEY (id);


--
-- Name: candidate_sources candidate_sources_source_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_sources
    ADD CONSTRAINT candidate_sources_source_name_key UNIQUE (source_name);


--
-- Name: candidate_tags candidate_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_tags
    ADD CONSTRAINT candidate_tags_pkey PRIMARY KEY (id);


--
-- Name: candidate_timeline candidate_timeline_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_timeline
    ADD CONSTRAINT candidate_timeline_pkey PRIMARY KEY (id);


--
-- Name: candidates candidates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT candidates_pkey PRIMARY KEY (id);


--
-- Name: certifications certifications_certification_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certifications
    ADD CONSTRAINT certifications_certification_name_key UNIQUE (certification_name);


--
-- Name: certifications certifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.certifications
    ADD CONSTRAINT certifications_pkey PRIMARY KEY (id);


--
-- Name: cities cities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_pkey PRIMARY KEY (id);


--
-- Name: coding_tests coding_tests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coding_tests
    ADD CONSTRAINT coding_tests_pkey PRIMARY KEY (id);


--
-- Name: communication_audit_logs communication_audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communication_audit_logs
    ADD CONSTRAINT communication_audit_logs_pkey PRIMARY KEY (id);


--
-- Name: communication_preferences communication_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communication_preferences
    ADD CONSTRAINT communication_preferences_pkey PRIMARY KEY (id);


--
-- Name: compensation_revisions compensation_revisions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compensation_revisions
    ADD CONSTRAINT compensation_revisions_pkey PRIMARY KEY (id);


--
-- Name: conversation_messages conversation_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conversation_messages
    ADD CONSTRAINT conversation_messages_pkey PRIMARY KEY (id);


--
-- Name: conversation_threads conversation_threads_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conversation_threads
    ADD CONSTRAINT conversation_threads_pkey PRIMARY KEY (id);


--
-- Name: countries countries_iso_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_iso_code_key UNIQUE (iso_code);


--
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (id);


--
-- Name: currencies currencies_currency_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_currency_code_key UNIQUE (currency_code);


--
-- Name: currencies currencies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_pkey PRIMARY KEY (id);


--
-- Name: dashboard_layouts dashboard_layouts_dashboard_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dashboard_layouts
    ADD CONSTRAINT dashboard_layouts_dashboard_id_key UNIQUE (dashboard_id);


--
-- Name: dashboard_layouts dashboard_layouts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dashboard_layouts
    ADD CONSTRAINT dashboard_layouts_pkey PRIMARY KEY (id);


--
-- Name: dashboard_widgets dashboard_widgets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dashboard_widgets
    ADD CONSTRAINT dashboard_widgets_pkey PRIMARY KEY (id);


--
-- Name: dashboards dashboards_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dashboards
    ADD CONSTRAINT dashboards_pkey PRIMARY KEY (id);


--
-- Name: degrees degrees_degree_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.degrees
    ADD CONSTRAINT degrees_degree_name_key UNIQUE (degree_name);


--
-- Name: degrees degrees_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.degrees
    ADD CONSTRAINT degrees_pkey PRIMARY KEY (id);


--
-- Name: delivery_metrics delivery_metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.delivery_metrics
    ADD CONSTRAINT delivery_metrics_pkey PRIMARY KEY (id);


--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (id);


--
-- Name: designations designations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.designations
    ADD CONSTRAINT designations_pkey PRIMARY KEY (id);


--
-- Name: document_chunks document_chunks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_chunks
    ADD CONSTRAINT document_chunks_pkey PRIMARY KEY (id);


--
-- Name: document_embeddings document_embeddings_chunk_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_embeddings
    ADD CONSTRAINT document_embeddings_chunk_id_key UNIQUE (chunk_id);


--
-- Name: document_embeddings document_embeddings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_embeddings
    ADD CONSTRAINT document_embeddings_pkey PRIMARY KEY (id);


--
-- Name: document_verifications document_verifications_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_verifications
    ADD CONSTRAINT document_verifications_candidate_id_key UNIQUE (candidate_id);


--
-- Name: document_verifications document_verifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_verifications
    ADD CONSTRAINT document_verifications_pkey PRIMARY KEY (id);


--
-- Name: duplicate_candidates duplicate_candidates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.duplicate_candidates
    ADD CONSTRAINT duplicate_candidates_pkey PRIMARY KEY (id);


--
-- Name: email_attachments email_attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_attachments
    ADD CONSTRAINT email_attachments_pkey PRIMARY KEY (id);


--
-- Name: email_delivery_logs email_delivery_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_delivery_logs
    ADD CONSTRAINT email_delivery_logs_pkey PRIMARY KEY (id);


--
-- Name: email_queue email_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_queue
    ADD CONSTRAINT email_queue_pkey PRIMARY KEY (id);


--
-- Name: email_templates email_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_templates
    ADD CONSTRAINT email_templates_pkey PRIMARY KEY (id);


--
-- Name: email_verifications email_verifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_verifications
    ADD CONSTRAINT email_verifications_pkey PRIMARY KEY (id);


--
-- Name: email_verifications email_verifications_verification_token_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_verifications
    ADD CONSTRAINT email_verifications_verification_token_key UNIQUE (verification_token);


--
-- Name: employee_conversion_logs employee_conversion_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_conversion_logs
    ADD CONSTRAINT employee_conversion_logs_pkey PRIMARY KEY (id);


--
-- Name: employee_conversions employee_conversions_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_conversions
    ADD CONSTRAINT employee_conversions_candidate_id_key UNIQUE (candidate_id);


--
-- Name: employee_conversions employee_conversions_employee_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_conversions
    ADD CONSTRAINT employee_conversions_employee_id_key UNIQUE (employee_id);


--
-- Name: employee_conversions employee_conversions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_conversions
    ADD CONSTRAINT employee_conversions_pkey PRIMARY KEY (id);


--
-- Name: employment_types employment_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employment_types
    ADD CONSTRAINT employment_types_pkey PRIMARY KEY (id);


--
-- Name: employment_types employment_types_type_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employment_types
    ADD CONSTRAINT employment_types_type_name_key UNIQUE (type_name);


--
-- Name: environment_variables environment_variables_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_variables
    ADD CONSTRAINT environment_variables_pkey PRIMARY KEY (id);


--
-- Name: environment_variables environment_variables_variable_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environment_variables
    ADD CONSTRAINT environment_variables_variable_key_key UNIQUE (variable_key);


--
-- Name: evaluation_criteria evaluation_criteria_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_criteria
    ADD CONSTRAINT evaluation_criteria_pkey PRIMARY KEY (id);


--
-- Name: evaluation_datasets evaluation_datasets_dataset_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_datasets
    ADD CONSTRAINT evaluation_datasets_dataset_name_key UNIQUE (dataset_name);


--
-- Name: evaluation_datasets evaluation_datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_datasets
    ADD CONSTRAINT evaluation_datasets_pkey PRIMARY KEY (id);


--
-- Name: evaluation_scores evaluation_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_scores
    ADD CONSTRAINT evaluation_scores_pkey PRIMARY KEY (id);


--
-- Name: experience_levels experience_levels_level_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.experience_levels
    ADD CONSTRAINT experience_levels_level_name_key UNIQUE (level_name);


--
-- Name: experience_levels experience_levels_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.experience_levels
    ADD CONSTRAINT experience_levels_pkey PRIMARY KEY (id);


--
-- Name: feature_flags feature_flags_flag_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.feature_flags
    ADD CONSTRAINT feature_flags_flag_code_key UNIQUE (flag_code);


--
-- Name: feature_flags feature_flags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.feature_flags
    ADD CONSTRAINT feature_flags_pkey PRIMARY KEY (id);


--
-- Name: file_metadata file_metadata_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.file_metadata
    ADD CONSTRAINT file_metadata_pkey PRIMARY KEY (id);


--
-- Name: file_versions file_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.file_versions
    ADD CONSTRAINT file_versions_pkey PRIMARY KEY (id);


--
-- Name: fine_tuning_datasets fine_tuning_datasets_dataset_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fine_tuning_datasets
    ADD CONSTRAINT fine_tuning_datasets_dataset_name_key UNIQUE (dataset_name);


--
-- Name: fine_tuning_datasets fine_tuning_datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fine_tuning_datasets
    ADD CONSTRAINT fine_tuning_datasets_pkey PRIMARY KEY (id);


--
-- Name: hiring_completions hiring_completions_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_completions
    ADD CONSTRAINT hiring_completions_candidate_id_key UNIQUE (candidate_id);


--
-- Name: hiring_completions hiring_completions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_completions
    ADD CONSTRAINT hiring_completions_pkey PRIMARY KEY (id);


--
-- Name: hiring_plans hiring_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_plans
    ADD CONSTRAINT hiring_plans_pkey PRIMARY KEY (id);


--
-- Name: hiring_request_attachments hiring_request_attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_request_attachments
    ADD CONSTRAINT hiring_request_attachments_pkey PRIMARY KEY (id);


--
-- Name: hiring_request_comments hiring_request_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_request_comments
    ADD CONSTRAINT hiring_request_comments_pkey PRIMARY KEY (id);


--
-- Name: hiring_requests hiring_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_requests
    ADD CONSTRAINT hiring_requests_pkey PRIMARY KEY (id);


--
-- Name: holiday_calendars holiday_calendars_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.holiday_calendars
    ADD CONSTRAINT holiday_calendars_pkey PRIMARY KEY (id);


--
-- Name: holidays holidays_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.holidays
    ADD CONSTRAINT holidays_pkey PRIMARY KEY (id);


--
-- Name: human_reviews human_reviews_execution_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.human_reviews
    ADD CONSTRAINT human_reviews_execution_id_key UNIQUE (execution_id);


--
-- Name: human_reviews human_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.human_reviews
    ADD CONSTRAINT human_reviews_pkey PRIMARY KEY (id);


--
-- Name: industries industries_industry_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.industries
    ADD CONSTRAINT industries_industry_code_key UNIQUE (industry_code);


--
-- Name: industries industries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.industries
    ADD CONSTRAINT industries_pkey PRIMARY KEY (id);


--
-- Name: integration_configurations integration_configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.integration_configurations
    ADD CONSTRAINT integration_configurations_pkey PRIMARY KEY (id);


--
-- Name: integration_registries integration_registries_integration_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.integration_registries
    ADD CONSTRAINT integration_registries_integration_name_key UNIQUE (integration_name);


--
-- Name: integration_registries integration_registries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.integration_registries
    ADD CONSTRAINT integration_registries_pkey PRIMARY KEY (id);


--
-- Name: internal_comments internal_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.internal_comments
    ADD CONSTRAINT internal_comments_pkey PRIMARY KEY (id);


--
-- Name: interview_analytics interview_analytics_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_analytics
    ADD CONSTRAINT interview_analytics_pkey PRIMARY KEY (id);


--
-- Name: interview_attachments interview_attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_attachments
    ADD CONSTRAINT interview_attachments_pkey PRIMARY KEY (id);


--
-- Name: interview_audit_logs interview_audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_audit_logs
    ADD CONSTRAINT interview_audit_logs_pkey PRIMARY KEY (id);


--
-- Name: interview_calendar_events interview_calendar_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_calendar_events
    ADD CONSTRAINT interview_calendar_events_pkey PRIMARY KEY (id);


--
-- Name: interview_cancellations interview_cancellations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_cancellations
    ADD CONSTRAINT interview_cancellations_pkey PRIMARY KEY (id);


--
-- Name: interview_decisions interview_decisions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_decisions
    ADD CONSTRAINT interview_decisions_pkey PRIMARY KEY (id);


--
-- Name: interview_feedback interview_feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_feedback
    ADD CONSTRAINT interview_feedback_pkey PRIMARY KEY (id);


--
-- Name: interview_notifications interview_notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_notifications
    ADD CONSTRAINT interview_notifications_pkey PRIMARY KEY (id);


--
-- Name: interview_panel_members interview_panel_members_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_panel_members
    ADD CONSTRAINT interview_panel_members_pkey PRIMARY KEY (id);


--
-- Name: interview_panels interview_panels_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_panels
    ADD CONSTRAINT interview_panels_pkey PRIMARY KEY (id);


--
-- Name: interview_participants interview_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_participants
    ADD CONSTRAINT interview_participants_pkey PRIMARY KEY (id);


--
-- Name: interview_plans interview_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_plans
    ADD CONSTRAINT interview_plans_pkey PRIMARY KEY (id);


--
-- Name: interview_recordings interview_recordings_interview_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_recordings
    ADD CONSTRAINT interview_recordings_interview_id_key UNIQUE (interview_id);


--
-- Name: interview_recordings interview_recordings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_recordings
    ADD CONSTRAINT interview_recordings_pkey PRIMARY KEY (id);


--
-- Name: interview_reschedules interview_reschedules_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_reschedules
    ADD CONSTRAINT interview_reschedules_pkey PRIMARY KEY (id);


--
-- Name: interview_rounds interview_rounds_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_rounds
    ADD CONSTRAINT interview_rounds_pkey PRIMARY KEY (id);


--
-- Name: interview_schedules interview_schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_schedules
    ADD CONSTRAINT interview_schedules_pkey PRIMARY KEY (id);


--
-- Name: interview_scorecards interview_scorecards_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_scorecards
    ADD CONSTRAINT interview_scorecards_pkey PRIMARY KEY (id);


--
-- Name: interview_stage_templates interview_stage_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_stage_templates
    ADD CONSTRAINT interview_stage_templates_pkey PRIMARY KEY (id);


--
-- Name: interview_timelines interview_timelines_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_timelines
    ADD CONSTRAINT interview_timelines_pkey PRIMARY KEY (id);


--
-- Name: interview_types interview_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_types
    ADD CONSTRAINT interview_types_pkey PRIMARY KEY (id);


--
-- Name: interview_types interview_types_type_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_types
    ADD CONSTRAINT interview_types_type_name_key UNIQUE (type_name);


--
-- Name: interviewer_assignments interviewer_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interviewer_assignments
    ADD CONSTRAINT interviewer_assignments_pkey PRIMARY KEY (id);


--
-- Name: interviews interviews_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interviews
    ADD CONSTRAINT interviews_pkey PRIMARY KEY (id);


--
-- Name: job_benefits job_benefits_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_benefits
    ADD CONSTRAINT job_benefits_pkey PRIMARY KEY (id);


--
-- Name: job_families job_families_family_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_families
    ADD CONSTRAINT job_families_family_code_key UNIQUE (family_code);


--
-- Name: job_families job_families_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_families
    ADD CONSTRAINT job_families_pkey PRIMARY KEY (id);


--
-- Name: job_hiring_managers job_hiring_managers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_hiring_managers
    ADD CONSTRAINT job_hiring_managers_pkey PRIMARY KEY (id);


--
-- Name: job_locations job_locations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_locations
    ADD CONSTRAINT job_locations_pkey PRIMARY KEY (id);


--
-- Name: job_publications job_publications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_publications
    ADD CONSTRAINT job_publications_pkey PRIMARY KEY (id);


--
-- Name: job_qualifications job_qualifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_qualifications
    ADD CONSTRAINT job_qualifications_pkey PRIMARY KEY (id);


--
-- Name: job_queues job_queues_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_queues
    ADD CONSTRAINT job_queues_pkey PRIMARY KEY (id);


--
-- Name: job_queues job_queues_queue_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_queues
    ADD CONSTRAINT job_queues_queue_name_key UNIQUE (queue_name);


--
-- Name: job_recruiters job_recruiters_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_recruiters
    ADD CONSTRAINT job_recruiters_pkey PRIMARY KEY (id);


--
-- Name: job_responsibilities job_responsibilities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_responsibilities
    ADD CONSTRAINT job_responsibilities_pkey PRIMARY KEY (id);


--
-- Name: job_salary_ranges job_salary_ranges_job_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_salary_ranges
    ADD CONSTRAINT job_salary_ranges_job_id_key UNIQUE (job_id);


--
-- Name: job_salary_ranges job_salary_ranges_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_salary_ranges
    ADD CONSTRAINT job_salary_ranges_pkey PRIMARY KEY (id);


--
-- Name: job_skills job_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_pkey PRIMARY KEY (id);


--
-- Name: job_templates job_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_templates
    ADD CONSTRAINT job_templates_pkey PRIMARY KEY (id);


--
-- Name: job_versions job_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_versions
    ADD CONSTRAINT job_versions_pkey PRIMARY KEY (id);


--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);


--
-- Name: joining_audits joining_audits_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.joining_audits
    ADD CONSTRAINT joining_audits_candidate_id_key UNIQUE (candidate_id);


--
-- Name: joining_audits joining_audits_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.joining_audits
    ADD CONSTRAINT joining_audits_pkey PRIMARY KEY (id);


--
-- Name: joining_confirmations joining_confirmations_offer_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.joining_confirmations
    ADD CONSTRAINT joining_confirmations_offer_id_key UNIQUE (offer_id);


--
-- Name: joining_confirmations joining_confirmations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.joining_confirmations
    ADD CONSTRAINT joining_confirmations_pkey PRIMARY KEY (id);


--
-- Name: knowledge_bases knowledge_bases_kb_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.knowledge_bases
    ADD CONSTRAINT knowledge_bases_kb_name_key UNIQUE (kb_name);


--
-- Name: knowledge_bases knowledge_bases_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.knowledge_bases
    ADD CONSTRAINT knowledge_bases_pkey PRIMARY KEY (id);


--
-- Name: knowledge_collections knowledge_collections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.knowledge_collections
    ADD CONSTRAINT knowledge_collections_pkey PRIMARY KEY (id);


--
-- Name: knowledge_documents knowledge_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.knowledge_documents
    ADD CONSTRAINT knowledge_documents_pkey PRIMARY KEY (id);


--
-- Name: languages languages_language_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_language_code_key UNIQUE (language_code);


--
-- Name: languages languages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_pkey PRIMARY KEY (id);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- Name: login_history login_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.login_history
    ADD CONSTRAINT login_history_pkey PRIMARY KEY (id);


--
-- Name: medical_verifications medical_verifications_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medical_verifications
    ADD CONSTRAINT medical_verifications_candidate_id_key UNIQUE (candidate_id);


--
-- Name: medical_verifications medical_verifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medical_verifications
    ADD CONSTRAINT medical_verifications_pkey PRIMARY KEY (id);


--
-- Name: meeting_invitations meeting_invitations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_invitations
    ADD CONSTRAINT meeting_invitations_pkey PRIMARY KEY (id);


--
-- Name: mentions mentions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentions
    ADD CONSTRAINT mentions_pkey PRIMARY KEY (id);


--
-- Name: message_attachments message_attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.message_attachments
    ADD CONSTRAINT message_attachments_pkey PRIMARY KEY (id);


--
-- Name: messaging_templates messaging_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messaging_templates
    ADD CONSTRAINT messaging_templates_pkey PRIMARY KEY (id);


--
-- Name: mfa_configurations mfa_configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_configurations
    ADD CONSTRAINT mfa_configurations_pkey PRIMARY KEY (id);


--
-- Name: mfa_configurations mfa_configurations_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_configurations
    ADD CONSTRAINT mfa_configurations_user_id_key UNIQUE (user_id);


--
-- Name: mfa_recovery_codes mfa_recovery_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_recovery_codes
    ADD CONSTRAINT mfa_recovery_codes_pkey PRIMARY KEY (id);


--
-- Name: notification_delivery_logs notification_delivery_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_delivery_logs
    ADD CONSTRAINT notification_delivery_logs_pkey PRIMARY KEY (id);


--
-- Name: notification_events notification_events_event_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_events
    ADD CONSTRAINT notification_events_event_code_key UNIQUE (event_code);


--
-- Name: notification_events notification_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_events
    ADD CONSTRAINT notification_events_pkey PRIMARY KEY (id);


--
-- Name: notification_queue notification_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_queue
    ADD CONSTRAINT notification_queue_pkey PRIMARY KEY (id);


--
-- Name: notification_templates notification_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_templates
    ADD CONSTRAINT notification_templates_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: object_storage object_storage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.object_storage
    ADD CONSTRAINT object_storage_pkey PRIMARY KEY (id);


--
-- Name: offer_acceptance offer_acceptance_offer_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_acceptance
    ADD CONSTRAINT offer_acceptance_offer_id_key UNIQUE (offer_id);


--
-- Name: offer_acceptance offer_acceptance_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_acceptance
    ADD CONSTRAINT offer_acceptance_pkey PRIMARY KEY (id);


--
-- Name: offer_approval_history offer_approval_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_approval_history
    ADD CONSTRAINT offer_approval_history_pkey PRIMARY KEY (id);


--
-- Name: offer_approvals offer_approvals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_approvals
    ADD CONSTRAINT offer_approvals_pkey PRIMARY KEY (id);


--
-- Name: offer_attachments offer_attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_attachments
    ADD CONSTRAINT offer_attachments_pkey PRIMARY KEY (id);


--
-- Name: offer_audits offer_audits_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_audits
    ADD CONSTRAINT offer_audits_pkey PRIMARY KEY (id);


--
-- Name: offer_compensation offer_compensation_offer_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_compensation
    ADD CONSTRAINT offer_compensation_offer_id_key UNIQUE (offer_id);


--
-- Name: offer_compensation offer_compensation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_compensation
    ADD CONSTRAINT offer_compensation_pkey PRIMARY KEY (id);


--
-- Name: offer_documents offer_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_documents
    ADD CONSTRAINT offer_documents_pkey PRIMARY KEY (id);


--
-- Name: offer_negotiations offer_negotiations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_negotiations
    ADD CONSTRAINT offer_negotiations_pkey PRIMARY KEY (id);


--
-- Name: offer_rejections offer_rejections_offer_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_rejections
    ADD CONSTRAINT offer_rejections_offer_id_key UNIQUE (offer_id);


--
-- Name: offer_rejections offer_rejections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_rejections
    ADD CONSTRAINT offer_rejections_pkey PRIMARY KEY (id);


--
-- Name: offer_templates offer_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_templates
    ADD CONSTRAINT offer_templates_pkey PRIMARY KEY (id);


--
-- Name: offer_versions offer_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_versions
    ADD CONSTRAINT offer_versions_pkey PRIMARY KEY (id);


--
-- Name: offers offers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offers
    ADD CONSTRAINT offers_pkey PRIMARY KEY (id);


--
-- Name: onboarding_checklists onboarding_checklists_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_checklists
    ADD CONSTRAINT onboarding_checklists_candidate_id_key UNIQUE (candidate_id);


--
-- Name: onboarding_checklists onboarding_checklists_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_checklists
    ADD CONSTRAINT onboarding_checklists_pkey PRIMARY KEY (id);


--
-- Name: onboarding_document_reviews onboarding_document_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_document_reviews
    ADD CONSTRAINT onboarding_document_reviews_pkey PRIMARY KEY (id);


--
-- Name: onboarding_document_submissions onboarding_document_submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_document_submissions
    ADD CONSTRAINT onboarding_document_submissions_pkey PRIMARY KEY (id);


--
-- Name: onboarding_documents onboarding_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_documents
    ADD CONSTRAINT onboarding_documents_pkey PRIMARY KEY (id);


--
-- Name: onboarding_plans onboarding_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_plans
    ADD CONSTRAINT onboarding_plans_pkey PRIMARY KEY (id);


--
-- Name: onboarding_task_assignments onboarding_task_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_task_assignments
    ADD CONSTRAINT onboarding_task_assignments_pkey PRIMARY KEY (id);


--
-- Name: onboarding_tasks onboarding_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_tasks
    ADD CONSTRAINT onboarding_tasks_pkey PRIMARY KEY (id);


--
-- Name: organization_settings organization_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organization_settings
    ADD CONSTRAINT organization_settings_pkey PRIMARY KEY (id);


--
-- Name: organizations organizations_organization_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_organization_code_key UNIQUE (organization_code);


--
-- Name: organizations organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (id);


--
-- Name: password_history password_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_history
    ADD CONSTRAINT password_history_pkey PRIMARY KEY (id);


--
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (id);


--
-- Name: password_reset_tokens password_reset_tokens_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_token_hash_key UNIQUE (token_hash);


--
-- Name: permission_groups permission_groups_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permission_groups
    ADD CONSTRAINT permission_groups_group_name_key UNIQUE (group_name);


--
-- Name: permission_groups permission_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permission_groups
    ADD CONSTRAINT permission_groups_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_permission_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_permission_code_key UNIQUE (permission_code);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: pipeline_stage_mapping pipeline_stage_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pipeline_stage_mapping
    ADD CONSTRAINT pipeline_stage_mapping_pkey PRIMARY KEY (id);


--
-- Name: probation_setups probation_setups_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.probation_setups
    ADD CONSTRAINT probation_setups_candidate_id_key UNIQUE (candidate_id);


--
-- Name: probation_setups probation_setups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.probation_setups
    ADD CONSTRAINT probation_setups_pkey PRIMARY KEY (id);


--
-- Name: prompt_evaluations prompt_evaluations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prompt_evaluations
    ADD CONSTRAINT prompt_evaluations_pkey PRIMARY KEY (id);


--
-- Name: prompt_templates prompt_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prompt_templates
    ADD CONSTRAINT prompt_templates_pkey PRIMARY KEY (id);


--
-- Name: prompt_templates prompt_templates_template_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prompt_templates
    ADD CONSTRAINT prompt_templates_template_name_key UNIQUE (template_name);


--
-- Name: prompt_variables prompt_variables_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prompt_variables
    ADD CONSTRAINT prompt_variables_pkey PRIMARY KEY (id);


--
-- Name: prompt_versions prompt_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prompt_versions
    ADD CONSTRAINT prompt_versions_pkey PRIMARY KEY (id);


--
-- Name: publication_channels publication_channels_channel_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publication_channels
    ADD CONSTRAINT publication_channels_channel_name_key UNIQUE (channel_name);


--
-- Name: publication_channels publication_channels_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publication_channels
    ADD CONSTRAINT publication_channels_pkey PRIMARY KEY (id);


--
-- Name: publication_history publication_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publication_history
    ADD CONSTRAINT publication_history_pkey PRIMARY KEY (id);


--
-- Name: push_delivery_logs push_delivery_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.push_delivery_logs
    ADD CONSTRAINT push_delivery_logs_pkey PRIMARY KEY (id);


--
-- Name: push_notifications push_notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.push_notifications
    ADD CONSTRAINT push_notifications_pkey PRIMARY KEY (id);


--
-- Name: rag_citations rag_citations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rag_citations
    ADD CONSTRAINT rag_citations_pkey PRIMARY KEY (id);


--
-- Name: rag_retrieval_results rag_retrieval_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rag_retrieval_results
    ADD CONSTRAINT rag_retrieval_results_pkey PRIMARY KEY (id);


--
-- Name: rag_sessions rag_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rag_sessions
    ADD CONSTRAINT rag_sessions_pkey PRIMARY KEY (id);


--
-- Name: recruiter_workloads recruiter_workloads_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruiter_workloads
    ADD CONSTRAINT recruiter_workloads_pkey PRIMARY KEY (id);


--
-- Name: recruiter_workloads recruiter_workloads_recruiter_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruiter_workloads
    ADD CONSTRAINT recruiter_workloads_recruiter_id_key UNIQUE (recruiter_id);


--
-- Name: recruitment_audit_logs recruitment_audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_audit_logs
    ADD CONSTRAINT recruitment_audit_logs_pkey PRIMARY KEY (id);


--
-- Name: recruitment_closures recruitment_closures_job_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_closures
    ADD CONSTRAINT recruitment_closures_job_id_key UNIQUE (job_id);


--
-- Name: recruitment_closures recruitment_closures_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_closures
    ADD CONSTRAINT recruitment_closures_pkey PRIMARY KEY (id);


--
-- Name: recruitment_metrics recruitment_metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_metrics
    ADD CONSTRAINT recruitment_metrics_pkey PRIMARY KEY (id);


--
-- Name: recruitment_pipelines recruitment_pipelines_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_pipelines
    ADD CONSTRAINT recruitment_pipelines_pkey PRIMARY KEY (id);


--
-- Name: recruitment_stages recruitment_stages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_stages
    ADD CONSTRAINT recruitment_stages_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_token_hash_key UNIQUE (token_hash);


--
-- Name: report_definitions report_definitions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.report_definitions
    ADD CONSTRAINT report_definitions_pkey PRIMARY KEY (id);


--
-- Name: report_execution_logs report_execution_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.report_execution_logs
    ADD CONSTRAINT report_execution_logs_pkey PRIMARY KEY (id);


--
-- Name: report_parameters report_parameters_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.report_parameters
    ADD CONSTRAINT report_parameters_pkey PRIMARY KEY (id);


--
-- Name: requisition_approvals requisition_approvals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requisition_approvals
    ADD CONSTRAINT requisition_approvals_pkey PRIMARY KEY (id);


--
-- Name: resume_parsing_history resume_parsing_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resume_parsing_history
    ADD CONSTRAINT resume_parsing_history_pkey PRIMARY KEY (id);


--
-- Name: resume_versions resume_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resume_versions
    ADD CONSTRAINT resume_versions_pkey PRIMARY KEY (id);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: salary_bands salary_bands_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salary_bands
    ADD CONSTRAINT salary_bands_pkey PRIMARY KEY (id);


--
-- Name: scheduled_jobs scheduled_jobs_job_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scheduled_jobs
    ADD CONSTRAINT scheduled_jobs_job_name_key UNIQUE (job_name);


--
-- Name: scheduled_jobs scheduled_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scheduled_jobs
    ADD CONSTRAINT scheduled_jobs_pkey PRIMARY KEY (id);


--
-- Name: scheduled_reports scheduled_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scheduled_reports
    ADD CONSTRAINT scheduled_reports_pkey PRIMARY KEY (id);


--
-- Name: scheduler_history scheduler_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scheduler_history
    ADD CONSTRAINT scheduler_history_pkey PRIMARY KEY (id);


--
-- Name: security_events security_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_events
    ADD CONSTRAINT security_events_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_session_token_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_session_token_key UNIQUE (session_token);


--
-- Name: shifts shifts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shifts
    ADD CONSTRAINT shifts_pkey PRIMARY KEY (id);


--
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (id);


--
-- Name: skills skills_skill_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_skill_name_key UNIQUE (skill_name);


--
-- Name: sms_queue sms_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_queue
    ADD CONSTRAINT sms_queue_pkey PRIMARY KEY (id);


--
-- Name: stage_sla stage_sla_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stage_sla
    ADD CONSTRAINT stage_sla_pkey PRIMARY KEY (id);


--
-- Name: states states_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.states
    ADD CONSTRAINT states_pkey PRIMARY KEY (id);


--
-- Name: storage_quotas storage_quotas_organization_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.storage_quotas
    ADD CONSTRAINT storage_quotas_organization_id_key UNIQUE (organization_id);


--
-- Name: storage_quotas storage_quotas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.storage_quotas
    ADD CONSTRAINT storage_quotas_pkey PRIMARY KEY (id);


--
-- Name: system_settings system_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.system_settings
    ADD CONSTRAINT system_settings_pkey PRIMARY KEY (id);


--
-- Name: system_settings system_settings_setting_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.system_settings
    ADD CONSTRAINT system_settings_setting_key_key UNIQUE (setting_key);


--
-- Name: tenant_preferences tenant_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tenant_preferences
    ADD CONSTRAINT tenant_preferences_pkey PRIMARY KEY (id);


--
-- Name: timezones timezones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timezones
    ADD CONSTRAINT timezones_pkey PRIMARY KEY (id);


--
-- Name: timezones timezones_timezone_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timezones
    ADD CONSTRAINT timezones_timezone_code_key UNIQUE (timezone_code);


--
-- Name: token_usage token_usage_execution_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token_usage
    ADD CONSTRAINT token_usage_execution_id_key UNIQUE (execution_id);


--
-- Name: token_usage token_usage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token_usage
    ADD CONSTRAINT token_usage_pkey PRIMARY KEY (id);


--
-- Name: universities universities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.universities
    ADD CONSTRAINT universities_pkey PRIMARY KEY (id);


--
-- Name: universities universities_university_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.universities
    ADD CONSTRAINT universities_university_name_key UNIQUE (university_name);


--
-- Name: offers uq_active_offer_per_app; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offers
    ADD CONSTRAINT uq_active_offer_per_app UNIQUE (candidate_application_id);


--
-- Name: assessment_attempts uq_assessment_attempt; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment_attempts
    ADD CONSTRAINT uq_assessment_attempt UNIQUE (assessment_id, candidate_id, attempt_number);


--
-- Name: onboarding_task_assignments uq_candidate_onboarding_task; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_task_assignments
    ADD CONSTRAINT uq_candidate_onboarding_task UNIQUE (candidate_id, onboarding_task_id);


--
-- Name: candidate_social_profiles uq_candidate_social; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_social_profiles
    ADD CONSTRAINT uq_candidate_social UNIQUE (candidate_id, social_platform);


--
-- Name: file_versions uq_file_version_num; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.file_versions
    ADD CONSTRAINT uq_file_version_num UNIQUE (file_id, version_number);


--
-- Name: interview_feedback uq_interview_feedback; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_feedback
    ADD CONSTRAINT uq_interview_feedback UNIQUE (interview_id, interviewer_id);


--
-- Name: interview_panel_members uq_interview_panel_member; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_panel_members
    ADD CONSTRAINT uq_interview_panel_member UNIQUE (panel_id, panel_member_id);


--
-- Name: job_hiring_managers uq_job_hiring_manager; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_hiring_managers
    ADD CONSTRAINT uq_job_hiring_manager UNIQUE (job_id, hiring_manager_id);


--
-- Name: job_recruiters uq_job_recruiter; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_recruiters
    ADD CONSTRAINT uq_job_recruiter UNIQUE (job_id, recruiter_id);


--
-- Name: ai_model_versions uq_model_version_code; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_model_versions
    ADD CONSTRAINT uq_model_version_code UNIQUE (model_id, version_code);


--
-- Name: offer_versions uq_offer_version; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_versions
    ADD CONSTRAINT uq_offer_version UNIQUE (offer_id, version_number);


--
-- Name: integration_configurations uq_org_integration_config; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.integration_configurations
    ADD CONSTRAINT uq_org_integration_config UNIQUE (organization_id, integration_id);


--
-- Name: notification_templates uq_org_notification_template; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_templates
    ADD CONSTRAINT uq_org_notification_template UNIQUE (organization_id, template_code);


--
-- Name: hiring_requests uq_org_requisition; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_requests
    ADD CONSTRAINT uq_org_requisition UNIQUE (organization_id, requisition_number);


--
-- Name: organization_settings uq_org_setting_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organization_settings
    ADD CONSTRAINT uq_org_setting_key UNIQUE (organization_id, setting_key);


--
-- Name: prompt_versions uq_prompt_template_version; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prompt_versions
    ADD CONSTRAINT uq_prompt_template_version UNIQUE (template_id, version_number);


--
-- Name: role_permissions uq_role_permission; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT uq_role_permission UNIQUE (role_id, permission_id);


--
-- Name: tenant_preferences uq_tenant_pref_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tenant_preferences
    ADD CONSTRAINT uq_tenant_pref_key UNIQUE (organization_id, preference_key);


--
-- Name: conversation_messages uq_thread_message_sequence; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conversation_messages
    ADD CONSTRAINT uq_thread_message_sequence UNIQUE (thread_id, message_sequence);


--
-- Name: user_devices uq_user_device; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_devices
    ADD CONSTRAINT uq_user_device UNIQUE (user_id, device_token);


--
-- Name: user_roles uq_user_role; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT uq_user_role UNIQUE (user_id, role_id);


--
-- Name: user_devices user_devices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_devices
    ADD CONSTRAINT user_devices_pkey PRIMARY KEY (id);


--
-- Name: user_preferences user_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_pkey PRIMARY KEY (id);


--
-- Name: user_preferences user_preferences_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_user_id_key UNIQUE (user_id);


--
-- Name: user_profiles user_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_pkey PRIMARY KEY (id);


--
-- Name: user_profiles user_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_user_id_key UNIQUE (user_id);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: webhook_deliveries webhook_deliveries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.webhook_deliveries
    ADD CONSTRAINT webhook_deliveries_pkey PRIMARY KEY (id);


--
-- Name: webhook_events webhook_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.webhook_events
    ADD CONSTRAINT webhook_events_pkey PRIMARY KEY (id);


--
-- Name: webhook_logs webhook_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.webhook_logs
    ADD CONSTRAINT webhook_logs_pkey PRIMARY KEY (id);


--
-- Name: webhook_registries webhook_registries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.webhook_registries
    ADD CONSTRAINT webhook_registries_pkey PRIMARY KEY (id);


--
-- Name: webhook_subscriptions webhook_subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.webhook_subscriptions
    ADD CONSTRAINT webhook_subscriptions_pkey PRIMARY KEY (id);


--
-- Name: welcome_kits welcome_kits_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.welcome_kits
    ADD CONSTRAINT welcome_kits_pkey PRIMARY KEY (id);


--
-- Name: whatsapp_queue whatsapp_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.whatsapp_queue
    ADD CONSTRAINT whatsapp_queue_pkey PRIMARY KEY (id);


--
-- Name: widget_configurations widget_configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.widget_configurations
    ADD CONSTRAINT widget_configurations_pkey PRIMARY KEY (id);


--
-- Name: widget_configurations widget_configurations_widget_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.widget_configurations
    ADD CONSTRAINT widget_configurations_widget_id_key UNIQUE (widget_id);


--
-- Name: widget_data_queries widget_data_queries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.widget_data_queries
    ADD CONSTRAINT widget_data_queries_pkey PRIMARY KEY (id);


--
-- Name: widget_data_queries widget_data_queries_widget_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.widget_data_queries
    ADD CONSTRAINT widget_data_queries_widget_id_key UNIQUE (widget_id);


--
-- Name: work_modes work_modes_mode_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.work_modes
    ADD CONSTRAINT work_modes_mode_name_key UNIQUE (mode_name);


--
-- Name: work_modes work_modes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.work_modes
    ADD CONSTRAINT work_modes_pkey PRIMARY KEY (id);


--
-- Name: ix_activity_feed_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_feed_id ON public.activity_feed USING btree (id);


--
-- Name: ix_activity_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activity_logs_id ON public.activity_logs USING btree (id);


--
-- Name: ix_ai_agent_capabilities_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_agent_capabilities_id ON public.ai_agent_capabilities USING btree (id);


--
-- Name: ix_ai_agents_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_agents_id ON public.ai_agents USING btree (id);


--
-- Name: ix_ai_audit_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_audit_logs_id ON public.ai_audit_logs USING btree (id);


--
-- Name: ix_ai_behavior_analysis_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_behavior_analysis_id ON public.ai_behavior_analysis USING btree (id);


--
-- Name: ix_ai_candidate_feedback_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_candidate_feedback_id ON public.ai_candidate_feedback USING btree (id);


--
-- Name: ix_ai_candidate_rankings_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_candidate_rankings_id ON public.ai_candidate_rankings USING btree (id);


--
-- Name: ix_ai_conversations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_conversations_id ON public.ai_conversations USING btree (id);


--
-- Name: ix_ai_cost_tracking_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_cost_tracking_id ON public.ai_cost_tracking USING btree (id);


--
-- Name: ix_ai_decision_support_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_decision_support_id ON public.ai_decision_support USING btree (id);


--
-- Name: ix_ai_execution_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_execution_logs_id ON public.ai_execution_logs USING btree (id);


--
-- Name: ix_ai_executions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_executions_id ON public.ai_executions USING btree (id);


--
-- Name: ix_ai_feedback_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_feedback_id ON public.ai_feedback USING btree (id);


--
-- Name: ix_ai_interview_analysis_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_interview_analysis_id ON public.ai_interview_analysis USING btree (id);


--
-- Name: ix_ai_interview_scores_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_interview_scores_id ON public.ai_interview_scores USING btree (id);


--
-- Name: ix_ai_interview_summary_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_interview_summary_id ON public.ai_interview_summary USING btree (id);


--
-- Name: ix_ai_job_recommendations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_job_recommendations_id ON public.ai_job_recommendations USING btree (id);


--
-- Name: ix_ai_memory_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_memory_id ON public.ai_memory USING btree (id);


--
-- Name: ix_ai_messages_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_messages_id ON public.ai_messages USING btree (id);


--
-- Name: ix_ai_metrics_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_metrics_id ON public.ai_metrics USING btree (id);


--
-- Name: ix_ai_model_configurations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_model_configurations_id ON public.ai_model_configurations USING btree (id);


--
-- Name: ix_ai_model_providers_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_model_providers_id ON public.ai_model_providers USING btree (id);


--
-- Name: ix_ai_model_versions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_model_versions_id ON public.ai_model_versions USING btree (id);


--
-- Name: ix_ai_models_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_models_id ON public.ai_models USING btree (id);


--
-- Name: ix_ai_recommendations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_recommendations_id ON public.ai_recommendations USING btree (id);


--
-- Name: ix_ai_recruitment_insights_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_recruitment_insights_id ON public.ai_recruitment_insights USING btree (id);


--
-- Name: ix_ai_requests_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_requests_id ON public.ai_requests USING btree (id);


--
-- Name: ix_ai_responses_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_responses_id ON public.ai_responses USING btree (id);


--
-- Name: ix_ai_screening_results_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_screening_results_id ON public.ai_screening_results USING btree (id);


--
-- Name: ix_ai_summaries_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_summaries_id ON public.ai_summaries USING btree (id);


--
-- Name: ix_ai_tool_executions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_tool_executions_id ON public.ai_tool_executions USING btree (id);


--
-- Name: ix_ai_tool_permissions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_tool_permissions_id ON public.ai_tool_permissions USING btree (id);


--
-- Name: ix_ai_tools_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_tools_id ON public.ai_tools USING btree (id);


--
-- Name: ix_ai_workflow_steps_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_workflow_steps_id ON public.ai_workflow_steps USING btree (id);


--
-- Name: ix_ai_workflows_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ai_workflows_id ON public.ai_workflows USING btree (id);


--
-- Name: ix_announcements_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_announcements_id ON public.announcements USING btree (id);


--
-- Name: ix_api_credentials_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_api_credentials_id ON public.api_credentials USING btree (id);


--
-- Name: ix_api_keys_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_api_keys_id ON public.api_keys USING btree (id);


--
-- Name: ix_application_documents_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_application_documents_id ON public.application_documents USING btree (id);


--
-- Name: ix_application_notes_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_application_notes_id ON public.application_notes USING btree (id);


--
-- Name: ix_application_screening_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_application_screening_id ON public.application_screening USING btree (id);


--
-- Name: ix_application_stage_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_application_stage_history_id ON public.application_stage_history USING btree (id);


--
-- Name: ix_application_tags_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_application_tags_id ON public.application_tags USING btree (id);


--
-- Name: ix_approval_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_approval_history_id ON public.approval_history USING btree (id);


--
-- Name: ix_assessment_answers_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_assessment_answers_id ON public.assessment_answers USING btree (id);


--
-- Name: ix_assessment_attempts_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_assessment_attempts_id ON public.assessment_attempts USING btree (id);


--
-- Name: ix_assessment_questions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_assessment_questions_id ON public.assessment_questions USING btree (id);


--
-- Name: ix_assessment_templates_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_assessment_templates_id ON public.assessment_templates USING btree (id);


--
-- Name: ix_assessments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_assessments_id ON public.assessments USING btree (id);


--
-- Name: ix_assignment_submissions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_assignment_submissions_id ON public.assignment_submissions USING btree (id);


--
-- Name: ix_audit_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_logs_id ON public.audit_logs USING btree (id);


--
-- Name: ix_background_check_items_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_background_check_items_id ON public.background_check_items USING btree (id);


--
-- Name: ix_background_jobs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_background_jobs_id ON public.background_jobs USING btree (id);


--
-- Name: ix_background_verifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_background_verifications_id ON public.background_verifications USING btree (id);


--
-- Name: ix_benchmark_results_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_benchmark_results_id ON public.benchmark_results USING btree (id);


--
-- Name: ix_branches_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_branches_id ON public.branches USING btree (id);


--
-- Name: ix_broadcast_messages_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_broadcast_messages_id ON public.broadcast_messages USING btree (id);


--
-- Name: ix_business_units_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_business_units_id ON public.business_units USING btree (id);


--
-- Name: ix_calendar_events_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_calendar_events_id ON public.calendar_events USING btree (id);


--
-- Name: ix_calendar_integrations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_calendar_integrations_id ON public.calendar_integrations USING btree (id);


--
-- Name: ix_candidate_achievements_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_achievements_id ON public.candidate_achievements USING btree (id);


--
-- Name: ix_candidate_activities_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_activities_id ON public.candidate_activities USING btree (id);


--
-- Name: ix_candidate_addresses_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_addresses_id ON public.candidate_addresses USING btree (id);


--
-- Name: ix_candidate_ai_profiles_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_ai_profiles_id ON public.candidate_ai_profiles USING btree (id);


--
-- Name: ix_candidate_ai_recommendations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_ai_recommendations_id ON public.candidate_ai_recommendations USING btree (id);


--
-- Name: ix_candidate_ai_summaries_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_ai_summaries_id ON public.candidate_ai_summaries USING btree (id);


--
-- Name: ix_candidate_applications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_applications_id ON public.candidate_applications USING btree (id);


--
-- Name: ix_candidate_audit_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_audit_logs_id ON public.candidate_audit_logs USING btree (id);


--
-- Name: ix_candidate_availability_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_availability_id ON public.candidate_availability USING btree (id);


--
-- Name: ix_candidate_blacklist_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_blacklist_id ON public.candidate_blacklist USING btree (id);


--
-- Name: ix_candidate_certifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_certifications_id ON public.candidate_certifications USING btree (id);


--
-- Name: ix_candidate_consents_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_consents_id ON public.candidate_consents USING btree (id);


--
-- Name: ix_candidate_document_types_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_document_types_id ON public.candidate_document_types USING btree (id);


--
-- Name: ix_candidate_documents_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_documents_id ON public.candidate_documents USING btree (id);


--
-- Name: ix_candidate_education_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_education_id ON public.candidate_education USING btree (id);


--
-- Name: ix_candidate_embeddings_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_embeddings_id ON public.candidate_embeddings USING btree (id);


--
-- Name: ix_candidate_emergency_contacts_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_emergency_contacts_id ON public.candidate_emergency_contacts USING btree (id);


--
-- Name: ix_candidate_experience_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_experience_id ON public.candidate_experience USING btree (id);


--
-- Name: ix_candidate_languages_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_languages_id ON public.candidate_languages USING btree (id);


--
-- Name: ix_candidate_merge_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_merge_history_id ON public.candidate_merge_history USING btree (id);


--
-- Name: ix_candidate_notes_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_notes_id ON public.candidate_notes USING btree (id);


--
-- Name: ix_candidate_ownership_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_ownership_id ON public.candidate_ownership USING btree (id);


--
-- Name: ix_candidate_patents_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_patents_id ON public.candidate_patents USING btree (id);


--
-- Name: ix_candidate_portfolios_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_portfolios_id ON public.candidate_portfolios USING btree (id);


--
-- Name: ix_candidate_preferences_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_preferences_id ON public.candidate_preferences USING btree (id);


--
-- Name: ix_candidate_profiles_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_profiles_id ON public.candidate_profiles USING btree (id);


--
-- Name: ix_candidate_projects_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_projects_id ON public.candidate_projects USING btree (id);


--
-- Name: ix_candidate_publications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_publications_id ON public.candidate_publications USING btree (id);


--
-- Name: ix_candidate_references_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_references_id ON public.candidate_references USING btree (id);


--
-- Name: ix_candidate_resumes_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_resumes_id ON public.candidate_resumes USING btree (id);


--
-- Name: ix_candidate_salary_expectations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_salary_expectations_id ON public.candidate_salary_expectations USING btree (id);


--
-- Name: ix_candidate_skills_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_skills_id ON public.candidate_skills USING btree (id);


--
-- Name: ix_candidate_social_profiles_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_social_profiles_id ON public.candidate_social_profiles USING btree (id);


--
-- Name: ix_candidate_source_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_source_history_id ON public.candidate_source_history USING btree (id);


--
-- Name: ix_candidate_sources_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_sources_id ON public.candidate_sources USING btree (id);


--
-- Name: ix_candidate_tags_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_tags_id ON public.candidate_tags USING btree (id);


--
-- Name: ix_candidate_timeline_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidate_timeline_id ON public.candidate_timeline USING btree (id);


--
-- Name: ix_candidates_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_candidates_id ON public.candidates USING btree (id);


--
-- Name: ix_certifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_certifications_id ON public.certifications USING btree (id);


--
-- Name: ix_cities_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_cities_id ON public.cities USING btree (id);


--
-- Name: ix_coding_tests_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_coding_tests_id ON public.coding_tests USING btree (id);


--
-- Name: ix_communication_audit_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_communication_audit_logs_id ON public.communication_audit_logs USING btree (id);


--
-- Name: ix_communication_preferences_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_communication_preferences_id ON public.communication_preferences USING btree (id);


--
-- Name: ix_compensation_revisions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_compensation_revisions_id ON public.compensation_revisions USING btree (id);


--
-- Name: ix_conversation_messages_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_conversation_messages_id ON public.conversation_messages USING btree (id);


--
-- Name: ix_conversation_threads_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_conversation_threads_id ON public.conversation_threads USING btree (id);


--
-- Name: ix_countries_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_countries_id ON public.countries USING btree (id);


--
-- Name: ix_currencies_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_currencies_id ON public.currencies USING btree (id);


--
-- Name: ix_dashboard_layouts_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_dashboard_layouts_id ON public.dashboard_layouts USING btree (id);


--
-- Name: ix_dashboard_widgets_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_dashboard_widgets_id ON public.dashboard_widgets USING btree (id);


--
-- Name: ix_dashboards_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_dashboards_id ON public.dashboards USING btree (id);


--
-- Name: ix_degrees_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_degrees_id ON public.degrees USING btree (id);


--
-- Name: ix_delivery_metrics_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_delivery_metrics_id ON public.delivery_metrics USING btree (id);


--
-- Name: ix_departments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_departments_id ON public.departments USING btree (id);


--
-- Name: ix_designations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_designations_id ON public.designations USING btree (id);


--
-- Name: ix_document_chunks_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_document_chunks_id ON public.document_chunks USING btree (id);


--
-- Name: ix_document_embeddings_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_document_embeddings_id ON public.document_embeddings USING btree (id);


--
-- Name: ix_document_verifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_document_verifications_id ON public.document_verifications USING btree (id);


--
-- Name: ix_duplicate_candidates_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_duplicate_candidates_id ON public.duplicate_candidates USING btree (id);


--
-- Name: ix_email_attachments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_email_attachments_id ON public.email_attachments USING btree (id);


--
-- Name: ix_email_delivery_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_email_delivery_logs_id ON public.email_delivery_logs USING btree (id);


--
-- Name: ix_email_queue_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_email_queue_id ON public.email_queue USING btree (id);


--
-- Name: ix_email_templates_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_email_templates_id ON public.email_templates USING btree (id);


--
-- Name: ix_email_verifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_email_verifications_id ON public.email_verifications USING btree (id);


--
-- Name: ix_employee_conversion_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_employee_conversion_logs_id ON public.employee_conversion_logs USING btree (id);


--
-- Name: ix_employee_conversions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_employee_conversions_id ON public.employee_conversions USING btree (id);


--
-- Name: ix_employment_types_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_employment_types_id ON public.employment_types USING btree (id);


--
-- Name: ix_environment_variables_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_environment_variables_id ON public.environment_variables USING btree (id);


--
-- Name: ix_evaluation_criteria_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_evaluation_criteria_id ON public.evaluation_criteria USING btree (id);


--
-- Name: ix_evaluation_datasets_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_evaluation_datasets_id ON public.evaluation_datasets USING btree (id);


--
-- Name: ix_evaluation_scores_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_evaluation_scores_id ON public.evaluation_scores USING btree (id);


--
-- Name: ix_experience_levels_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_experience_levels_id ON public.experience_levels USING btree (id);


--
-- Name: ix_feature_flags_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_feature_flags_id ON public.feature_flags USING btree (id);


--
-- Name: ix_file_metadata_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_file_metadata_id ON public.file_metadata USING btree (id);


--
-- Name: ix_file_versions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_file_versions_id ON public.file_versions USING btree (id);


--
-- Name: ix_fine_tuning_datasets_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_fine_tuning_datasets_id ON public.fine_tuning_datasets USING btree (id);


--
-- Name: ix_hiring_completions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_hiring_completions_id ON public.hiring_completions USING btree (id);


--
-- Name: ix_hiring_plans_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_hiring_plans_id ON public.hiring_plans USING btree (id);


--
-- Name: ix_hiring_request_attachments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_hiring_request_attachments_id ON public.hiring_request_attachments USING btree (id);


--
-- Name: ix_hiring_request_comments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_hiring_request_comments_id ON public.hiring_request_comments USING btree (id);


--
-- Name: ix_hiring_requests_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_hiring_requests_id ON public.hiring_requests USING btree (id);


--
-- Name: ix_holiday_calendars_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_holiday_calendars_id ON public.holiday_calendars USING btree (id);


--
-- Name: ix_holidays_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_holidays_id ON public.holidays USING btree (id);


--
-- Name: ix_human_reviews_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_human_reviews_id ON public.human_reviews USING btree (id);


--
-- Name: ix_industries_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_industries_id ON public.industries USING btree (id);


--
-- Name: ix_integration_configurations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_integration_configurations_id ON public.integration_configurations USING btree (id);


--
-- Name: ix_integration_registries_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_integration_registries_id ON public.integration_registries USING btree (id);


--
-- Name: ix_internal_comments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_internal_comments_id ON public.internal_comments USING btree (id);


--
-- Name: ix_interview_analytics_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_analytics_id ON public.interview_analytics USING btree (id);


--
-- Name: ix_interview_attachments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_attachments_id ON public.interview_attachments USING btree (id);


--
-- Name: ix_interview_audit_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_audit_logs_id ON public.interview_audit_logs USING btree (id);


--
-- Name: ix_interview_calendar_events_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_calendar_events_id ON public.interview_calendar_events USING btree (id);


--
-- Name: ix_interview_cancellations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_cancellations_id ON public.interview_cancellations USING btree (id);


--
-- Name: ix_interview_decisions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_decisions_id ON public.interview_decisions USING btree (id);


--
-- Name: ix_interview_feedback_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_feedback_id ON public.interview_feedback USING btree (id);


--
-- Name: ix_interview_notifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_notifications_id ON public.interview_notifications USING btree (id);


--
-- Name: ix_interview_panel_members_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_panel_members_id ON public.interview_panel_members USING btree (id);


--
-- Name: ix_interview_panels_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_panels_id ON public.interview_panels USING btree (id);


--
-- Name: ix_interview_participants_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_participants_id ON public.interview_participants USING btree (id);


--
-- Name: ix_interview_plans_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_plans_id ON public.interview_plans USING btree (id);


--
-- Name: ix_interview_recordings_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_recordings_id ON public.interview_recordings USING btree (id);


--
-- Name: ix_interview_reschedules_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_reschedules_id ON public.interview_reschedules USING btree (id);


--
-- Name: ix_interview_rounds_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_rounds_id ON public.interview_rounds USING btree (id);


--
-- Name: ix_interview_schedules_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_schedules_id ON public.interview_schedules USING btree (id);


--
-- Name: ix_interview_scorecards_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_scorecards_id ON public.interview_scorecards USING btree (id);


--
-- Name: ix_interview_stage_templates_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_stage_templates_id ON public.interview_stage_templates USING btree (id);


--
-- Name: ix_interview_timelines_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_timelines_id ON public.interview_timelines USING btree (id);


--
-- Name: ix_interview_types_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interview_types_id ON public.interview_types USING btree (id);


--
-- Name: ix_interviewer_assignments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interviewer_assignments_id ON public.interviewer_assignments USING btree (id);


--
-- Name: ix_interviews_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_interviews_id ON public.interviews USING btree (id);


--
-- Name: ix_job_benefits_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_benefits_id ON public.job_benefits USING btree (id);


--
-- Name: ix_job_families_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_families_id ON public.job_families USING btree (id);


--
-- Name: ix_job_hiring_managers_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_hiring_managers_id ON public.job_hiring_managers USING btree (id);


--
-- Name: ix_job_locations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_locations_id ON public.job_locations USING btree (id);


--
-- Name: ix_job_publications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_publications_id ON public.job_publications USING btree (id);


--
-- Name: ix_job_qualifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_qualifications_id ON public.job_qualifications USING btree (id);


--
-- Name: ix_job_queues_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_queues_id ON public.job_queues USING btree (id);


--
-- Name: ix_job_recruiters_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_recruiters_id ON public.job_recruiters USING btree (id);


--
-- Name: ix_job_responsibilities_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_responsibilities_id ON public.job_responsibilities USING btree (id);


--
-- Name: ix_job_salary_ranges_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_salary_ranges_id ON public.job_salary_ranges USING btree (id);


--
-- Name: ix_job_skills_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_skills_id ON public.job_skills USING btree (id);


--
-- Name: ix_job_templates_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_templates_id ON public.job_templates USING btree (id);


--
-- Name: ix_job_versions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_job_versions_id ON public.job_versions USING btree (id);


--
-- Name: ix_jobs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_jobs_id ON public.jobs USING btree (id);


--
-- Name: ix_joining_audits_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_joining_audits_id ON public.joining_audits USING btree (id);


--
-- Name: ix_joining_confirmations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_joining_confirmations_id ON public.joining_confirmations USING btree (id);


--
-- Name: ix_knowledge_bases_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_knowledge_bases_id ON public.knowledge_bases USING btree (id);


--
-- Name: ix_knowledge_collections_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_knowledge_collections_id ON public.knowledge_collections USING btree (id);


--
-- Name: ix_knowledge_documents_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_knowledge_documents_id ON public.knowledge_documents USING btree (id);


--
-- Name: ix_languages_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_languages_id ON public.languages USING btree (id);


--
-- Name: ix_locations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_locations_id ON public.locations USING btree (id);


--
-- Name: ix_login_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_login_history_id ON public.login_history USING btree (id);


--
-- Name: ix_medical_verifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_medical_verifications_id ON public.medical_verifications USING btree (id);


--
-- Name: ix_meeting_invitations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_meeting_invitations_id ON public.meeting_invitations USING btree (id);


--
-- Name: ix_mentions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_mentions_id ON public.mentions USING btree (id);


--
-- Name: ix_message_attachments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_message_attachments_id ON public.message_attachments USING btree (id);


--
-- Name: ix_messaging_templates_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_messaging_templates_id ON public.messaging_templates USING btree (id);


--
-- Name: ix_mfa_configurations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_mfa_configurations_id ON public.mfa_configurations USING btree (id);


--
-- Name: ix_mfa_recovery_codes_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_mfa_recovery_codes_id ON public.mfa_recovery_codes USING btree (id);


--
-- Name: ix_notification_delivery_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notification_delivery_logs_id ON public.notification_delivery_logs USING btree (id);


--
-- Name: ix_notification_events_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notification_events_id ON public.notification_events USING btree (id);


--
-- Name: ix_notification_queue_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notification_queue_id ON public.notification_queue USING btree (id);


--
-- Name: ix_notification_templates_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notification_templates_id ON public.notification_templates USING btree (id);


--
-- Name: ix_notifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notifications_id ON public.notifications USING btree (id);


--
-- Name: ix_object_storage_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_object_storage_id ON public.object_storage USING btree (id);


--
-- Name: ix_offer_acceptance_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offer_acceptance_id ON public.offer_acceptance USING btree (id);


--
-- Name: ix_offer_approval_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offer_approval_history_id ON public.offer_approval_history USING btree (id);


--
-- Name: ix_offer_approvals_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offer_approvals_id ON public.offer_approvals USING btree (id);


--
-- Name: ix_offer_attachments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offer_attachments_id ON public.offer_attachments USING btree (id);


--
-- Name: ix_offer_audits_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offer_audits_id ON public.offer_audits USING btree (id);


--
-- Name: ix_offer_compensation_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offer_compensation_id ON public.offer_compensation USING btree (id);


--
-- Name: ix_offer_documents_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offer_documents_id ON public.offer_documents USING btree (id);


--
-- Name: ix_offer_negotiations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offer_negotiations_id ON public.offer_negotiations USING btree (id);


--
-- Name: ix_offer_rejections_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offer_rejections_id ON public.offer_rejections USING btree (id);


--
-- Name: ix_offer_templates_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offer_templates_id ON public.offer_templates USING btree (id);


--
-- Name: ix_offer_versions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offer_versions_id ON public.offer_versions USING btree (id);


--
-- Name: ix_offers_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_offers_id ON public.offers USING btree (id);


--
-- Name: ix_onboarding_checklists_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_onboarding_checklists_id ON public.onboarding_checklists USING btree (id);


--
-- Name: ix_onboarding_document_reviews_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_onboarding_document_reviews_id ON public.onboarding_document_reviews USING btree (id);


--
-- Name: ix_onboarding_document_submissions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_onboarding_document_submissions_id ON public.onboarding_document_submissions USING btree (id);


--
-- Name: ix_onboarding_documents_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_onboarding_documents_id ON public.onboarding_documents USING btree (id);


--
-- Name: ix_onboarding_plans_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_onboarding_plans_id ON public.onboarding_plans USING btree (id);


--
-- Name: ix_onboarding_task_assignments_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_onboarding_task_assignments_id ON public.onboarding_task_assignments USING btree (id);


--
-- Name: ix_onboarding_tasks_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_onboarding_tasks_id ON public.onboarding_tasks USING btree (id);


--
-- Name: ix_organization_settings_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_organization_settings_id ON public.organization_settings USING btree (id);


--
-- Name: ix_organizations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_organizations_id ON public.organizations USING btree (id);


--
-- Name: ix_password_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_password_history_id ON public.password_history USING btree (id);


--
-- Name: ix_password_reset_tokens_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_password_reset_tokens_id ON public.password_reset_tokens USING btree (id);


--
-- Name: ix_permission_groups_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_permission_groups_id ON public.permission_groups USING btree (id);


--
-- Name: ix_permissions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_permissions_id ON public.permissions USING btree (id);


--
-- Name: ix_pipeline_stage_mapping_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_pipeline_stage_mapping_id ON public.pipeline_stage_mapping USING btree (id);


--
-- Name: ix_probation_setups_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_probation_setups_id ON public.probation_setups USING btree (id);


--
-- Name: ix_prompt_evaluations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_prompt_evaluations_id ON public.prompt_evaluations USING btree (id);


--
-- Name: ix_prompt_templates_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_prompt_templates_id ON public.prompt_templates USING btree (id);


--
-- Name: ix_prompt_variables_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_prompt_variables_id ON public.prompt_variables USING btree (id);


--
-- Name: ix_prompt_versions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_prompt_versions_id ON public.prompt_versions USING btree (id);


--
-- Name: ix_publication_channels_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_publication_channels_id ON public.publication_channels USING btree (id);


--
-- Name: ix_publication_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_publication_history_id ON public.publication_history USING btree (id);


--
-- Name: ix_push_delivery_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_push_delivery_logs_id ON public.push_delivery_logs USING btree (id);


--
-- Name: ix_push_notifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_push_notifications_id ON public.push_notifications USING btree (id);


--
-- Name: ix_rag_citations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_rag_citations_id ON public.rag_citations USING btree (id);


--
-- Name: ix_rag_retrieval_results_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_rag_retrieval_results_id ON public.rag_retrieval_results USING btree (id);


--
-- Name: ix_rag_sessions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_rag_sessions_id ON public.rag_sessions USING btree (id);


--
-- Name: ix_recruiter_workloads_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_recruiter_workloads_id ON public.recruiter_workloads USING btree (id);


--
-- Name: ix_recruitment_audit_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_recruitment_audit_logs_id ON public.recruitment_audit_logs USING btree (id);


--
-- Name: ix_recruitment_closures_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_recruitment_closures_id ON public.recruitment_closures USING btree (id);


--
-- Name: ix_recruitment_metrics_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_recruitment_metrics_id ON public.recruitment_metrics USING btree (id);


--
-- Name: ix_recruitment_pipelines_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_recruitment_pipelines_id ON public.recruitment_pipelines USING btree (id);


--
-- Name: ix_recruitment_stages_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_recruitment_stages_id ON public.recruitment_stages USING btree (id);


--
-- Name: ix_refresh_tokens_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_refresh_tokens_id ON public.refresh_tokens USING btree (id);


--
-- Name: ix_report_definitions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_report_definitions_id ON public.report_definitions USING btree (id);


--
-- Name: ix_report_execution_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_report_execution_logs_id ON public.report_execution_logs USING btree (id);


--
-- Name: ix_report_parameters_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_report_parameters_id ON public.report_parameters USING btree (id);


--
-- Name: ix_requisition_approvals_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_requisition_approvals_id ON public.requisition_approvals USING btree (id);


--
-- Name: ix_resume_parsing_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_resume_parsing_history_id ON public.resume_parsing_history USING btree (id);


--
-- Name: ix_resume_versions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_resume_versions_id ON public.resume_versions USING btree (id);


--
-- Name: ix_role_permissions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_role_permissions_id ON public.role_permissions USING btree (id);


--
-- Name: ix_roles_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_roles_id ON public.roles USING btree (id);


--
-- Name: ix_salary_bands_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_salary_bands_id ON public.salary_bands USING btree (id);


--
-- Name: ix_scheduled_jobs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_scheduled_jobs_id ON public.scheduled_jobs USING btree (id);


--
-- Name: ix_scheduled_reports_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_scheduled_reports_id ON public.scheduled_reports USING btree (id);


--
-- Name: ix_scheduler_history_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_scheduler_history_id ON public.scheduler_history USING btree (id);


--
-- Name: ix_security_events_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_security_events_id ON public.security_events USING btree (id);


--
-- Name: ix_sessions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sessions_id ON public.sessions USING btree (id);


--
-- Name: ix_shifts_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_shifts_id ON public.shifts USING btree (id);


--
-- Name: ix_skills_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_skills_id ON public.skills USING btree (id);


--
-- Name: ix_sms_queue_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sms_queue_id ON public.sms_queue USING btree (id);


--
-- Name: ix_stage_sla_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_stage_sla_id ON public.stage_sla USING btree (id);


--
-- Name: ix_states_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_states_id ON public.states USING btree (id);


--
-- Name: ix_storage_quotas_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_storage_quotas_id ON public.storage_quotas USING btree (id);


--
-- Name: ix_system_settings_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_system_settings_id ON public.system_settings USING btree (id);


--
-- Name: ix_tenant_preferences_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tenant_preferences_id ON public.tenant_preferences USING btree (id);


--
-- Name: ix_timezones_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_timezones_id ON public.timezones USING btree (id);


--
-- Name: ix_token_usage_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_token_usage_id ON public.token_usage USING btree (id);


--
-- Name: ix_universities_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_universities_id ON public.universities USING btree (id);


--
-- Name: ix_user_devices_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_devices_id ON public.user_devices USING btree (id);


--
-- Name: ix_user_preferences_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_preferences_id ON public.user_preferences USING btree (id);


--
-- Name: ix_user_profiles_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_profiles_id ON public.user_profiles USING btree (id);


--
-- Name: ix_user_roles_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_roles_id ON public.user_roles USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_webhook_deliveries_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_webhook_deliveries_id ON public.webhook_deliveries USING btree (id);


--
-- Name: ix_webhook_events_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_webhook_events_id ON public.webhook_events USING btree (id);


--
-- Name: ix_webhook_logs_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_webhook_logs_id ON public.webhook_logs USING btree (id);


--
-- Name: ix_webhook_registries_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_webhook_registries_id ON public.webhook_registries USING btree (id);


--
-- Name: ix_webhook_subscriptions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_webhook_subscriptions_id ON public.webhook_subscriptions USING btree (id);


--
-- Name: ix_welcome_kits_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_welcome_kits_id ON public.welcome_kits USING btree (id);


--
-- Name: ix_whatsapp_queue_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_whatsapp_queue_id ON public.whatsapp_queue USING btree (id);


--
-- Name: ix_widget_configurations_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_widget_configurations_id ON public.widget_configurations USING btree (id);


--
-- Name: ix_widget_data_queries_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_widget_data_queries_id ON public.widget_data_queries USING btree (id);


--
-- Name: ix_work_modes_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_work_modes_id ON public.work_modes USING btree (id);


--
-- Name: activity_logs activity_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: ai_agent_capabilities ai_agent_capabilities_agent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_agent_capabilities
    ADD CONSTRAINT ai_agent_capabilities_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES public.ai_agents(id);


--
-- Name: ai_behavior_analysis ai_behavior_analysis_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_behavior_analysis
    ADD CONSTRAINT ai_behavior_analysis_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: ai_candidate_feedback ai_candidate_feedback_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_candidate_feedback
    ADD CONSTRAINT ai_candidate_feedback_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: ai_candidate_rankings ai_candidate_rankings_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_candidate_rankings
    ADD CONSTRAINT ai_candidate_rankings_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.candidate_applications(id);


--
-- Name: ai_candidate_rankings ai_candidate_rankings_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_candidate_rankings
    ADD CONSTRAINT ai_candidate_rankings_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: ai_cost_tracking ai_cost_tracking_execution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_cost_tracking
    ADD CONSTRAINT ai_cost_tracking_execution_id_fkey FOREIGN KEY (execution_id) REFERENCES public.ai_executions(id);


--
-- Name: ai_decision_support ai_decision_support_recommendation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_decision_support
    ADD CONSTRAINT ai_decision_support_recommendation_id_fkey FOREIGN KEY (recommendation_id) REFERENCES public.ai_recommendations(id);


--
-- Name: ai_execution_logs ai_execution_logs_execution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_execution_logs
    ADD CONSTRAINT ai_execution_logs_execution_id_fkey FOREIGN KEY (execution_id) REFERENCES public.ai_executions(id);


--
-- Name: ai_executions ai_executions_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_executions
    ADD CONSTRAINT ai_executions_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.ai_requests(id);


--
-- Name: ai_feedback ai_feedback_execution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_feedback
    ADD CONSTRAINT ai_feedback_execution_id_fkey FOREIGN KEY (execution_id) REFERENCES public.ai_executions(id);


--
-- Name: ai_interview_analysis ai_interview_analysis_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_interview_analysis
    ADD CONSTRAINT ai_interview_analysis_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: ai_interview_scores ai_interview_scores_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_interview_scores
    ADD CONSTRAINT ai_interview_scores_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: ai_interview_summary ai_interview_summary_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_interview_summary
    ADD CONSTRAINT ai_interview_summary_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: ai_job_recommendations ai_job_recommendations_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_job_recommendations
    ADD CONSTRAINT ai_job_recommendations_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: ai_messages ai_messages_conversation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_messages
    ADD CONSTRAINT ai_messages_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES public.ai_conversations(id);


--
-- Name: ai_model_configurations ai_model_configurations_model_version_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_model_configurations
    ADD CONSTRAINT ai_model_configurations_model_version_id_fkey FOREIGN KEY (model_version_id) REFERENCES public.ai_model_versions(id);


--
-- Name: ai_model_versions ai_model_versions_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_model_versions
    ADD CONSTRAINT ai_model_versions_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.ai_models(id);


--
-- Name: ai_models ai_models_provider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_models
    ADD CONSTRAINT ai_models_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES public.ai_model_providers(id);


--
-- Name: ai_recruitment_insights ai_recruitment_insights_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_recruitment_insights
    ADD CONSTRAINT ai_recruitment_insights_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: ai_responses ai_responses_execution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_responses
    ADD CONSTRAINT ai_responses_execution_id_fkey FOREIGN KEY (execution_id) REFERENCES public.ai_executions(id);


--
-- Name: ai_screening_results ai_screening_results_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_screening_results
    ADD CONSTRAINT ai_screening_results_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.candidate_applications(id);


--
-- Name: ai_summaries ai_summaries_conversation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_summaries
    ADD CONSTRAINT ai_summaries_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES public.ai_conversations(id);


--
-- Name: ai_tool_executions ai_tool_executions_execution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_tool_executions
    ADD CONSTRAINT ai_tool_executions_execution_id_fkey FOREIGN KEY (execution_id) REFERENCES public.ai_executions(id);


--
-- Name: ai_tool_executions ai_tool_executions_tool_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_tool_executions
    ADD CONSTRAINT ai_tool_executions_tool_id_fkey FOREIGN KEY (tool_id) REFERENCES public.ai_tools(id);


--
-- Name: ai_tool_permissions ai_tool_permissions_tool_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_tool_permissions
    ADD CONSTRAINT ai_tool_permissions_tool_id_fkey FOREIGN KEY (tool_id) REFERENCES public.ai_tools(id);


--
-- Name: ai_workflow_steps ai_workflow_steps_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_workflow_steps
    ADD CONSTRAINT ai_workflow_steps_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.ai_workflows(id);


--
-- Name: api_keys api_keys_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.api_keys
    ADD CONSTRAINT api_keys_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: application_documents application_documents_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_documents
    ADD CONSTRAINT application_documents_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.candidate_applications(id);


--
-- Name: application_notes application_notes_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_notes
    ADD CONSTRAINT application_notes_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.candidate_applications(id);


--
-- Name: application_screening application_screening_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_screening
    ADD CONSTRAINT application_screening_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.candidate_applications(id);


--
-- Name: application_stage_history application_stage_history_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_stage_history
    ADD CONSTRAINT application_stage_history_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.candidate_applications(id);


--
-- Name: application_stage_history application_stage_history_from_stage_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_stage_history
    ADD CONSTRAINT application_stage_history_from_stage_id_fkey FOREIGN KEY (from_stage_id) REFERENCES public.recruitment_stages(id);


--
-- Name: application_stage_history application_stage_history_to_stage_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_stage_history
    ADD CONSTRAINT application_stage_history_to_stage_id_fkey FOREIGN KEY (to_stage_id) REFERENCES public.recruitment_stages(id);


--
-- Name: application_tags application_tags_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_tags
    ADD CONSTRAINT application_tags_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.candidate_applications(id);


--
-- Name: approval_history approval_history_hiring_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.approval_history
    ADD CONSTRAINT approval_history_hiring_request_id_fkey FOREIGN KEY (hiring_request_id) REFERENCES public.hiring_requests(id);


--
-- Name: assessment_answers assessment_answers_attempt_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment_answers
    ADD CONSTRAINT assessment_answers_attempt_id_fkey FOREIGN KEY (attempt_id) REFERENCES public.assessment_attempts(id);


--
-- Name: assessment_answers assessment_answers_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment_answers
    ADD CONSTRAINT assessment_answers_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.assessment_questions(id);


--
-- Name: assessment_attempts assessment_attempts_assessment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment_attempts
    ADD CONSTRAINT assessment_attempts_assessment_id_fkey FOREIGN KEY (assessment_id) REFERENCES public.assessments(id);


--
-- Name: assessment_questions assessment_questions_assessment_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessment_questions
    ADD CONSTRAINT assessment_questions_assessment_template_id_fkey FOREIGN KEY (assessment_template_id) REFERENCES public.assessment_templates(id);


--
-- Name: assessments assessments_assessment_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assessments
    ADD CONSTRAINT assessments_assessment_template_id_fkey FOREIGN KEY (assessment_template_id) REFERENCES public.assessment_templates(id);


--
-- Name: assignment_submissions assignment_submissions_attempt_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assignment_submissions
    ADD CONSTRAINT assignment_submissions_attempt_id_fkey FOREIGN KEY (attempt_id) REFERENCES public.assessment_attempts(id);


--
-- Name: audit_logs audit_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: background_check_items background_check_items_bg_verification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.background_check_items
    ADD CONSTRAINT background_check_items_bg_verification_id_fkey FOREIGN KEY (bg_verification_id) REFERENCES public.background_verifications(id);


--
-- Name: benchmark_results benchmark_results_dataset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.benchmark_results
    ADD CONSTRAINT benchmark_results_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES public.evaluation_datasets(id);


--
-- Name: benchmark_results benchmark_results_model_version_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.benchmark_results
    ADD CONSTRAINT benchmark_results_model_version_id_fkey FOREIGN KEY (model_version_id) REFERENCES public.ai_model_versions(id);


--
-- Name: branches branches_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.branches
    ADD CONSTRAINT branches_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.locations(id);


--
-- Name: branches branches_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.branches
    ADD CONSTRAINT branches_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: business_units business_units_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_units
    ADD CONSTRAINT business_units_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: candidate_achievements candidate_achievements_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_achievements
    ADD CONSTRAINT candidate_achievements_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_activities candidate_activities_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_activities
    ADD CONSTRAINT candidate_activities_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_addresses candidate_addresses_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_addresses
    ADD CONSTRAINT candidate_addresses_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_ai_profiles candidate_ai_profiles_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_ai_profiles
    ADD CONSTRAINT candidate_ai_profiles_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_ai_recommendations candidate_ai_recommendations_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_ai_recommendations
    ADD CONSTRAINT candidate_ai_recommendations_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_ai_summaries candidate_ai_summaries_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_ai_summaries
    ADD CONSTRAINT candidate_ai_summaries_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_applications candidate_applications_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_applications
    ADD CONSTRAINT candidate_applications_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_applications candidate_applications_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_applications
    ADD CONSTRAINT candidate_applications_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: candidate_audit_logs candidate_audit_logs_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_audit_logs
    ADD CONSTRAINT candidate_audit_logs_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_availability candidate_availability_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_availability
    ADD CONSTRAINT candidate_availability_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_blacklist candidate_blacklist_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_blacklist
    ADD CONSTRAINT candidate_blacklist_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_blacklist candidate_blacklist_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_blacklist
    ADD CONSTRAINT candidate_blacklist_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: candidate_certifications candidate_certifications_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_certifications
    ADD CONSTRAINT candidate_certifications_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_consents candidate_consents_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_consents
    ADD CONSTRAINT candidate_consents_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_documents candidate_documents_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_documents
    ADD CONSTRAINT candidate_documents_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_documents candidate_documents_document_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_documents
    ADD CONSTRAINT candidate_documents_document_type_id_fkey FOREIGN KEY (document_type_id) REFERENCES public.candidate_document_types(id);


--
-- Name: candidate_education candidate_education_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_education
    ADD CONSTRAINT candidate_education_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_embeddings candidate_embeddings_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_embeddings
    ADD CONSTRAINT candidate_embeddings_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_embeddings candidate_embeddings_resume_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_embeddings
    ADD CONSTRAINT candidate_embeddings_resume_id_fkey FOREIGN KEY (resume_id) REFERENCES public.candidate_resumes(id);


--
-- Name: candidate_emergency_contacts candidate_emergency_contacts_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_emergency_contacts
    ADD CONSTRAINT candidate_emergency_contacts_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_experience candidate_experience_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_experience
    ADD CONSTRAINT candidate_experience_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_languages candidate_languages_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_languages
    ADD CONSTRAINT candidate_languages_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_merge_history candidate_merge_history_master_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_merge_history
    ADD CONSTRAINT candidate_merge_history_master_candidate_id_fkey FOREIGN KEY (master_candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_merge_history candidate_merge_history_merged_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_merge_history
    ADD CONSTRAINT candidate_merge_history_merged_candidate_id_fkey FOREIGN KEY (merged_candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_merge_history candidate_merge_history_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_merge_history
    ADD CONSTRAINT candidate_merge_history_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: candidate_notes candidate_notes_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_notes
    ADD CONSTRAINT candidate_notes_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_ownership candidate_ownership_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_ownership
    ADD CONSTRAINT candidate_ownership_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_patents candidate_patents_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_patents
    ADD CONSTRAINT candidate_patents_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_portfolios candidate_portfolios_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_portfolios
    ADD CONSTRAINT candidate_portfolios_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_preferences candidate_preferences_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_preferences
    ADD CONSTRAINT candidate_preferences_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_profiles candidate_profiles_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_profiles
    ADD CONSTRAINT candidate_profiles_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_projects candidate_projects_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_projects
    ADD CONSTRAINT candidate_projects_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_publications candidate_publications_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_publications
    ADD CONSTRAINT candidate_publications_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_references candidate_references_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_references
    ADD CONSTRAINT candidate_references_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_resumes candidate_resumes_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_resumes
    ADD CONSTRAINT candidate_resumes_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_salary_expectations candidate_salary_expectations_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_salary_expectations
    ADD CONSTRAINT candidate_salary_expectations_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_skills candidate_skills_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_skills
    ADD CONSTRAINT candidate_skills_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_skills candidate_skills_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_skills
    ADD CONSTRAINT candidate_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(id);


--
-- Name: candidate_social_profiles candidate_social_profiles_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_social_profiles
    ADD CONSTRAINT candidate_social_profiles_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_source_history candidate_source_history_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_source_history
    ADD CONSTRAINT candidate_source_history_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_source_history candidate_source_history_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_source_history
    ADD CONSTRAINT candidate_source_history_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.candidate_sources(id);


--
-- Name: candidate_tags candidate_tags_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_tags
    ADD CONSTRAINT candidate_tags_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidate_timeline candidate_timeline_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidate_timeline
    ADD CONSTRAINT candidate_timeline_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidates candidates_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT candidates_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: cities cities_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_state_id_fkey FOREIGN KEY (state_id) REFERENCES public.states(id);


--
-- Name: coding_tests coding_tests_assessment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coding_tests
    ADD CONSTRAINT coding_tests_assessment_id_fkey FOREIGN KEY (assessment_id) REFERENCES public.assessments(id);


--
-- Name: compensation_revisions compensation_revisions_negotiation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compensation_revisions
    ADD CONSTRAINT compensation_revisions_negotiation_id_fkey FOREIGN KEY (negotiation_id) REFERENCES public.offer_negotiations(id);


--
-- Name: conversation_messages conversation_messages_thread_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conversation_messages
    ADD CONSTRAINT conversation_messages_thread_id_fkey FOREIGN KEY (thread_id) REFERENCES public.conversation_threads(id);


--
-- Name: dashboard_layouts dashboard_layouts_dashboard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dashboard_layouts
    ADD CONSTRAINT dashboard_layouts_dashboard_id_fkey FOREIGN KEY (dashboard_id) REFERENCES public.dashboards(id);


--
-- Name: dashboard_widgets dashboard_widgets_dashboard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dashboard_widgets
    ADD CONSTRAINT dashboard_widgets_dashboard_id_fkey FOREIGN KEY (dashboard_id) REFERENCES public.dashboards(id);


--
-- Name: departments departments_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: departments departments_parent_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_parent_department_id_fkey FOREIGN KEY (parent_department_id) REFERENCES public.departments(id);


--
-- Name: designations designations_job_family_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.designations
    ADD CONSTRAINT designations_job_family_id_fkey FOREIGN KEY (job_family_id) REFERENCES public.job_families(id);


--
-- Name: designations designations_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.designations
    ADD CONSTRAINT designations_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: document_chunks document_chunks_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_chunks
    ADD CONSTRAINT document_chunks_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.knowledge_documents(id);


--
-- Name: document_embeddings document_embeddings_chunk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_embeddings
    ADD CONSTRAINT document_embeddings_chunk_id_fkey FOREIGN KEY (chunk_id) REFERENCES public.document_chunks(id);


--
-- Name: duplicate_candidates duplicate_candidates_duplicate_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.duplicate_candidates
    ADD CONSTRAINT duplicate_candidates_duplicate_candidate_id_fkey FOREIGN KEY (duplicate_candidate_id) REFERENCES public.candidates(id);


--
-- Name: duplicate_candidates duplicate_candidates_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.duplicate_candidates
    ADD CONSTRAINT duplicate_candidates_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: duplicate_candidates duplicate_candidates_primary_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.duplicate_candidates
    ADD CONSTRAINT duplicate_candidates_primary_candidate_id_fkey FOREIGN KEY (primary_candidate_id) REFERENCES public.candidates(id);


--
-- Name: email_attachments email_attachments_email_queue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_attachments
    ADD CONSTRAINT email_attachments_email_queue_id_fkey FOREIGN KEY (email_queue_id) REFERENCES public.email_queue(id);


--
-- Name: email_delivery_logs email_delivery_logs_email_queue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_delivery_logs
    ADD CONSTRAINT email_delivery_logs_email_queue_id_fkey FOREIGN KEY (email_queue_id) REFERENCES public.email_queue(id);


--
-- Name: email_verifications email_verifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_verifications
    ADD CONSTRAINT email_verifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: evaluation_scores evaluation_scores_evaluation_criterion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_scores
    ADD CONSTRAINT evaluation_scores_evaluation_criterion_id_fkey FOREIGN KEY (evaluation_criterion_id) REFERENCES public.evaluation_criteria(id);


--
-- Name: evaluation_scores evaluation_scores_interview_feedback_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_scores
    ADD CONSTRAINT evaluation_scores_interview_feedback_id_fkey FOREIGN KEY (interview_feedback_id) REFERENCES public.interview_feedback(id);


--
-- Name: file_versions file_versions_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.file_versions
    ADD CONSTRAINT file_versions_file_id_fkey FOREIGN KEY (file_id) REFERENCES public.file_metadata(id);


--
-- Name: hiring_plans hiring_plans_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_plans
    ADD CONSTRAINT hiring_plans_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: hiring_request_attachments hiring_request_attachments_hiring_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_request_attachments
    ADD CONSTRAINT hiring_request_attachments_hiring_request_id_fkey FOREIGN KEY (hiring_request_id) REFERENCES public.hiring_requests(id);


--
-- Name: hiring_request_comments hiring_request_comments_hiring_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_request_comments
    ADD CONSTRAINT hiring_request_comments_hiring_request_id_fkey FOREIGN KEY (hiring_request_id) REFERENCES public.hiring_requests(id);


--
-- Name: hiring_requests hiring_requests_hiring_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_requests
    ADD CONSTRAINT hiring_requests_hiring_plan_id_fkey FOREIGN KEY (hiring_plan_id) REFERENCES public.hiring_plans(id);


--
-- Name: hiring_requests hiring_requests_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hiring_requests
    ADD CONSTRAINT hiring_requests_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: holiday_calendars holiday_calendars_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.holiday_calendars
    ADD CONSTRAINT holiday_calendars_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: holidays holidays_holiday_calendar_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.holidays
    ADD CONSTRAINT holidays_holiday_calendar_id_fkey FOREIGN KEY (holiday_calendar_id) REFERENCES public.holiday_calendars(id);


--
-- Name: human_reviews human_reviews_execution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.human_reviews
    ADD CONSTRAINT human_reviews_execution_id_fkey FOREIGN KEY (execution_id) REFERENCES public.ai_executions(id);


--
-- Name: integration_configurations integration_configurations_integration_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.integration_configurations
    ADD CONSTRAINT integration_configurations_integration_id_fkey FOREIGN KEY (integration_id) REFERENCES public.integration_registries(id);


--
-- Name: interview_attachments interview_attachments_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_attachments
    ADD CONSTRAINT interview_attachments_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_audit_logs interview_audit_logs_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_audit_logs
    ADD CONSTRAINT interview_audit_logs_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_calendar_events interview_calendar_events_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_calendar_events
    ADD CONSTRAINT interview_calendar_events_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_cancellations interview_cancellations_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_cancellations
    ADD CONSTRAINT interview_cancellations_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_decisions interview_decisions_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_decisions
    ADD CONSTRAINT interview_decisions_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_feedback interview_feedback_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_feedback
    ADD CONSTRAINT interview_feedback_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_notifications interview_notifications_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_notifications
    ADD CONSTRAINT interview_notifications_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_panel_members interview_panel_members_panel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_panel_members
    ADD CONSTRAINT interview_panel_members_panel_id_fkey FOREIGN KEY (panel_id) REFERENCES public.interview_panels(id);


--
-- Name: interview_panels interview_panels_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_panels
    ADD CONSTRAINT interview_panels_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_participants interview_participants_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_participants
    ADD CONSTRAINT interview_participants_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_recordings interview_recordings_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_recordings
    ADD CONSTRAINT interview_recordings_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_reschedules interview_reschedules_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_reschedules
    ADD CONSTRAINT interview_reschedules_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_rounds interview_rounds_interview_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_rounds
    ADD CONSTRAINT interview_rounds_interview_plan_id_fkey FOREIGN KEY (interview_plan_id) REFERENCES public.interview_plans(id);


--
-- Name: interview_schedules interview_schedules_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_schedules
    ADD CONSTRAINT interview_schedules_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_scorecards interview_scorecards_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_scorecards
    ADD CONSTRAINT interview_scorecards_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interview_timelines interview_timelines_interview_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interview_timelines
    ADD CONSTRAINT interview_timelines_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(id);


--
-- Name: interviews interviews_interview_round_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interviews
    ADD CONSTRAINT interviews_interview_round_id_fkey FOREIGN KEY (interview_round_id) REFERENCES public.interview_rounds(id);


--
-- Name: interviews interviews_interview_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.interviews
    ADD CONSTRAINT interviews_interview_type_id_fkey FOREIGN KEY (interview_type_id) REFERENCES public.interview_types(id);


--
-- Name: job_benefits job_benefits_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_benefits
    ADD CONSTRAINT job_benefits_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_hiring_managers job_hiring_managers_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_hiring_managers
    ADD CONSTRAINT job_hiring_managers_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_locations job_locations_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_locations
    ADD CONSTRAINT job_locations_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_publications job_publications_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_publications
    ADD CONSTRAINT job_publications_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.publication_channels(id);


--
-- Name: job_publications job_publications_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_publications
    ADD CONSTRAINT job_publications_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_qualifications job_qualifications_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_qualifications
    ADD CONSTRAINT job_qualifications_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_recruiters job_recruiters_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_recruiters
    ADD CONSTRAINT job_recruiters_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_responsibilities job_responsibilities_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_responsibilities
    ADD CONSTRAINT job_responsibilities_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_salary_ranges job_salary_ranges_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_salary_ranges
    ADD CONSTRAINT job_salary_ranges_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_skills job_skills_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_templates job_templates_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_templates
    ADD CONSTRAINT job_templates_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: job_versions job_versions_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_versions
    ADD CONSTRAINT job_versions_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: jobs jobs_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id);


--
-- Name: jobs jobs_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: joining_confirmations joining_confirmations_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.joining_confirmations
    ADD CONSTRAINT joining_confirmations_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: knowledge_collections knowledge_collections_kb_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.knowledge_collections
    ADD CONSTRAINT knowledge_collections_kb_id_fkey FOREIGN KEY (kb_id) REFERENCES public.knowledge_bases(id);


--
-- Name: knowledge_documents knowledge_documents_collection_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.knowledge_documents
    ADD CONSTRAINT knowledge_documents_collection_id_fkey FOREIGN KEY (collection_id) REFERENCES public.knowledge_collections(id);


--
-- Name: locations locations_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.cities(id);


--
-- Name: locations locations_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: login_history login_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.login_history
    ADD CONSTRAINT login_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: meeting_invitations meeting_invitations_calendar_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meeting_invitations
    ADD CONSTRAINT meeting_invitations_calendar_event_id_fkey FOREIGN KEY (calendar_event_id) REFERENCES public.calendar_events(id);


--
-- Name: mentions mentions_comment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentions
    ADD CONSTRAINT mentions_comment_id_fkey FOREIGN KEY (comment_id) REFERENCES public.internal_comments(id);


--
-- Name: mentions mentions_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mentions
    ADD CONSTRAINT mentions_message_id_fkey FOREIGN KEY (message_id) REFERENCES public.conversation_messages(id);


--
-- Name: message_attachments message_attachments_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.message_attachments
    ADD CONSTRAINT message_attachments_message_id_fkey FOREIGN KEY (message_id) REFERENCES public.conversation_messages(id);


--
-- Name: mfa_configurations mfa_configurations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_configurations
    ADD CONSTRAINT mfa_configurations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: mfa_recovery_codes mfa_recovery_codes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mfa_recovery_codes
    ADD CONSTRAINT mfa_recovery_codes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: notification_delivery_logs notification_delivery_logs_notification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_delivery_logs
    ADD CONSTRAINT notification_delivery_logs_notification_id_fkey FOREIGN KEY (notification_id) REFERENCES public.notifications(id);


--
-- Name: notification_queue notification_queue_notification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_queue
    ADD CONSTRAINT notification_queue_notification_id_fkey FOREIGN KEY (notification_id) REFERENCES public.notifications(id);


--
-- Name: offer_acceptance offer_acceptance_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_acceptance
    ADD CONSTRAINT offer_acceptance_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: offer_approval_history offer_approval_history_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_approval_history
    ADD CONSTRAINT offer_approval_history_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: offer_approvals offer_approvals_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_approvals
    ADD CONSTRAINT offer_approvals_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: offer_attachments offer_attachments_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_attachments
    ADD CONSTRAINT offer_attachments_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: offer_audits offer_audits_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_audits
    ADD CONSTRAINT offer_audits_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: offer_compensation offer_compensation_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_compensation
    ADD CONSTRAINT offer_compensation_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: offer_documents offer_documents_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_documents
    ADD CONSTRAINT offer_documents_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: offer_negotiations offer_negotiations_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_negotiations
    ADD CONSTRAINT offer_negotiations_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: offer_rejections offer_rejections_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_rejections
    ADD CONSTRAINT offer_rejections_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: offer_versions offer_versions_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer_versions
    ADD CONSTRAINT offer_versions_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offers(id);


--
-- Name: onboarding_document_reviews onboarding_document_reviews_submission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_document_reviews
    ADD CONSTRAINT onboarding_document_reviews_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES public.onboarding_document_submissions(id);


--
-- Name: onboarding_document_submissions onboarding_document_submissions_onboarding_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_document_submissions
    ADD CONSTRAINT onboarding_document_submissions_onboarding_document_id_fkey FOREIGN KEY (onboarding_document_id) REFERENCES public.onboarding_documents(id);


--
-- Name: onboarding_task_assignments onboarding_task_assignments_onboarding_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_task_assignments
    ADD CONSTRAINT onboarding_task_assignments_onboarding_task_id_fkey FOREIGN KEY (onboarding_task_id) REFERENCES public.onboarding_tasks(id);


--
-- Name: onboarding_tasks onboarding_tasks_onboarding_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.onboarding_tasks
    ADD CONSTRAINT onboarding_tasks_onboarding_plan_id_fkey FOREIGN KEY (onboarding_plan_id) REFERENCES public.onboarding_plans(id);


--
-- Name: organizations organizations_industry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_industry_id_fkey FOREIGN KEY (industry_id) REFERENCES public.industries(id);


--
-- Name: password_history password_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_history
    ADD CONSTRAINT password_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: password_reset_tokens password_reset_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: pipeline_stage_mapping pipeline_stage_mapping_pipeline_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pipeline_stage_mapping
    ADD CONSTRAINT pipeline_stage_mapping_pipeline_id_fkey FOREIGN KEY (pipeline_id) REFERENCES public.recruitment_pipelines(id);


--
-- Name: pipeline_stage_mapping pipeline_stage_mapping_stage_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pipeline_stage_mapping
    ADD CONSTRAINT pipeline_stage_mapping_stage_id_fkey FOREIGN KEY (stage_id) REFERENCES public.recruitment_stages(id);


--
-- Name: prompt_evaluations prompt_evaluations_version_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prompt_evaluations
    ADD CONSTRAINT prompt_evaluations_version_id_fkey FOREIGN KEY (version_id) REFERENCES public.prompt_versions(id);


--
-- Name: prompt_variables prompt_variables_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prompt_variables
    ADD CONSTRAINT prompt_variables_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.prompt_templates(id);


--
-- Name: prompt_versions prompt_versions_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prompt_versions
    ADD CONSTRAINT prompt_versions_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.prompt_templates(id);


--
-- Name: publication_history publication_history_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publication_history
    ADD CONSTRAINT publication_history_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.publication_channels(id);


--
-- Name: publication_history publication_history_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.publication_history
    ADD CONSTRAINT publication_history_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: push_delivery_logs push_delivery_logs_push_notification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.push_delivery_logs
    ADD CONSTRAINT push_delivery_logs_push_notification_id_fkey FOREIGN KEY (push_notification_id) REFERENCES public.push_notifications(id);


--
-- Name: rag_citations rag_citations_retrieval_result_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rag_citations
    ADD CONSTRAINT rag_citations_retrieval_result_id_fkey FOREIGN KEY (retrieval_result_id) REFERENCES public.rag_retrieval_results(id);


--
-- Name: rag_retrieval_results rag_retrieval_results_chunk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rag_retrieval_results
    ADD CONSTRAINT rag_retrieval_results_chunk_id_fkey FOREIGN KEY (chunk_id) REFERENCES public.document_chunks(id);


--
-- Name: rag_retrieval_results rag_retrieval_results_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rag_retrieval_results
    ADD CONSTRAINT rag_retrieval_results_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.rag_sessions(id);


--
-- Name: recruiter_workloads recruiter_workloads_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruiter_workloads
    ADD CONSTRAINT recruiter_workloads_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: recruitment_audit_logs recruitment_audit_logs_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_audit_logs
    ADD CONSTRAINT recruitment_audit_logs_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.candidate_applications(id);


--
-- Name: recruitment_audit_logs recruitment_audit_logs_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_audit_logs
    ADD CONSTRAINT recruitment_audit_logs_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: recruitment_audit_logs recruitment_audit_logs_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_audit_logs
    ADD CONSTRAINT recruitment_audit_logs_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: recruitment_closures recruitment_closures_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_closures
    ADD CONSTRAINT recruitment_closures_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: recruitment_metrics recruitment_metrics_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_metrics
    ADD CONSTRAINT recruitment_metrics_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: recruitment_pipelines recruitment_pipelines_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_pipelines
    ADD CONSTRAINT recruitment_pipelines_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: recruitment_stages recruitment_stages_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruitment_stages
    ADD CONSTRAINT recruitment_stages_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: refresh_tokens refresh_tokens_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id);


--
-- Name: report_execution_logs report_execution_logs_scheduled_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.report_execution_logs
    ADD CONSTRAINT report_execution_logs_scheduled_report_id_fkey FOREIGN KEY (scheduled_report_id) REFERENCES public.scheduled_reports(id);


--
-- Name: report_parameters report_parameters_report_definition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.report_parameters
    ADD CONSTRAINT report_parameters_report_definition_id_fkey FOREIGN KEY (report_definition_id) REFERENCES public.report_definitions(id);


--
-- Name: requisition_approvals requisition_approvals_hiring_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requisition_approvals
    ADD CONSTRAINT requisition_approvals_hiring_request_id_fkey FOREIGN KEY (hiring_request_id) REFERENCES public.hiring_requests(id);


--
-- Name: resume_parsing_history resume_parsing_history_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resume_parsing_history
    ADD CONSTRAINT resume_parsing_history_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: resume_parsing_history resume_parsing_history_resume_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resume_parsing_history
    ADD CONSTRAINT resume_parsing_history_resume_id_fkey FOREIGN KEY (resume_id) REFERENCES public.candidate_resumes(id);


--
-- Name: resume_versions resume_versions_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resume_versions
    ADD CONSTRAINT resume_versions_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: resume_versions resume_versions_resume_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resume_versions
    ADD CONSTRAINT resume_versions_resume_id_fkey FOREIGN KEY (resume_id) REFERENCES public.candidate_resumes(id);


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: roles roles_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: salary_bands salary_bands_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salary_bands
    ADD CONSTRAINT salary_bands_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


--
-- Name: salary_bands salary_bands_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salary_bands
    ADD CONSTRAINT salary_bands_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: scheduled_reports scheduled_reports_report_definition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scheduled_reports
    ADD CONSTRAINT scheduled_reports_report_definition_id_fkey FOREIGN KEY (report_definition_id) REFERENCES public.report_definitions(id);


--
-- Name: scheduler_history scheduler_history_scheduled_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scheduler_history
    ADD CONSTRAINT scheduler_history_scheduled_job_id_fkey FOREIGN KEY (scheduled_job_id) REFERENCES public.scheduled_jobs(id);


--
-- Name: security_events security_events_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_events
    ADD CONSTRAINT security_events_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: shifts shifts_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shifts
    ADD CONSTRAINT shifts_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: stage_sla stage_sla_pipeline_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stage_sla
    ADD CONSTRAINT stage_sla_pipeline_id_fkey FOREIGN KEY (pipeline_id) REFERENCES public.recruitment_pipelines(id);


--
-- Name: stage_sla stage_sla_stage_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stage_sla
    ADD CONSTRAINT stage_sla_stage_id_fkey FOREIGN KEY (stage_id) REFERENCES public.recruitment_stages(id);


--
-- Name: states states_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.states
    ADD CONSTRAINT states_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.countries(id);


--
-- Name: token_usage token_usage_execution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token_usage
    ADD CONSTRAINT token_usage_execution_id_fkey FOREIGN KEY (execution_id) REFERENCES public.ai_executions(id);


--
-- Name: universities universities_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.universities
    ADD CONSTRAINT universities_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.countries(id);


--
-- Name: user_preferences user_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_profiles user_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: webhook_deliveries webhook_deliveries_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.webhook_deliveries
    ADD CONSTRAINT webhook_deliveries_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.webhook_subscriptions(id);


--
-- Name: webhook_events webhook_events_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.webhook_events
    ADD CONSTRAINT webhook_events_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.webhook_subscriptions(id);


--
-- Name: webhook_logs webhook_logs_webhook_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.webhook_logs
    ADD CONSTRAINT webhook_logs_webhook_id_fkey FOREIGN KEY (webhook_id) REFERENCES public.webhook_registries(id);


--
-- Name: widget_configurations widget_configurations_widget_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.widget_configurations
    ADD CONSTRAINT widget_configurations_widget_id_fkey FOREIGN KEY (widget_id) REFERENCES public.dashboard_widgets(id);


--
-- Name: widget_data_queries widget_data_queries_widget_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.widget_data_queries
    ADD CONSTRAINT widget_data_queries_widget_id_fkey FOREIGN KEY (widget_id) REFERENCES public.dashboard_widgets(id);


--
-- PostgreSQL database dump complete
--

\unrestrict AY9XsZWxTwcWFJksnJr14dbjN3fFSHxiUHHkH6AT5cqKzbxMWQYgs6FjzMfoGzI

