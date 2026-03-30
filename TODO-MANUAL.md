# TODO-MANUAL.md — Manual Setup Steps (Cannot Be Automated by Claude Code)

## Before Starting Development

### 1. GitHub Repository
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
- [ ] Set up VPS or provision cloud server
- [ ] Install Docker + Docker Compose on server
- [ ] Set up DNS records (A record → server IP)
- [ ] SSL certificate via Let's Encrypt / Cloudflare

### 4. Development Environment
- [ ] Install Python 3.12+, Node.js 20+, Docker Desktop
- [ ] Clone repo and run `docker compose -f docker-compose.dev.yml up -d`
- [ ] Copy .env.example to .env and fill in API keys

### 5. Legal & Compliance
- [ ] Terms of Service (users must own/authorize targets)
- [ ] Responsible disclosure policy
- [ ] Privacy policy (GDPR/Indian DPDPA compliant)

### 6. Payment Infrastructure (Phase 3+)
- [ ] Razorpay account (India payments)
- [ ] Stripe account (international payments)
