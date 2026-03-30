"""Tests for scope enforcement."""

from hexstrike.sandbox.scope_enforcer import ScopeEnforcer


def test_domain_in_scope():
    enforcer = ScopeEnforcer({"domains": ["example.com"]})
    assert enforcer.is_in_scope("example.com")
    assert enforcer.is_in_scope("sub.example.com")
    assert not enforcer.is_in_scope("evil.com")


def test_ip_in_scope():
    enforcer = ScopeEnforcer({"ips": ["192.168.1.1"]})
    assert enforcer.is_in_scope("192.168.1.1")
    assert not enforcer.is_in_scope("10.0.0.1")


def test_cidr_in_scope():
    enforcer = ScopeEnforcer({"cidrs": ["10.0.0.0/24"]})
    assert enforcer.is_in_scope("10.0.0.50")
    assert not enforcer.is_in_scope("10.0.1.1")


def test_excluded_target():
    enforcer = ScopeEnforcer({
        "domains": ["example.com"],
        "excluded": ["admin.example.com"],
    })
    assert enforcer.is_in_scope("www.example.com")
    assert not enforcer.is_in_scope("admin.example.com")
