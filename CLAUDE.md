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
Multi-agent hierarchical system:
- Orchestrator Agent controls the overall pentest workflow via LangGraph state machine
- Specialized agents (Recon, Vuln, Exploit, Chain, Report) execute specific phases
- All security tools run inside Docker sandbox containers with network/fs isolation

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
