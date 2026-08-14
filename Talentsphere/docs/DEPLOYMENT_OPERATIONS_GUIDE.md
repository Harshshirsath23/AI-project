# TalentSphere Sourcing Subgraph - Operations & Deployment Guide

**Document Type**: Operations & DevOps  
**Audience**: DevOps Engineers, System Administrators  
**Last Updated**: August 14, 2026  

---

## 1. Infrastructure Requirements

### Minimum System Specifications

```
┌─────────────────────────────────────────────────┐
│ Development Environment                         │
├─────────────────────────────────────────────────┤
│ CPU: 2+ cores (Intel/AMD x86_64)               │
│ RAM: 4 GB                                       │
│ Disk: 20 GB SSD                                │
│ Network: 1 Mbps+ internet                      │
│ OS: Ubuntu 20.04+ / macOS 12+ / Windows 11    │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Production Environment (Single Node)             │
├─────────────────────────────────────────────────┤
│ CPU: 4+ cores (Intel/AMD x86_64)               │
│ RAM: 8 GB minimum (16 GB recommended)          │
│ Disk: 100 GB SSD (faster I/O)                  │
│ Network: 10+ Mbps (1 Gbps recommended)         │
│ OS: Ubuntu 20.04 LTS or RHEL 8+                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Production Environment (HA Cluster)              │
├─────────────────────────────────────────────────┤
│ API Nodes (3): 4 cores, 8 GB RAM each         │
│ Database Node: 8+ cores, 32 GB RAM, fast SSD  │
│ Redis Node: 4 cores, 16 GB RAM                │
│ Load Balancer: Nginx or HAProxy                │
│ Total: 12+ cores, 72 GB RAM cluster            │
└─────────────────────────────────────────────────┘
```

### Required Software

```bash
# Core Services
✓ Python 3.11 or higher
✓ PostgreSQL 14+ (with pgvector extension)
✓ Redis 7.0+ (for caching & sessions)
✓ Nginx 1.20+ or HAProxy (reverse proxy)

# For AI/ML
✓ NVIDIA Nemotron 3 Ultra API access
✓ OpenAI API key (GPT-4 fallback)

# For Observability
✓ LangSmith account & API key
✓ Prometheus 2.30+ (metrics)
✓ Grafana 8.0+ (dashboards)
✓ ELK Stack (Elasticsearch 8.0+)

# For Development
✓ Git 2.30+
✓ Docker 20.10+ (containerization)
✓ Docker Compose 2.0+ (local orchestration)
✓ pytest 7.0+ (testing)
```

---

## 2. Setup Instructions

### 2.1 Local Development Setup

```bash
#!/bin/bash
# setup-dev.sh - Complete local development setup

# 1. Clone repository
git clone https://github.com/talentsphere/talentsphere.git
cd talentsphere

# 2. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 3. Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt

# 4. Copy environment template
cp backend/.env.example backend/.env

# 5. Update .env with your credentials
# REQUIRED:
# - DATABASE_URL=postgresql://user:password@localhost:5432/talentsphere
# - NEMOTRON_API_KEY=your-nvidia-key
# - OPENAI_API_KEY=your-openai-key
# - LANGSMITH_API_KEY=your-langsmith-key

# 6. Create database and run migrations
cd backend
alembic upgrade head

# 7. Seed initial data
python scripts/seed_organizations.py
python scripts/seed_iam.py

# 8. Start FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 9. Test API
curl http://localhost:8000/health
```

### 2.2 Docker Compose Setup (Local + Services)

```yaml
# docker-compose.yml
version: '3.9'

services:
  # PostgreSQL Database
  postgres:
    image: pgvector/pgvector:pg15-latest
    container_name: talentsphere-postgres
    environment:
      POSTGRES_USER: talentsphere
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-devpassword}
      POSTGRES_DB: talentsphere
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U talentsphere"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: talentsphere-redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # FastAPI Application
  app:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: talentsphere-app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://talentsphere:${POSTGRES_PASSWORD:-devpassword}@postgres:5432/talentsphere
      REDIS_URL: redis://redis:6379
      NEMOTRON_API_KEY: ${NEMOTRON_API_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      LANGSMITH_API_KEY: ${LANGSMITH_API_KEY}
      LANGSMITH_PROJECT: talentsphere-dev
      ENVIRONMENT: development
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Prometheus Metrics
  prometheus:
    image: prom/prometheus:latest
    container_name: talentsphere-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./docker/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  # Grafana Dashboards
  grafana:
    image: grafana/grafana:latest
    container_name: talentsphere-grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD:-admin}
      GF_INSTALL_PLUGINS: grafana-piechart-panel
    volumes:
      - ./docker/grafana/provisioning:/etc/grafana/provisioning
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

**Start Services:**
```bash
docker-compose up -d

# Wait for services to be ready
docker-compose logs -f app | grep "Uvicorn running"

# Test services
curl http://localhost:8000/health
```

### 2.3 Production Deployment (Kubernetes)

```bash
#!/bin/bash
# deploy-prod.sh - Production Kubernetes deployment

# 1. Create namespace
kubectl create namespace talentsphere-prod
kubectl config set-context --current --namespace=talentsphere-prod

# 2. Create secrets
kubectl create secret generic talentsphere-secrets \
  --from-literal=database-url="postgresql://user:pass@postgres:5432/talentsphere" \
  --from-literal=nemotron-api-key="$NEMOTRON_API_KEY" \
  --from-literal=openai-api-key="$OPENAI_API_KEY" \
  --from-literal=langsmith-api-key="$LANGSMITH_API_KEY"

# 3. Deploy PostgreSQL (via Helm or manifest)
helm install postgres bitnami/postgresql -f k8s/postgres-values.yaml

# 4. Deploy Redis (via Helm or manifest)
helm install redis bitnami/redis -f k8s/redis-values.yaml

# 5. Deploy FastAPI application
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml

# 6. Deploy ingress
kubectl apply -f k8s/ingress.yaml

# 7. Verify deployment
kubectl rollout status deployment/talentsphere-app
kubectl logs -f deployment/talentsphere-app

# 8. Check service endpoints
kubectl get svc talentsphere-app
kubectl get ingress
```

---

## 3. Configuration Management

### Environment Variables

```bash
# ==================== REQUIRED ====================

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/talentsphere
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40
DATABASE_POOL_RECYCLE=3600

# Redis
REDIS_URL=redis://localhost:6379
REDIS_DB=0

# API Keys
NEMOTRON_API_KEY=your-nvidia-nim-api-key
OPENAI_API_KEY=your-openai-api-key
LANGSMITH_API_KEY=your-langsmith-api-key

# LangSmith
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=talentsphere-production
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# ==================== OPTIONAL ====================

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security
JWT_SECRET_KEY=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=https://app.talentsphere.com

# Storage
S3_BUCKET=talentsphere-storage
S3_REGION=us-west-2
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key

# Observability
SENTRY_DSN=https://key@sentry.io/project-id
PROMETHEUS_PORT=9090
GRAFANA_URL=http://localhost:3000

# Performance
WORKER_PROCESSES=4
WORKER_TIMEOUT=300
REQUEST_TIMEOUT=120
CACHE_TTL=3600

# Feature Flags
ENABLE_HITL=true
ENABLE_JOB_BOARD_PUBLISHING=true
ENABLE_COMPLIANCE_AUDIT=true
ENABLE_LANGSM ITH_TRACING=true
```

### Configuration Files

```yaml
# config/production.yaml
server:
  host: 0.0.0.0
  port: 8000
  workers: 4
  timeout: 300

database:
  pool_size: 20
  max_overflow: 40
  pool_recycle: 3600
  echo: false

redis:
  url: redis://redis:6379
  db: 0
  decode_responses: true

langsmith:
  tracing: true
  project: talentsphere-production
  capture_inputs: true
  capture_outputs: true
  sample_rate: 1.0

observability:
  prometheus_port: 9090
  log_level: INFO
  sentry_dsn: ${SENTRY_DSN}

security:
  jwt_algorithm: HS256
  jwt_expiration_hours: 24
  password_min_length: 12
  require_tls: true
  cors_origins:
    - https://app.talentsphere.com
    - https://api.talentsphere.com
```

---

## 4. Database Migrations

### Schema Setup

```bash
# Initialize migrations (first time)
cd backend
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema with sourcing tables"

# Apply migrations
alembic upgrade head

# Check migration status
alembic current

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade ae1027a6acf
```

### Backup & Recovery

```bash
#!/bin/bash
# backup.sh - PostgreSQL backup

# Backup database
pg_dump -h localhost -U talentsphere talentsphere > backup-$(date +%Y%m%d).sql

# Backup with compression
pg_dump -h localhost -U talentsphere talentsphere | gzip > backup-$(date +%Y%m%d).sql.gz

# Restore from backup
psql -h localhost -U talentsphere talentsphere < backup-20260814.sql

# Restore from compressed backup
gunzip -c backup-20260814.sql.gz | psql -h localhost -U talentsphere talentsphere
```

---

## 5. Monitoring & Observability

### Prometheus Metrics

```yaml
# docker/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'talentsphere-api'
    static_configs:
      - targets: ['localhost:9090']
```

### Key Metrics to Monitor

```
# Application Metrics
talentsphere_workflow_executions_total
talentsphere_workflow_duration_seconds
talentsphere_agent_executions_total
talentsphere_hitl_approvals_pending

# API Metrics
http_requests_total
http_request_duration_seconds
http_requests_in_progress

# Database Metrics
postgresql_up
postgresql_connections_used
postgresql_connections_max

# AI/LLM Metrics
talentsphere_tokens_used_total
talentsphere_llm_latency_seconds
talentsphere_nemotron_calls_total
```

### Grafana Dashboards

Create dashboards for:
- Workflow Execution Overview
- Agent Performance Metrics
- API Latency & Throughput
- Error Rates & Debugging
- Resource Utilization (CPU, Memory, Disk)
- Database Performance

### Alerting Rules

```yaml
# alerts.yml
groups:
  - name: talentsphere_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        annotations:
          summary: "High error rate detected"

      - alert: WorkflowExecutionSlow
        expr: histogram_quantile(0.95, talentsphere_workflow_duration_seconds) > 30
        annotations:
          summary: "Workflow execution is slow"

      - alert: DatabaseConnectionPoolExhausted
        expr: postgresql_connections_used / postgresql_connections_max > 0.9
        annotations:
          summary: "Database connection pool nearly exhausted"
```

---

## 6. Log Management

### Structured Logging

```python
# Example structured log
logger.info("workflow_executed", extra={
    "organization_id": org_id,
    "execution_id": exec_id,
    "workflow_type": "sourcing",
    "status": "completed",
    "duration_ms": 12345,
    "job_id": job_id,
    "candidates_analyzed": 150,
    "candidates_shortlisted": 15
})
```

### Log Aggregation with ELK

```yaml
# docker-compose-logging.yml
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
  environment:
    - discovery.type=single-node
  ports:
    - "9200:9200"

logstash:
  image: docker.elastic.co/logstash/logstash:8.0.0
  volumes:
    - ./config/logstash.conf:/usr/share/logstash/pipeline/logstash.conf
  depends_on:
    - elasticsearch

kibana:
  image: docker.elastic.co/kibana/kibana:8.0.0
  ports:
    - "5601:5601"
  depends_on:
    - elasticsearch
```

---

## 7. Backup & Disaster Recovery

### Backup Strategy

```bash
# Daily backup (cron job)
0 2 * * * /opt/talentsphere/scripts/backup.sh

# Backup Script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/backups/talentsphere

# Database backup
pg_dump -h $DB_HOST -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/db_$DATE.sql.gz s3://talentsphere-backups/

# Clean old backups (keep 30 days)
find $BACKUP_DIR -type f -mtime +30 -delete
```

### Disaster Recovery Procedure

```
1. Assess Situation
   - Determine scope of data loss
   - Identify most recent clean backup
   - Estimate recovery time required

2. Recovery Steps
   a. Provision new infrastructure
   b. Restore database from backup
   c. Restore application code
   d. Verify data integrity
   e. Perform sanity checks
   f. Communicate status to stakeholders

3. Post-Recovery
   - Run full test suite
   - Monitor system closely
   - Document lessons learned
   - Update recovery procedures

Recovery Time Objective (RTO): < 4 hours
Recovery Point Objective (RPO): < 1 hour
```

---

## 8. Performance Tuning

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_ai_executions_org_status ON ai_executions(organization_id, status);
CREATE INDEX idx_candidates_org_skills ON candidates(organization_id) USING GIN(skills);
CREATE INDEX idx_jobs_org_created ON jobs(organization_id, created_at DESC);

-- Vector index for similarity search
CREATE INDEX idx_candidate_embeddings ON candidate_embeddings USING HNSW(embedding vector_cosine_ops);

-- Analyze query plans
EXPLAIN ANALYZE SELECT * FROM ai_executions WHERE organization_id = '...' AND status = 'COMPLETED';

-- Vacuum and analyze
VACUUM ANALYZE;
```

### Application Optimization

```python
# Connection pooling
DATABASE_POOL_SIZE = 20
DATABASE_MAX_OVERFLOW = 40

# Caching
CACHE_TTL = 3600  # 1 hour
CACHE_MAX_SIZE = 1000

# Async optimization
asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())  # Windows
```

### Load Balancing Configuration

```nginx
# Nginx reverse proxy
upstream talentsphere_backend {
    server app1:8000 weight=1;
    server app2:8000 weight=1;
    server app3:8000 weight=1;
    keepalive 32;
}

server {
    listen 80;
    server_name api.talentsphere.com;

    location / {
        proxy_pass http://talentsphere_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_buffering off;
        proxy_request_buffering off;
    }
}
```

---

## 9. Security Hardening

### SSL/TLS Configuration

```bash
# Generate self-signed certificate (development)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Use Let's Encrypt (production)
certbot certonly --standalone -d api.talentsphere.com
```

### Firewall Rules

```bash
# UFW (Ubuntu)
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp  # SSH
ufw allow 80/tcp  # HTTP
ufw allow 443/tcp # HTTPS
ufw allow 5432/tcp from DATABASE_HOST  # PostgreSQL
ufw allow 6379/tcp from REDIS_HOST     # Redis
ufw enable
```

### Secrets Management

```bash
# Use environment variables (development)
export DATABASE_URL=postgresql://...
export NEMOTRON_API_KEY=...

# Use HashiCorp Vault (production)
vault kv get secret/talentsphere/database-url
vault kv get secret/talentsphere/api-keys

# Use AWS Secrets Manager
aws secretsmanager get-secret-value --secret-id talentsphere/database-url
```

---

## 10. Incident Response

### Monitoring & Alerting

```bash
# Set up alerts for:
- High error rate (>1% for 5 minutes)
- Slow workflow execution (>30s for 95th percentile)
- Database connection pool exhausted (>90%)
- Memory usage >85%
- Disk usage >85%
- API downtime
```

### Escalation Procedure

```
Severity Level    Detection Time    Response Time    Escalation
─────────────────────────────────────────────────────────────
CRITICAL (P1)     Real-time         15 minutes       VP of Eng
HIGH (P2)         5 minutes         30 minutes       Tech Lead
MEDIUM (P3)       30 minutes        2 hours          Senior Eng
LOW (P4)          Next business day 24 hours         Team Lead
```

---

## 11. Maintenance Windows

### Regular Maintenance Tasks

```bash
# Daily
- Check error logs
- Monitor resource usage
- Verify backup completion

# Weekly
- Database maintenance (VACUUM ANALYZE)
- Log rotation
- Security patch review

# Monthly
- Database backup verification
- Disaster recovery drill
- Performance analysis
- Security audit

# Quarterly
- Infrastructure capacity review
- Dependency updates
- Major version upgrades
- Compliance audit
```

---

## 12. Support & Troubleshooting

### Common Issues

**Issue: Database Connection Pool Exhausted**
```
Symptom: "QueuePool limit exceeded"
Solution: Increase pool size in config or check for connection leaks
```

**Issue: High Memory Usage**
```
Symptom: App crashes or becomes unresponsive
Solution: Check for memory leaks, increase instance size, or restart
```

**Issue: Slow Workflow Execution**
```
Symptom: Workflows take >30s to complete
Solution: Check LLM latency, database performance, or add caching
```

### Support Contacts

- **Engineering Team**: engineering@talentsphere.com
- **On-Call**: ops@talentsphere.com
- **Security Issues**: security@talentsphere.com
- **GitHub Issues**: https://github.com/talentsphere/talentsphere/issues

---

## Appendix: Quick Reference Commands

```bash
# Health Checks
curl http://localhost:8000/health

# Database Checks
psql -U talentsphere -d talentsphere -c "SELECT version();"

# Application Logs
docker-compose logs -f app

# Database Migrations
alembic current
alembic upgrade head
alembic downgrade -1

# Backup & Restore
pg_dump talentsphere | gzip > backup.sql.gz
gunzip -c backup.sql.gz | psql talentsphere

# Performance Monitoring
kubectl top nodes
kubectl top pods

# Container Management
docker-compose up -d
docker-compose down
docker-compose restart app
```

---

**Document Version**: 1.0  
**Last Updated**: August 14, 2026  
**Next Review**: September 14, 2026
