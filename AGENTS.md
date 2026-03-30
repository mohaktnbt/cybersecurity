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

### 6. Remediation Agent (remediation_agent.py)
- ROLE: Generate specific fix recommendations with code patches
- KNOWLEDGE: RAG over remediation guides, framework-specific fixes
- OUTPUT: Code-level patches, configuration changes, prioritized fix plan
- VERIFICATION: Re-tests after remediation to confirm fixes

### 7. Report Agent (report_agent.py)
- ROLE: Generate executive and technical reports
- FRAMEWORKS: OWASP Top 10, MITRE ATT&CK, CVSS 4.0, PCI-DSS, NIST
- OUTPUT: PDF/HTML reports with executive summary, technical details, evidence

## Agent Communication Protocol
- Agents communicate via structured messages through the Orchestrator
- All tool outputs are stored in PostgreSQL with S3 references for large artifacts
- Neo4j stores the evolving attack graph as agents discover new paths
- Redis pub/sub for real-time progress updates to the dashboard

## Parallel Execution
- Recon agents can run in parallel across different target subdomains
- Vuln scanning parallelizes across discovered services
- Exploitation is sequential per target (safety) but parallel across targets
- Report generation runs after all other agents complete

## Session Continuity
- Every scan session has a UUID stored in PostgreSQL
- Agent state is checkpointed to Redis every 30 seconds
- Sessions can be paused/resumed across server restarts
