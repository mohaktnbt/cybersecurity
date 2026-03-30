"""OWASP Top 10 mapping for vulnerability classification."""

OWASP_TOP_10_2021 = {
    "A01": "Broken Access Control",
    "A02": "Cryptographic Failures",
    "A03": "Injection",
    "A04": "Insecure Design",
    "A05": "Security Misconfiguration",
    "A06": "Vulnerable and Outdated Components",
    "A07": "Identification and Authentication Failures",
    "A08": "Software and Data Integrity Failures",
    "A09": "Security Logging and Monitoring Failures",
    "A10": "Server-Side Request Forgery",
}

# CWE to OWASP mapping
CWE_TO_OWASP = {
    "CWE-79": "A03",   # XSS → Injection
    "CWE-89": "A03",   # SQLi → Injection
    "CWE-78": "A03",   # OS Command Injection
    "CWE-22": "A01",   # Path Traversal → Broken Access Control
    "CWE-352": "A01",  # CSRF → Broken Access Control
    "CWE-918": "A10",  # SSRF
    "CWE-287": "A07",  # Improper Authentication
    "CWE-502": "A08",  # Deserialization
    "CWE-327": "A02",  # Broken Crypto
    "CWE-611": "A05",  # XXE → Misconfiguration
}


class OwaspMapper:
    """Map findings to OWASP Top 10 categories."""

    def map_by_cwe(self, cwe_id: str) -> str | None:
        """Map CWE to OWASP Top 10 category."""
        return CWE_TO_OWASP.get(cwe_id)

    def categorize_findings(self, findings: list[dict]) -> dict[str, list]:
        """Group findings by OWASP Top 10 category."""
        categories: dict[str, list] = {code: [] for code in OWASP_TOP_10_2021}
        for finding in findings:
            cwe = finding.get("cwe_id")
            if cwe and cwe in CWE_TO_OWASP:
                categories[CWE_TO_OWASP[cwe]].append(finding)
        return categories
