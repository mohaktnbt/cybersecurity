# CLAUDE-CODE-PLAN: AI Autonomous Penetration Testing Platform

## Project Codename: **HEXSTRIKE**

> Build a superior AI-powered autonomous penetration testing platform that surpasses Hex Security, XBOW, Pentera, Horizon3.ai, and all competitors in the space. Target: India-first pricing, global quality.

---

## TABLE OF CONTENTS

1. [CLAUDE.md — Project Configuration](#1-claudemd)
2. [AGENTS.md — Team & Agent Conventions](#2-agentsmd)
3. [TODO-MANUAL.md — Manual Setup Steps](#3-todo-manualmd)
4. [TIMELINE.md — Phased Build Roadmap](#4-timelinemd)
5. [Architecture Deep Dive](#5-architecture)
6. [Complete Build Plan — Phase by Phase](#6-build-plan)
7. [Competitive Differentiation Strategy](#7-differentiation)
8. [Open Source Tools Integration Map](#8-tools-map)

---

# 1. CLAUDE.md

```markdown
# CLAUDE.md — HexStrike AI Pentesting Platform

## Project Overview
HexStrike is an AI-native autonomous penetration testing platform that deploys
multi-agent AI systems to continuously probe web applications, APIs, cloud
infrastructure, and internal networks for vulnerabilities. Unlike competitors
that wrap basic scanners with GPT, HexStrike uses a hierarchical multi-agent
architecture with specialized agents for reconnaissance, vulnerability analysis,
exploitation, chaining, and reporting — delivering validated findings with
working proof-of-concept exploits and zero false positives.

## Business Context
- Market: $3.5-4.5B today, $8-14B by 2030 (20-30% CAGR)
- Key gap: No affordable continuous pentesting for SMBs (87% of critical
  findings occur in orgs with <200 employees)
- Differentiator: India-first pricing ($99-499/mo vs $5K-150K traditional),
  end-to-end remediation (find → validate → fix → verify), and business
  logic testing via proprietary reasoning chains

## Technology Stack
### Core Languages
- Backend API: Python 3.12+ (FastAPI + async)
- Agent Engine: Python 3.12+ (LangGraph for orchestration)
- Frontend Dashboard: Next.js 15 (TypeScript, App Router)
- CLI Tool: Python (Click/Typer)
- Infrastructure: Terraform + Kubernetes (Helm)

### AI/ML Layer
- Primary LLM: Claude API (claude-sonnet-4-20250514 for agents, claude-opus-4-20250115 for complex reasoning)
- Fallback LLM: OpenAI GPT-4o for cost-optimized simple tasks
- Local Models: Ollama (Llama 3.1 70B) for air-gapped deployments
- Agent Framework: LangGraph (state machines + tool calling)
- Embeddings: text-embedding-3-small for vulnerability knowledge base
- Vector DB: ChromaDB (dev) / Pinecone (prod)

### Data Layer
- Primary DB: PostgreSQL 16 (scan metadata, users, orgs, findings)
- Cache/Queue: Redis 7 (BullMQ job queues, session cache, rate limiting)
- Time-Series: TimescaleDB (scan metrics, performance tracking)
- Object Storage: S3-compatible (MinIO dev / S3 prod) for reports, screenshots, artifacts
- Knowledge Graph: Neo4j (attack paths, vulnerability chains, asset relationships)

### Security Tools (Docker-sandboxed)
- Network: Nmap, Masscan, Amass, Subfinder, httpx
- Web: Nuclei, OWASP ZAP, Nikto, ffuf, sqlmap, Burp Suite CE
- Exploitation: Metasploit Framework (controlled), custom exploit modules
- Credentials: Hydra, custom wordlists
- OSINT: theHarvester, Shodan API, Censys API

### Infrastructure
- Container Runtime: Docker (tool sandboxing) + Kubernetes (orchestration)
- CI/CD: GitHub Actions
- Monitoring: Prometheus + Grafana + OpenTelemetry
- Logging: Loki + Promtail
- Secrets: HashiCorp Vault (prod) / .env (dev)

## Architecture Pattern
Multi-agent hierarchical system following the PentestAgent/AWS Security Agent pattern:

```
┌─────────────────────────────────────────────────────┐
│                  ORCHESTRATOR AGENT                   │
│  (LangGraph State Machine — controls overall flow)   │
├──────────┬──────────┬──────────┬──────────┬─────────┤
│  RECON   │  VULN    │ EXPLOIT  │  CHAIN   │ REPORT  │
│  AGENT   │  AGENT   │  AGENT   │  AGENT   │  AGENT  │
│          │          │          │          │         │
│ Subdomain│ Nuclei   │ sqlmap   │ Multi-   │ CVSS    │
│ Port scan│ ZAP      │ Custom   │ step     │ MITRE   │
│ Service  │ Manual   │ Metasploi│ attack   │ OWASP   │
│ detect   │ checks   │ PoC gen  │ paths    │ PDF/HTML│
└──────────┴──────────┴──────────┴──────────┴─────────┘
        ↕               ↕               ↕
┌─────────────────────────────────────────────────────┐
│              TOOL EXECUTION SANDBOX                   │
│    (Docker containers with network/fs isolation)     │
└─────────────────────────────────────────────────────┘
```

## Development Principles
- INCREMENTAL BUILDS: Audit existing code before writing new code
- GAP ANALYSIS FIRST: Check what exists, identify gaps, then fill them
- DOCKER SANDBOX EVERYTHING: No security tool runs outside containers
- ZERO FALSE POSITIVES: Every finding must have a working PoC or evidence
- SAFE BY DEFAULT: Rate limiting, scope controls, human approval gates
- TEST COVERAGE: 80% minimum for agent logic, 90% for exploit validation

## Code Conventions
- Python: Ruff linter + Black formatter, type hints everywhere, async/await
- TypeScript: ESLint + Prettier, strict mode, no any
- Commits: Conventional Commits (feat:, fix:, refactor:, docs:, test:)
- Branch naming: feature/, fix/, refactor/ prefixes
- PR required: 1 approval minimum, CI must pass

## Key Commands
```bash
# Development
docker compose -f docker-compose.dev.yml up -d    # Start all services
cd apps/api && uvicorn main:app --reload           # API server
cd apps/web && npm run dev                          # Frontend
cd apps/agents && python -m hexstrike.cli scan      # Run a scan

# Testing
pytest apps/api/tests/ -v --cov                     # API tests
pytest apps/agents/tests/ -v --cov                  # Agent tests
npm run test --workspace=apps/web                    # Frontend tests

# Linting
ruff check apps/ --fix                              # Python lint
npm run lint --workspace=apps/web                    # TS lint
```

## Environment Variables
```
DATABASE_URL=postgresql://dev:dev@localhost:5432/hexstrike_dev
REDIS_URL=redis://localhost:6379
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
NEO4J_URI=bolt://localhost:7687
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
SHODAN_API_KEY=...
CENSYS_API_KEY=...
```
```

---

# 2. AGENTS.md

```markdown
# AGENTS.md — HexStrike Agent Architecture & Team Conventions

## Agent Hierarchy

### 1. Orchestrator Agent (orchestrator.py)
- ROLE: Master controller that manages the overall pentest workflow
- STATE MACHINE: Idle → Scoping → Recon → Analysis → Exploitation → Chaining → Reporting → Complete
- DECISIONS: Which agents to dispatch, priority ordering, resource allocation
- ANTI-HALLUCINATION: Validates every agent output against tool evidence
- MODEL: Claude Sonnet (fast reasoning, good tool use)

### 2. Reconnaissance Agent (recon_agent.py)
- ROLE: Asset discovery, subdomain enumeration, port scanning, service detection
- TOOLS: Nmap, Masscan, Amass, Subfinder, httpx, theHarvester, Shodan, Censys
- OUTPUT: Structured asset inventory (JSON) with services, versions, technologies
- SANDBOXING: Docker container with outbound-only network to target scope

### 3. Vulnerability Analysis Agent (vuln_agent.py)
- ROLE: Identify potential vulnerabilities from recon data + active scanning
- TOOLS: Nuclei (with custom templates), OWASP ZAP, Nikto, custom checks
- KNOWLEDGE: RAG over CVE database, exploit-db, vulnerability advisories
- OUTPUT: Ranked vulnerability candidates with confidence scores

### 4. Exploitation Agent (exploit_agent.py)
- ROLE: Validate vulnerabilities with working proof-of-concept exploits
- TOOLS: sqlmap, custom exploit scripts, Metasploit (controlled), Hydra
- SAFETY: Rate limiting, scope enforcement, rollback capability
- OUTPUT: Validated findings with PoC code, evidence screenshots, impact assessment
- HUMAN-IN-THE-LOOP: Requires approval for destructive/high-risk exploitation

### 5. Chain Analysis Agent (chain_agent.py)
- ROLE: Identify multi-step attack paths by chaining individual findings
- KNOWLEDGE: Neo4j attack graph, MITRE ATT&CK mapping
- OUTPUT: Attack chains with step-by-step paths, cumulative impact scores
- DIFFERENTIATION: This is where we beat competitors — business logic chaining

### 6. Remediation Agent (remediation_agent.py)
- ROLE: Generate specific fix recommendations with code patches
- KNOWLEDGE: RAG over remediation guides, framework-specific fixes
- OUTPUT: Code-level patches, configuration changes, prioritized fix plan
- VERIFICATION: Re-tests after remediation to confirm fixes

### 7. Report Agent (report_agent.py)
- ROLE: Generate executive and technical reports
- FRAMEWORKS: OWASP Top 10, MITRE ATT&CK, CVSS 4.0, PCI-DSS, NIST
- OUTPUT: PDF/HTML reports with executive summary, technical details, evidence
- TEMPLATES: Compliance-specific (SOC 2, ISO 27001, HIPAA, DORA, NIS2)

## Agent Communication Protocol
- Agents communicate via structured messages through the Orchestrator
- All tool outputs are stored in PostgreSQL with S3 references for large artifacts
- Neo4j stores the evolving attack graph as agents discover new paths
- Redis pub/sub for real-time progress updates to the dashboard

## ClawTeam Parallel Execution
- Recon agents can run in parallel across different target subdomains
- Vuln scanning parallelizes across discovered services
- Exploitation is sequential per target (safety) but parallel across targets
- Report generation runs after all other agents complete

## Session Continuity
- Every scan session has a UUID stored in PostgreSQL
- Agent state is checkpointed to Redis every 30 seconds
- Sessions can be paused/resumed across server restarts
- TIMELINE.md tracks progress across multi-day engagements
```

---

# 3. TODO-MANUAL.md

```markdown
# TODO-MANUAL.md — Manual Setup Steps (Cannot Be Automated by Claude Code)

## Before Starting Development

### 1. GitHub Repository
- [ ] Create repo: github.com/mohaktnbt/hexstrike (PRIVATE initially)
- [ ] Set up branch protection: main requires PR + 1 approval + CI pass
- [ ] Create GitHub Actions secrets: ANTHROPIC_API_KEY, OPENAI_API_KEY, DOCKER_HUB_TOKEN
- [ ] Enable Dependabot for security updates

### 2. API Keys & Accounts
- [ ] Anthropic API key (Claude): https://console.anthropic.com
- [ ] OpenAI API key (fallback): https://platform.openai.com
- [ ] Shodan API key: https://account.shodan.io
- [ ] Censys API key: https://search.censys.io/account/api
- [ ] (Optional) VirusTotal API key
- [ ] (Optional) SecurityTrails API key

### 3. Domain & Infrastructure
- [ ] Register domain (e.g., hexstrike.ai or hexstrike.in)
- [ ] Set up Hostinger VPS (168.231.103.49) or provision new server
- [ ] Install Docker + Docker Compose on VPS
- [ ] Set up DNS records (A record → VPS IP)
- [ ] SSL certificate via Let's Encrypt / Cloudflare

### 4. Development Environment
- [ ] Install Python 3.12+, Node.js 20+, Docker Desktop
- [ ] Install tmux for session persistence on VPS
- [ ] Clone repo and run `docker compose -f docker-compose.dev.yml up -d`
- [ ] Copy .env.example to .env and fill in API keys

### 5. Legal & Compliance
- [ ] Terms of Service (users must own/authorize targets)
- [ ] Responsible disclosure policy
- [ ] Bug bounty scope limitations
- [ ] Data processing agreement template
- [ ] Privacy policy (GDPR/Indian DPDPA compliant)

### 6. Payment Infrastructure (Phase 3+)
- [ ] Razorpay account (India payments)
- [ ] Stripe account (international payments)
- [ ] Pricing page: Free tier → Pro ($99/mo) → Business ($499/mo) → Enterprise (custom)
```

---

# 4. TIMELINE.md

```markdown
# TIMELINE.md — HexStrike Build Roadmap

## Phase 0: Foundation (Week 1-2)
### Session 1: Repository & Infrastructure Setup
- [x] RESEARCH: Complete competitive intelligence (Hex Security, XBOW, Pentera, Horizon3, etc.)
- [ ] Create GitHub repo with monorepo structure
- [ ] Set up Docker Compose for local dev (PostgreSQL, Redis, Neo4j, MinIO)
- [ ] Initialize Python backend (FastAPI + async)
- [ ] Initialize Next.js frontend
- [ ] Create CLAUDE.md, AGENTS.md, TODO-MANUAL.md
- [ ] Set up CI/CD with GitHub Actions

### Session 2: Database Schema & Core API
- [ ] Design PostgreSQL schema (users, orgs, targets, scans, findings, reports)
- [ ] Set up Prisma or SQLAlchemy migrations
- [ ] Implement auth (JWT + OAuth2 with Google/GitHub)
- [ ] Create core REST/GraphQL API endpoints
- [ ] Set up Redis for job queues (BullMQ pattern via Python)
- [ ] Create Neo4j schema for attack graphs

## Phase 1: Agent Engine Core (Week 3-5)
### Session 3: LangGraph Agent Framework
- [ ] Set up LangGraph with state machine for pentest workflow
- [ ] Implement Orchestrator Agent with phase transitions
- [ ] Create tool execution sandbox (Docker-in-Docker or Sysbox)
- [ ] Build tool wrapper interfaces (Nmap, Nuclei, httpx, etc.)
- [ ] Implement agent communication protocol
- [ ] Add checkpointing and session persistence

### Session 4: Reconnaissance Agent
- [ ] Subdomain enumeration (Amass, Subfinder integration)
- [ ] Port scanning (Nmap with intelligent flag generation)
- [ ] Service detection and version fingerprinting
- [ ] Technology stack detection (Wappalyzer-style)
- [ ] OSINT integration (Shodan, Censys, theHarvester)
- [ ] Asset inventory builder (structured JSON output)

### Session 5: Vulnerability Analysis Agent
- [ ] Nuclei integration with 10,000+ templates
- [ ] OWASP ZAP active scanning integration
- [ ] Custom vulnerability checks (auth bypass, IDOR, SSRF)
- [ ] RAG knowledge base over CVE/NVD database
- [ ] Vulnerability confidence scoring system
- [ ] False positive reduction through LLM reasoning

## Phase 2: Exploitation & Chaining (Week 6-8)
### Session 6: Exploitation Agent
- [ ] SQL injection validation (sqlmap integration)
- [ ] XSS validation with PoC generation
- [ ] Authentication bypass testing
- [ ] SSRF/CSRF validation
- [ ] Rate limiting and scope enforcement
- [ ] Evidence collection (screenshots, HTTP traces, PoC scripts)
- [ ] Human approval gates for high-risk exploits

### Session 7: Chain Analysis Agent
- [ ] Neo4j attack graph builder
- [ ] Multi-step attack path identification
- [ ] MITRE ATT&CK tactic/technique mapping
- [ ] Business logic vulnerability reasoning
- [ ] Impact score aggregation across chains
- [ ] Visual attack path generation (Mermaid/D3)

### Session 8: Remediation Agent
- [ ] Fix recommendation engine (framework-specific)
- [ ] Code patch generation for common vulns
- [ ] Configuration fix suggestions
- [ ] Priority scoring (CVSS + business context + exploitability)
- [ ] Re-verification after remediation
- [ ] Integration with GitHub (auto-create fix PRs)

## Phase 3: Dashboard & Reporting (Week 9-11)
### Session 9: Frontend Dashboard
- [ ] Next.js app with auth (NextAuth.js)
- [ ] Dashboard overview (active scans, finding stats, risk score)
- [ ] Target management (add, configure, schedule)
- [ ] Real-time scan progress (WebSocket/SSE)
- [ ] Finding detail views with evidence
- [ ] Attack path visualization (interactive graph)

### Session 10: Reporting Engine
- [ ] PDF report generation (executive + technical)
- [ ] HTML interactive report
- [ ] OWASP Top 10 compliance mapping
- [ ] MITRE ATT&CK heat map
- [ ] PCI-DSS / SOC 2 / HIPAA compliance views
- [ ] Trend analysis across scans
- [ ] Email/Slack notifications

### Session 11: Continuous Scanning
- [ ] Cron-based scheduled scans
- [ ] Webhook triggers (CI/CD integration)
- [ ] Diff analysis (new vs. known findings)
- [ ] Regression testing (verify previous fixes)
- [ ] Alert rules and escalation

## Phase 4: Production & Launch (Week 12-14)
### Session 12: Production Infrastructure
- [ ] Kubernetes deployment manifests (Helm charts)
- [ ] Terraform for cloud infrastructure
- [ ] Horizontal scaling for agent workers
- [ ] Monitoring (Prometheus + Grafana dashboards)
- [ ] Log aggregation (Loki)
- [ ] Backup and disaster recovery

### Session 13: Security Hardening
- [ ] Platform security audit (dogfooding!)
- [ ] Rate limiting and abuse prevention
- [ ] Multi-tenancy isolation
- [ ] Encryption at rest and in transit
- [ ] SOC 2 preparation
- [ ] Penetration test of own platform

### Session 14: Launch Preparation
- [ ] Landing page and marketing site
- [ ] Documentation (user guides, API docs)
- [ ] Pricing and payment integration (Razorpay + Stripe)
- [ ] Beta program with 10-20 pilot customers
- [ ] Product Hunt launch preparation
- [ ] Customer support infrastructure
```

---

# 5. Architecture Deep Dive

## 5.1 Repository Structure

```
hexstrike/
├── apps/
│   ├── api/                          # FastAPI backend
│   │   ├── src/
│   │   │   ├── main.py               # App entry point
│   │   │   ├── config.py             # Settings (Pydantic BaseSettings)
│   │   │   ├── auth/                 # JWT, OAuth2, RBAC
│   │   │   ├── models/               # SQLAlchemy/Prisma models
│   │   │   ├── schemas/              # Pydantic request/response schemas
│   │   │   ├── routers/              # API route handlers
│   │   │   │   ├── targets.py        # Target CRUD
│   │   │   │   ├── scans.py          # Scan management
│   │   │   │   ├── findings.py       # Finding queries
│   │   │   │   ├── reports.py        # Report generation
│   │   │   │   └── webhooks.py       # CI/CD webhooks
│   │   │   ├── services/             # Business logic
│   │   │   ├── workers/              # Background job processors
│   │   │   └── utils/                # Helpers
│   │   ├── tests/
│   │   ├── alembic/                  # DB migrations
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   │
│   ├── agents/                       # AI Agent Engine
│   │   ├── src/hexstrike/
│   │   │   ├── cli.py                # CLI entry point
│   │   │   ├── orchestrator.py       # Master orchestrator (LangGraph)
│   │   │   ├── agents/
│   │   │   │   ├── recon.py          # Reconnaissance agent
│   │   │   │   ├── vuln.py           # Vulnerability analysis agent
│   │   │   │   ├── exploit.py        # Exploitation agent
│   │   │   │   ├── chain.py          # Attack chain agent
│   │   │   │   ├── remediation.py    # Fix recommendation agent
│   │   │   │   └── report.py         # Report generation agent
│   │   │   ├── tools/
│   │   │   │   ├── base.py           # Tool interface base class
│   │   │   │   ├── nmap.py           # Nmap wrapper
│   │   │   │   ├── nuclei.py         # Nuclei wrapper
│   │   │   │   ├── zap.py            # OWASP ZAP wrapper
│   │   │   │   ├── sqlmap.py         # sqlmap wrapper
│   │   │   │   ├── ffuf.py           # ffuf directory brute-force
│   │   │   │   ├── httpx.py          # httpx probe wrapper
│   │   │   │   ├── amass.py          # Amass subdomain enum
│   │   │   │   ├── subfinder.py      # Subfinder wrapper
│   │   │   │   ├── hydra.py          # Hydra brute-force
│   │   │   │   └── shodan_api.py     # Shodan API client
│   │   │   ├── sandbox/
│   │   │   │   ├── docker_executor.py # Docker container execution
│   │   │   │   ├── scope_enforcer.py  # Target scope validation
│   │   │   │   └── rate_limiter.py    # Request rate control
│   │   │   ├── knowledge/
│   │   │   │   ├── cve_rag.py         # CVE knowledge base (RAG)
│   │   │   │   ├── exploit_db.py      # Exploit-DB integration
│   │   │   │   ├── mitre_attack.py    # MITRE ATT&CK mapping
│   │   │   │   └── owasp.py           # OWASP Top 10 mapping
│   │   │   ├── graph/
│   │   │   │   ├── attack_graph.py    # Neo4j attack graph builder
│   │   │   │   └── chain_finder.py    # Multi-step path discovery
│   │   │   └── reporting/
│   │   │       ├── pdf_generator.py   # PDF report builder
│   │   │       ├── html_generator.py  # HTML interactive report
│   │   │       └── templates/         # Jinja2 report templates
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   │
│   ├── web/                          # Next.js Frontend Dashboard
│   │   ├── src/
│   │   │   ├── app/                  # Next.js App Router
│   │   │   │   ├── (auth)/           # Auth pages (login, register)
│   │   │   │   ├── dashboard/        # Main dashboard
│   │   │   │   ├── targets/          # Target management
│   │   │   │   ├── scans/            # Scan views
│   │   │   │   ├── findings/         # Finding details
│   │   │   │   ├── reports/          # Report viewer
│   │   │   │   └── settings/         # Org/user settings
│   │   │   ├── components/           # React components
│   │   │   ├── hooks/                # Custom React hooks
│   │   │   ├── lib/                  # Utilities, API client
│   │   │   └── stores/               # Zustand state management
│   │   ├── Dockerfile
│   │   └── package.json
│   │
│   └── sandbox-images/               # Docker images for security tools
│       ├── nmap/Dockerfile
│       ├── nuclei/Dockerfile
│       ├── zap/Dockerfile
│       ├── sqlmap/Dockerfile
│       └── recon/Dockerfile           # Combined recon tools
│
├── packages/
│   ├── types/                        # Shared type definitions
│   ├── config/                       # Shared configs (ESLint, etc.)
│   └── sdk/                          # Python SDK for API consumers
│
├── infra/
│   ├── terraform/                    # AWS/cloud infrastructure
│   │   ├── modules/
│   │   │   ├── vpc/
│   │   │   ├── eks/
│   │   │   ├── rds/
│   │   │   ├── redis/
│   │   │   └── s3/
│   │   ├── environments/
│   │   │   ├── dev/
│   │   │   ├── staging/
│   │   │   └── production/
│   │   └── main.tf
│   ├── kubernetes/
│   │   ├── base/                     # Kustomize base
│   │   ├── overlays/                 # Environment overlays
│   │   └── helm/                     # Helm charts
│   └── docker-compose.dev.yml        # Local development
│
├── docs/
│   ├── architecture/                 # ADRs, system diagrams
│   ├── api/                          # API documentation
│   └── user-guides/                  # Product docs
│
├── scripts/
│   ├── seed_cve_db.py               # Populate CVE knowledge base
│   ├── build_nuclei_templates.py    # Custom Nuclei template builder
│   └── benchmark.py                  # Performance benchmarking
│
├── CLAUDE.md
├── AGENTS.md
├── TODO-MANUAL.md
├── TIMELINE.md
├── docker-compose.dev.yml
├── pyproject.toml                    # Root Python project
├── package.json                      # Root Node.js project (workspaces)
└── .github/
    └── workflows/
        ├── ci.yml                    # Lint + test + build
        ├── security.yml              # Dependency scanning
        └── deploy.yml                # Production deployment
```

## 5.2 Database Schema (PostgreSQL)

```sql
-- Core multi-tenant schema for HexStrike

-- Organizations (tenants)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    plan TEXT DEFAULT 'free' CHECK (plan IN ('free', 'pro', 'business', 'enterprise')),
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT,
    name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Org memberships
CREATE TABLE org_memberships (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    PRIMARY KEY (user_id, org_id)
);

-- Targets (assets to test)
CREATE TABLE targets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('web_app', 'api', 'network', 'cloud', 'mobile')),
    scope JSONB NOT NULL,  -- {domains: [], ips: [], cidrs: [], excluded: []}
    config JSONB DEFAULT '{}',  -- scan intensity, auth creds, etc.
    verified BOOLEAN DEFAULT FALSE,  -- ownership verification
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Scans (pentest sessions)
CREATE TABLE scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_id UUID REFERENCES targets(id) ON DELETE CASCADE,
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'pending' CHECK (status IN (
        'pending', 'scoping', 'recon', 'analyzing', 'exploiting',
        'chaining', 'reporting', 'completed', 'failed', 'cancelled'
    )),
    scan_type TEXT DEFAULT 'full' CHECK (scan_type IN ('full', 'quick', 'recon_only', 'custom')),
    config JSONB DEFAULT '{}',
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Findings (validated vulnerabilities)
CREATE TABLE findings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID REFERENCES scans(id) ON DELETE CASCADE,
    target_id UUID REFERENCES targets(id),
    org_id UUID REFERENCES organizations(id),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low', 'info')),
    cvss_score DECIMAL(3,1),
    cvss_vector TEXT,
    cwe_id TEXT,
    owasp_category TEXT,
    mitre_technique TEXT,
    affected_asset TEXT NOT NULL,  -- URL, IP:port, etc.
    evidence JSONB NOT NULL,  -- {request, response, screenshot_url, poc_script}
    remediation JSONB,  -- {description, code_patch, config_change, priority}
    status TEXT DEFAULT 'open' CHECK (status IN ('open', 'confirmed', 'fixed', 'accepted', 'false_positive')),
    is_chain_part BOOLEAN DEFAULT FALSE,
    chain_id UUID,  -- links to attack_chains
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Attack chains (multi-step paths)
CREATE TABLE attack_chains (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID REFERENCES scans(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    total_impact TEXT NOT NULL,  -- critical/high/medium/low
    steps JSONB NOT NULL,  -- ordered array of {finding_id, step_description, technique}
    mitre_tactics JSONB,  -- array of MITRE ATT&CK tactics used
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Scan events (real-time progress log)
CREATE TABLE scan_events (
    id BIGSERIAL PRIMARY KEY,
    scan_id UUID REFERENCES scans(id) ON DELETE CASCADE,
    agent TEXT NOT NULL,  -- which agent produced this
    event_type TEXT NOT NULL,  -- 'tool_start', 'tool_complete', 'finding', 'error', 'info'
    message TEXT NOT NULL,
    data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Reports (generated documents)
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID REFERENCES scans(id),
    org_id UUID REFERENCES organizations(id),
    type TEXT NOT NULL CHECK (type IN ('executive', 'technical', 'compliance', 'diff')),
    format TEXT NOT NULL CHECK (format IN ('pdf', 'html', 'json')),
    file_url TEXT NOT NULL,  -- S3 URL
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_findings_scan ON findings(scan_id);
CREATE INDEX idx_findings_severity ON findings(org_id, severity);
CREATE INDEX idx_scans_target ON scans(target_id);
CREATE INDEX idx_scans_status ON scans(org_id, status);
CREATE INDEX idx_scan_events_scan ON scan_events(scan_id, created_at);
```

## 5.3 Docker Compose (Development)

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: hexstrike_dev
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports: ["5432:5432"]
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    ports: ["6379:6379"]

  neo4j:
    image: neo4j:5-community
    environment:
      NEO4J_AUTH: neo4j/devpassword
    ports: ["7474:7474", "7687:7687"]
    volumes:
      - neo4jdata:/data

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports: ["9000:9000", "9001:9001"]
    volumes:
      - miniodata:/data

volumes:
  pgdata:
  neo4jdata:
  miniodata:
```

---

# 6. Complete Build Plan — Phase by Phase

## Phase 0: Foundation (Sessions 1-2)

### Step 0.1: Initialize Monorepo
```bash
mkdir hexstrike && cd hexstrike
git init
# Python root
touch pyproject.toml
# Node root (for Next.js frontend)
npm init -y
# Create directory structure per Section 5.1
```

### Step 0.2: FastAPI Backend Skeleton
```bash
cd apps/api
pip install fastapi uvicorn sqlalchemy alembic pydantic-settings redis
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

Core files to create:
- `apps/api/src/main.py` — FastAPI app with CORS, health check
- `apps/api/src/config.py` — Pydantic BaseSettings
- `apps/api/src/auth/jwt.py` — JWT token creation/verification
- `apps/api/src/auth/oauth2.py` — Google/GitHub OAuth2
- `apps/api/src/models/` — SQLAlchemy models matching schema above
- `apps/api/src/routers/` — Target, scan, finding, report CRUD

### Step 0.3: Next.js Frontend Skeleton
```bash
cd apps/web
npx create-next-app@latest . --typescript --tailwind --app --src-dir
npm install zustand @tanstack/react-query lucide-react
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu
```

### Step 0.4: Docker Compose + CI
- Create `docker-compose.dev.yml` (Section 5.3)
- Create `.github/workflows/ci.yml` with lint + test + build

## Phase 1: Agent Engine (Sessions 3-5)

### Step 1.1: LangGraph Orchestrator
```bash
pip install langgraph langchain-anthropic langchain-openai
```

Key implementation:
```python
# apps/agents/src/hexstrike/orchestrator.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class PentestState(TypedDict):
    target_scope: dict
    recon_results: dict
    vulnerabilities: list
    exploited_findings: list
    attack_chains: list
    report_url: str
    current_phase: str
    errors: list

def create_pentest_graph():
    graph = StateGraph(PentestState)
    graph.add_node("scope", scope_agent)
    graph.add_node("recon", recon_agent)
    graph.add_node("analyze", vuln_agent)
    graph.add_node("exploit", exploit_agent)
    graph.add_node("chain", chain_agent)
    graph.add_node("remediate", remediation_agent)
    graph.add_node("report", report_agent)

    graph.set_entry_point("scope")
    graph.add_edge("scope", "recon")
    graph.add_edge("recon", "analyze")
    graph.add_conditional_edges("analyze", should_exploit,
        {"exploit": "exploit", "report": "report"})
    graph.add_edge("exploit", "chain")
    graph.add_edge("chain", "remediate")
    graph.add_edge("remediate", "report")
    graph.add_edge("report", END)
    return graph.compile()
```

### Step 1.2: Docker Sandbox Executor
```python
# apps/agents/src/hexstrike/sandbox/docker_executor.py
import docker
import asyncio

class SandboxExecutor:
    """Execute security tools inside isolated Docker containers."""

    def __init__(self):
        self.client = docker.from_env()

    async def run_tool(self, image: str, command: str,
                       timeout: int = 300, network_mode: str = "bridge",
                       scope: dict = None) -> dict:
        """Run a security tool in a sandboxed container."""
        # Validate command against scope
        if scope:
            self._validate_scope(command, scope)

        container = self.client.containers.run(
            image=image,
            command=command,
            detach=True,
            network_mode=network_mode,
            mem_limit="512m",
            cpu_period=100000,
            cpu_quota=50000,  # 50% CPU
            read_only=True,
            security_opt=["no-new-privileges"],
            cap_drop=["ALL"],
        )

        try:
            result = container.wait(timeout=timeout)
            logs = container.logs().decode()
            return {"exit_code": result["StatusCode"], "output": logs}
        finally:
            container.remove(force=True)
```

### Step 1.3: Tool Wrappers
Each tool gets a wrapper that:
1. Constructs appropriate command flags based on LLM reasoning
2. Executes via SandboxExecutor
3. Parses output into structured data
4. Returns typed results to the agent

Example for Nmap:
```python
# apps/agents/src/hexstrike/tools/nmap.py
from .base import SecurityTool, ToolResult

class NmapTool(SecurityTool):
    name = "nmap"
    description = "Network port scanner and service detector"
    docker_image = "hexstrike/nmap:latest"

    async def execute(self, target: str, scan_type: str = "default",
                      ports: str = None) -> ToolResult:
        cmd = f"nmap -oX - {self._build_flags(scan_type, ports)} {target}"
        result = await self.sandbox.run_tool(self.docker_image, cmd)
        return self._parse_xml(result["output"])
```

## Phase 2: Exploitation & Chaining (Sessions 6-8)

### Step 2.1: Exploit Validation Pipeline
- For each vulnerability candidate from vuln_agent:
  1. LLM reasons about appropriate exploit technique
  2. Selects and configures tool (sqlmap for SQLi, custom for auth bypass, etc.)
  3. Executes in sandbox with strict scope enforcement
  4. Captures evidence (full HTTP request/response, screenshots via Playwright)
  5. LLM validates: is this a real finding or false positive?
  6. If validated: generate PoC script, calculate CVSS, assign CWE/OWASP

### Step 2.2: Neo4j Attack Graph
```cypher
// Node types
(:Asset {url, ip, port, service, version})
(:Vulnerability {id, title, severity, cvss})
(:Credential {type, username, access_level})
(:DataExposure {type, record_count, sensitivity})

// Relationship types
(:Asset)-[:HAS_VULN]->(:Vulnerability)
(:Vulnerability)-[:ENABLES]->(:Vulnerability)  // chaining
(:Vulnerability)-[:EXPOSES]->(:Credential)
(:Vulnerability)-[:EXPOSES]->(:DataExposure)
(:Credential)-[:GRANTS_ACCESS]->(:Asset)
```

### Step 2.3: Remediation Engine
- RAG over framework-specific fix databases (Django, Express, Spring, Rails, etc.)
- Code patch generation using Claude with context from the vulnerability
- Configuration fix templates (Nginx, Apache, AWS IAM, etc.)
- Re-scan verification after fixes applied

## Phase 3: Dashboard & Reports (Sessions 9-11)

### Step 3.1: Dashboard Pages
- `/dashboard` — Overview with risk score donut, active scans, recent findings
- `/targets` — CRUD for scan targets with scope configuration
- `/targets/[id]/scans` — Scan history with diff view
- `/scans/[id]` — Real-time scan progress with agent activity log
- `/scans/[id]/findings` — Finding list with filters (severity, status, type)
- `/findings/[id]` — Finding detail with evidence, PoC, remediation, timeline
- `/reports` — Generated reports with download/share
- `/settings` — Org, team, billing, API keys

### Step 3.2: Real-Time Scan Updates
- Server-Sent Events (SSE) from FastAPI to stream scan_events
- Zustand store for client-side scan state
- Agent activity visualization (which agent is running, what tool is executing)
- Finding cards that appear in real-time as agents discover vulnerabilities

### Step 3.3: Report Generation
- WeasyPrint for PDF generation from HTML/CSS templates
- Jinja2 templates for executive and technical reports
- Interactive HTML reports with collapsible sections and evidence viewers
- Compliance-specific report variants (PCI-DSS, SOC 2, DORA, NIS2)

---

# 7. Competitive Differentiation Strategy

## Where We Beat Every Competitor

| Gap in Market | Our Solution | Why Competitors Miss This |
|---|---|---|
| **No affordable continuous testing for SMBs** | $99/mo Pro tier with unlimited scans | Pentera charges $100K+/yr, XBOW targets enterprise |
| **Find-only, no fix** | End-to-end: Find → Validate → Fix → Verify | Most stop at finding; only Cogent does remediation |
| **Business logic blind spot** | LLM-powered reasoning chains for auth/logic flaws | Most rely on signature-based scanning |
| **India/APAC market ignored** | India-first pricing, Razorpay, INR billing, local support | All competitors are US/EU focused |
| **No attack chain visualization** | Interactive Neo4j-powered attack path explorer | Most show flat vulnerability lists |
| **Compliance report hell** | One-click DORA, NIS2, PCI-DSS, SOC 2 mapping | Manual mapping in most tools |
| **False positive fatigue** | Zero false positives via PoC validation for every finding | Scanners produce 30-70% false positives |

## Pricing Strategy (India-First, Global)

| Tier | Price (INR) | Price (USD) | Targets | Scans/mo | Features |
|---|---|---|---|---|---|
| Free | ₹0 | $0 | 1 | 1 | Quick scan, basic report |
| Pro | ₹8,299 | $99 | 5 | Unlimited | Full scans, remediation, PDF reports |
| Business | ₹41,499 | $499 | 25 | Unlimited | + API, CI/CD, team, compliance reports |
| Enterprise | Custom | Custom | Unlimited | Unlimited | + SSO, SLA, on-prem, custom agents |

---

# 8. Open Source Tools Integration Map

| Category | Tool | Docker Image | Agent User | Output Format |
|---|---|---|---|---|
| Subdomain enum | Amass | hexstrike/amass | Recon Agent | JSON |
| Subdomain enum | Subfinder | hexstrike/subfinder | Recon Agent | JSON |
| HTTP probing | httpx | hexstrike/httpx | Recon Agent | JSON |
| Port scanning | Nmap | hexstrike/nmap | Recon Agent | XML |
| Fast port scan | Masscan | hexstrike/masscan | Recon Agent | JSON |
| Vuln scanning | Nuclei | hexstrike/nuclei | Vuln Agent | JSON |
| Web scanning | OWASP ZAP | hexstrike/zap | Vuln Agent | JSON |
| Web scanning | Nikto | hexstrike/nikto | Vuln Agent | JSON |
| Dir brute-force | ffuf | hexstrike/ffuf | Vuln Agent | JSON |
| SQL injection | sqlmap | hexstrike/sqlmap | Exploit Agent | JSON |
| Credential test | Hydra | hexstrike/hydra | Exploit Agent | stdout |
| OSINT | theHarvester | hexstrike/harvester | Recon Agent | JSON |
| Screenshots | Playwright | hexstrike/playwright | Exploit Agent | PNG |
| OSINT API | Shodan | (API call) | Recon Agent | JSON |
| OSINT API | Censys | (API call) | Recon Agent | JSON |

---

## HOW TO USE THIS PLAN

1. **Create the GitHub repo** (see TODO-MANUAL.md)
2. **Copy CLAUDE.md into repo root** — this is Claude Code's project context
3. **Copy AGENTS.md into repo root** — agent architecture reference
4. **Copy TIMELINE.md into repo root** — session progress tracker
5. **Start Claude Code session**: `claude` in the repo directory
6. **Paste the current session's tasks** from TIMELINE.md
7. **Let Claude Code execute** — it reads CLAUDE.md for full context
8. **Update TIMELINE.md** after each session with progress

Each session should take 2-4 hours of Claude Code execution time. The full MVP is achievable in ~14 sessions (6-8 weeks of focused building).
