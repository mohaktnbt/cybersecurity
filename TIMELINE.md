# TIMELINE.md — HexStrike Build Roadmap

## Phase 0: Foundation (Week 1-2)
### Session 1: Repository & Infrastructure Setup
- [x] RESEARCH: Complete competitive intelligence
- [x] Create GitHub repo with monorepo structure
- [x] Set up Docker Compose for local dev (PostgreSQL, Redis, Neo4j, MinIO)
- [x] Initialize Python backend (FastAPI + async)
- [x] Initialize Next.js frontend
- [x] Create CLAUDE.md, AGENTS.md, TODO-MANUAL.md
- [x] Set up CI/CD with GitHub Actions

### Session 2: Database Schema & Core API
- [ ] Design PostgreSQL schema (users, orgs, targets, scans, findings, reports)
- [ ] Set up SQLAlchemy + Alembic migrations
- [ ] Implement auth (JWT + OAuth2 with Google/GitHub)
- [ ] Create core REST API endpoints
- [ ] Set up Redis for job queues
- [ ] Create Neo4j schema for attack graphs

## Phase 1: Agent Engine Core (Week 3-5)
### Session 3: LangGraph Agent Framework
- [ ] Set up LangGraph with state machine for pentest workflow
- [ ] Implement Orchestrator Agent with phase transitions
- [ ] Create tool execution sandbox (Docker-in-Docker)
- [ ] Build tool wrapper interfaces
- [ ] Implement agent communication protocol
- [ ] Add checkpointing and session persistence

### Session 4: Reconnaissance Agent
- [ ] Subdomain enumeration (Amass, Subfinder)
- [ ] Port scanning (Nmap)
- [ ] Service detection and version fingerprinting
- [ ] Technology stack detection
- [ ] OSINT integration (Shodan, Censys)
- [ ] Asset inventory builder

### Session 5: Vulnerability Analysis Agent
- [ ] Nuclei integration with templates
- [ ] OWASP ZAP active scanning
- [ ] Custom vulnerability checks
- [ ] RAG knowledge base over CVE/NVD
- [ ] Vulnerability confidence scoring
- [ ] False positive reduction via LLM reasoning

## Phase 2: Exploitation & Chaining (Week 6-8)
### Session 6: Exploitation Agent
- [ ] SQL injection validation (sqlmap)
- [ ] XSS validation with PoC generation
- [ ] Authentication bypass testing
- [ ] SSRF/CSRF validation
- [ ] Evidence collection
- [ ] Human approval gates

### Session 7: Chain Analysis Agent
- [ ] Neo4j attack graph builder
- [ ] Multi-step attack path identification
- [ ] MITRE ATT&CK mapping
- [ ] Business logic vulnerability reasoning
- [ ] Visual attack path generation

### Session 8: Remediation Agent
- [ ] Fix recommendation engine
- [ ] Code patch generation
- [ ] Priority scoring (CVSS + business context)
- [ ] Re-verification after remediation
- [ ] GitHub integration (auto-create fix PRs)

## Phase 3: Dashboard & Reporting (Week 9-11)
### Session 9-11: Frontend + Reports + Continuous Scanning

## Phase 4: Production & Launch (Week 12-14)
### Session 12-14: Infrastructure + Security + Launch
