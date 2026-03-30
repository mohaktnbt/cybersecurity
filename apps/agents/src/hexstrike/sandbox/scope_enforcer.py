"""Scope Enforcer — Ensure all tool execution stays within authorized targets."""

import ipaddress
import re
from urllib.parse import urlparse


class ScopeEnforcer:
    """Validates that operations stay within the authorized target scope."""

    def __init__(self, scope: dict):
        self.allowed_domains: list[str] = scope.get("domains", [])
        self.allowed_ips: list[str] = scope.get("ips", [])
        self.allowed_cidrs: list[str] = scope.get("cidrs", [])
        self.excluded: list[str] = scope.get("excluded", [])

    def is_in_scope(self, target: str) -> bool:
        """Check if a target (URL, IP, or domain) is within scope."""
        if self._is_excluded(target):
            return False

        # Check as URL
        parsed = urlparse(target)
        hostname = parsed.hostname or target

        # Check domain match
        if self._matches_domain(hostname):
            return True

        # Check IP match
        try:
            ip = ipaddress.ip_address(hostname)
            if self._matches_ip(ip):
                return True
        except ValueError:
            pass

        return False

    def _is_excluded(self, target: str) -> bool:
        for excluded in self.excluded:
            if excluded in target:
                return True
        return False

    def _matches_domain(self, hostname: str) -> bool:
        for domain in self.allowed_domains:
            if hostname == domain or hostname.endswith(f".{domain}"):
                return True
        return False

    def _matches_ip(self, ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
        for allowed_ip in self.allowed_ips:
            if str(ip) == allowed_ip:
                return True
        for cidr in self.allowed_cidrs:
            if ip in ipaddress.ip_network(cidr, strict=False):
                return True
        return False

    def validate_command(self, command: str) -> bool:
        """Extract targets from a command and validate all are in scope."""
        # Extract IPs and domains from command
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'

        targets = re.findall(ip_pattern, command) + re.findall(domain_pattern, command)
        return all(self.is_in_scope(t) for t in targets)
