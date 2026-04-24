#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from kb_domains import KB_DOMAIN_PATHS, KB_MANAGED_DOMAINS, parse_simple_yaml_domains


ROOT = Path(__file__).resolve().parent.parent
IS_SOURCE_CHECKOUT = (ROOT / "pyproject.toml").exists()
ROUTING_PATH = ROOT / ".agentcodex" / "routing" / "routing.json"
KB_INDEX_PATH = ROOT / ".agentcodex" / "kb" / "index.yaml"
KB_ROOT = ROOT / ".agentcodex" / "kb"
ROLES_PATH = ROOT / ".agentcodex" / "roles" / "roles.yaml"
COMMANDS_DIR = ROOT / "docs" / "commands"
WORKFLOW_DIR = ROOT / "docs" / "workflow"
TEMPLATES_DIR = ROOT / ".agentcodex" / "templates"
COMMANDS_INDEX_PATH = ROOT / "docs" / "COMMANDS.md"
IMPORTS_MANIFEST_PATH = ROOT / ".agentcodex" / "imports" / "manifest.json"
MATURITY5_BASELINE_PATH = ROOT / ".agentcodex" / "maturity" / "maturity5-baseline.json"
HOOKS_PATH = ROOT / ".agentcodex" / "imports" / "agentspec" / "plugin_hooks" / "hooks.json"
PERSONAL_PATH_PATTERNS = [
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"C:\\Users\\[^\\\s]+", re.IGNORECASE),
]
ALLOWED_BUILTIN_ROLES = {"reviewer", "explorer", "domain-researcher"}
COMMAND_REQUIRED_SECTIONS = [
    "## Purpose",
    "## Primary Role",
    "## Inputs",
    "## Procedure",
    "## Outputs",
]
RE_TEXT_FILE = re.compile(r"\.(md|json|yaml|yml|toml|py)$", re.IGNORECASE)
WORKFLOW_PHASES = {"brainstorm", "define", "design", "build", "ship", "iterate"}
WORKFLOW_TEMPLATE_MAP = {
    "brainstorm": "BRAINSTORM_TEMPLATE.md",
    "define": "DEFINE_TEMPLATE.md",
    "design": "DESIGN_TEMPLATE.md",
    "build": "BUILD_REPORT_TEMPLATE.md",
    "ship": "SHIPPED_TEMPLATE.md",
}
PHASE_REFERENCE_RE = re.compile(r"`(brainstorm|define|design|build|ship|iterate)`")
ROLE_REFERENCE_RE = re.compile(r"`([a-z][a-z0-9-]+)`")
ARTIFACT_TEMPLATE_RE = re.compile(r"([A-Z_]+\{FEATURE\}(?:_\{DATE\})?\.md)")
HYGIENE_ROOTS = [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "docs",
    ROOT / "scripts",
    ROOT / ".agentcodex",
]
def parse_roles_yaml(path: Path) -> dict[str, dict]:
    roles: dict[str, dict] = {}
    current: dict | None = None
    current_id: str | None = None
    current_list_key: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("version:") or stripped == "roles:":
            continue
        if stripped.startswith("- id:"):
            current_id = stripped.split(":", 1)[1].strip()
            current = {"id": current_id, "kb_domains": [], "owns": [], "escalates_to": []}
            roles[current_id] = current
            current_list_key = None
            continue
        if current is None or current_id is None:
            continue
        if stripped.endswith(":") and stripped[:-1] in {"kb_domains", "owns", "escalates_to"}:
            current_list_key = stripped[:-1]
            continue
        if stripped.startswith("- ") and current_list_key:
            current[current_list_key].append(stripped[2:].strip())
            continue
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            normalized_key = key.strip()
            normalized_value = value.strip()
            if normalized_key in {"kb_domains", "owns", "escalates_to"} and normalized_value == "[]":
                current[normalized_key] = []
            else:
                current[normalized_key] = normalized_value
            current_list_key = None

    return roles


def collect_bullets(section_body: str) -> list[str]:
    values: list[str] = []
    for raw_line in section_body.splitlines():
        line = raw_line.strip()
        if line.startswith("- "):
            values.append(line[2:].strip().strip("`"))
    return values


def parse_section_bullets(text: str, heading: str) -> list[str]:
    pattern = rf"{re.escape(heading)}\n(.*?)(?:\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return []
    return collect_bullets(match.group(1))


def validate_command_docs(
    errors: list[str],
    domains: list[str],
    roles: dict[str, dict],
) -> list[str]:
    command_names: list[str] = []
    if not COMMANDS_DIR.exists():
        errors.append(f"Missing commands directory: {COMMANDS_DIR}")
        return command_names

    known_roles = set(roles) | ALLOWED_BUILTIN_ROLES
    for command_path in sorted(COMMANDS_DIR.glob("*.md")):
        command_names.append(command_path.name)
        text = command_path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"Command procedure is empty: {command_path}")
            continue

        for section in COMMAND_REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"Command procedure missing section {section}: {command_path}")

        primary_roles = parse_section_bullets(text, "## Primary Role")
        escalation_roles = parse_section_bullets(text, "## Escalation Roles")
        kb_domains = parse_section_bullets(text, "## KB Domains")

        if not primary_roles:
            errors.append(f"Command procedure missing primary role bullet: {command_path}")
        for role_id in primary_roles + escalation_roles:
            if role_id not in known_roles:
                errors.append(f"Command procedure references unknown role {role_id}: {command_path}")
        for kb_domain in kb_domains:
            if kb_domain not in domains:
                errors.append(f"Command procedure references unknown KB domain {kb_domain}: {command_path}")

    return command_names


def validate_commands_index(errors: list[str], command_names: list[str]) -> None:
    if not COMMANDS_INDEX_PATH.exists():
        errors.append(f"Missing commands index doc: {COMMANDS_INDEX_PATH}")
        return
    text = COMMANDS_INDEX_PATH.read_text(encoding="utf-8")
    indexed = sorted(set(re.findall(r"`docs/commands/([^`]+\.md)`", text)))
    expected = sorted(command_names)
    if indexed != expected:
        missing = sorted(set(expected) - set(indexed))
        extra = sorted(set(indexed) - set(expected))
        if missing:
            errors.append(f"Commands index missing entries: {', '.join(missing)}")
        if extra:
            errors.append(f"Commands index references non-existent procedures: {', '.join(extra)}")


def validate_workflow_docs(errors: list[str], roles: dict[str, dict]) -> None:
    if not WORKFLOW_DIR.exists():
        errors.append(f"Missing workflow docs directory: {WORKFLOW_DIR}")
        return

    known_roles = set(roles) | ALLOWED_BUILTIN_ROLES
    for phase in WORKFLOW_PHASES:
        path = WORKFLOW_DIR / f"{phase}.md"
        if not path.exists():
            errors.append(f"Missing workflow doc for phase {phase}: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"Workflow doc is empty: {path}")
            continue

        for referenced_phase in PHASE_REFERENCE_RE.findall(text):
            if referenced_phase not in WORKFLOW_PHASES:
                errors.append(f"Workflow doc references unknown phase {referenced_phase}: {path}")

        for role_id in ROLE_REFERENCE_RE.findall(text):
            if role_id in WORKFLOW_PHASES:
                continue
            if role_id.isupper():
                continue
            if role_id not in known_roles:
                errors.append(f"Workflow doc references unknown role {role_id}: {path}")

        for artifact_name in ARTIFACT_TEMPLATE_RE.findall(text):
            expected_template = artifact_name.replace("{FEATURE}", "TEMPLATE").replace("_{DATE}", "")
            if expected_template not in {
                "BRAINSTORM_TEMPLATE.md",
                "DEFINE_TEMPLATE.md",
                "DESIGN_TEMPLATE.md",
                "BUILD_REPORT_TEMPLATE.md",
                "SHIPPED_TEMPLATE.md",
            }:
                continue
            template_path = TEMPLATES_DIR / expected_template
            if not template_path.exists():
                errors.append(f"Workflow doc references missing template {expected_template}: {path}")

    for phase, template_name in WORKFLOW_TEMPLATE_MAP.items():
        template_path = TEMPLATES_DIR / template_name
        if not template_path.exists():
            errors.append(f"Missing workflow template for {phase}: {template_path}")


def validate_routing_to_workflows(errors: list[str]) -> None:
    if not ROUTING_PATH.exists():
        return
    routing = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))
    workflow_roles = {
        "workflow-brainstormer",
        "workflow-definer",
        "workflow-designer",
        "workflow-builder",
        "workflow-shipper",
        "workflow-iterator",
    }
    routed = {
        item["preferred_role"]
        for item in routing.get("workflow_phase_routing", [])
    }
    missing = sorted(workflow_roles - routed)
    if missing:
        errors.append(f"Workflow phase routing missing workflow roles: {', '.join(missing)}")


def validate_imports_manifest(errors: list[str]) -> None:
    if not IS_SOURCE_CHECKOUT and not IMPORTS_MANIFEST_PATH.exists():
        return
    if not IMPORTS_MANIFEST_PATH.exists():
        errors.append(f"Missing imports manifest: {IMPORTS_MANIFEST_PATH}")
        return

    try:
        manifest = json.loads(IMPORTS_MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid imports manifest JSON: {exc}")
        return

    imports = manifest.get("imports", [])
    if not imports:
        errors.append("Imports manifest does not declare any imported sources")
        return

    for source in imports:
        source_name = source.get("source", "<unknown>")
        target_root = Path(source.get("target_root", ""))
        if not target_root.exists():
            errors.append(f"Imported source target_root missing for {source_name}: {target_root}")
        for item in source.get("imports", []):
            destination = Path(item.get("destination", ""))
            status = item.get("status")
            if status != "copied":
                errors.append(
                    f"Import entry for {source_name}/{item.get('name', '<unknown>')} not copied: {status}"
                )
                continue
            if not destination.exists():
                errors.append(f"Imported destination missing for {source_name}: {destination}")


def validate_maturity5_baseline(errors: list[str]) -> None:
    if not MATURITY5_BASELINE_PATH.exists():
        errors.append(f"Missing maturity baseline manifest: {MATURITY5_BASELINE_PATH}")
        return
    try:
        baseline = json.loads(MATURITY5_BASELINE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid maturity baseline JSON: {exc}")
        return
    required_keys = {"version", "name", "scaffold_root", "default_profile", "profiles"}
    missing = sorted(required_keys - set(baseline))
    if missing:
        errors.append(f"Maturity baseline missing keys: {', '.join(missing)}")
        return
    if not baseline["profiles"]:
        errors.append("Maturity baseline does not declare any profiles")
        return
    profile_ids = {profile.get("id") for profile in baseline["profiles"]}
    if baseline["default_profile"] not in profile_ids:
        errors.append("Maturity baseline default_profile does not match any declared profile")
    for profile in baseline["profiles"]:
        if "id" not in profile:
            errors.append("Maturity baseline profile missing id")
            continue
        if not profile.get("dimensions"):
            errors.append(f"Maturity baseline profile has no dimensions: {profile['id']}")
            continue
        for dimension in profile["dimensions"]:
            if "id" not in dimension:
                errors.append(f"Maturity baseline profile {profile['id']} has a dimension without id")
                continue
            if not any(
                key in dimension
                for key in ("required_blocks", "required_control_checks", "required_feature_paths", "required_repo_paths")
            ):
                errors.append(f"Maturity baseline dimension has no evidence requirements: {profile['id']}/{dimension['id']}")


def validate_imported_hook_reference(errors: list[str]) -> None:
    if not IS_SOURCE_CHECKOUT and not HOOKS_PATH.exists():
        return
    if not HOOKS_PATH.exists():
        errors.append(f"Missing imported AgentSpec hooks file: {HOOKS_PATH}")
        return

    try:
        hooks_data = json.loads(HOOKS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid AgentSpec hooks JSON: {exc}")
        return

    session_hooks = hooks_data.get("hooks", {}).get("SessionStart", [])
    if not session_hooks:
        errors.append("Imported AgentSpec hooks do not declare SessionStart entries")


def validate_text_hygiene(errors: list[str]) -> None:
    for root_path in HYGIENE_ROOTS:
        if not root_path.exists():
            continue
        candidate_paths = [root_path] if root_path.is_file() else root_path.rglob("*")
        for path in candidate_paths:
            if not path.is_file():
                continue
            if any(part in {".git", "__pycache__", ".venv", ".venv-packaging"} for part in path.parts):
                continue
            if path == ROOT / "scripts" / "validate_agentcodex.py":
                continue
            if ".agentcodex" in path.parts and "imports" in path.parts:
                continue
            if not RE_TEXT_FILE.search(path.name):
                continue
            text = path.read_text(encoding="utf-8")
            if "\u200b" in text or "\ufeff" in text:
                errors.append(f"Text hygiene issue in {path}: contains zero-width or BOM characters")
            for pattern in PERSONAL_PATH_PATTERNS:
                if pattern.search(text):
                    errors.append(f"Text hygiene issue in {path}: contains personal absolute path")
                    break


def main() -> int:
    errors: list[str] = []

    if not ROUTING_PATH.exists():
        errors.append(f"Missing routing manifest: {ROUTING_PATH}")
    else:
        try:
            routing = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid routing.json: {exc}")
            routing = None
        if routing:
            for key in [
                "workflow_phase_routing",
                "data_engineering_routing",
                "domain_routing",
                "platform_routing",
                "control_routing",
                "file_pattern_hints",
                "escalations",
            ]:
                if key not in routing:
                    errors.append(f"routing.json missing key: {key}")

    if not KB_INDEX_PATH.exists():
        errors.append(f"Missing KB index: {KB_INDEX_PATH}")
        domains = []
    else:
        domains = parse_simple_yaml_domains(KB_INDEX_PATH)
        if not domains:
            errors.append("KB index does not declare any domains")
        if sorted(domains) != sorted(KB_MANAGED_DOMAINS):
            errors.append(
                "KB index domains do not match managed scaffold domains: "
                f"index={domains} managed={KB_MANAGED_DOMAINS}"
            )

    for domain in domains:
        domain_dir = KB_ROOT / KB_DOMAIN_PATHS[domain]
        index_md = domain_dir / "index.md"
        index_md_alt = domain_dir / "INDEX.md"
        quick_ref = domain_dir / "quick-reference.md"
        if not domain_dir.exists():
            errors.append(f"KB domain directory missing: {domain_dir}")
            continue
        if not index_md.exists() and not index_md_alt.exists():
            errors.append(f"KB domain missing index.md: {index_md}")
        if domain not in {
            "governance",
            "lineage",
            "observability",
            "access-control",
            "data-contracts",
            "azure",
            "databricks",
            "snowflake",
            "mcp",
            "rag",
        } and not quick_ref.exists():
            errors.append(f"KB domain missing quick-reference.md: {quick_ref}")

    if not ROLES_PATH.exists():
        errors.append(f"Missing roles manifest: {ROLES_PATH}")
        roles = {}
    else:
        roles = parse_roles_yaml(ROLES_PATH)
        if not roles:
            errors.append("Roles manifest does not declare any roles")

    for role_id, role in roles.items():
        doc_path = ROOT / role.get("doc", "")
        if not doc_path.exists():
            errors.append(f"Role doc missing for {role_id}: {doc_path}")
        for kb_domain in role.get("kb_domains", []):
            if kb_domain not in domains:
                errors.append(f"Role {role_id} references unknown KB domain: {kb_domain}")
            if kb_domain not in KB_MANAGED_DOMAINS:
                errors.append(f"Role {role_id} references unmanaged KB domain: {kb_domain}")

    command_names = validate_command_docs(errors, domains, roles)
    validate_commands_index(errors, command_names)
    validate_workflow_docs(errors, roles)

    if ROUTING_PATH.exists() and roles:
        routing = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))
        routed_roles = set()
        for section in [
            "workflow_phase_routing",
            "data_engineering_routing",
            "domain_routing",
            "platform_routing",
            "control_routing",
            "file_pattern_hints",
        ]:
            for item in routing.get(section, []):
                routed_roles.add(item["preferred_role"])
                for key in ("explore_first_with", "review_with", "research_with"):
                    if key in item:
                        routed_roles.add(item[key])
        for item in routing.get("escalations", []):
            routed_roles.add(item["from"])
            routed_roles.add(item["to"])
        for role_id in sorted(routed_roles):
            if role_id not in roles and role_id not in {"domain-researcher", "reviewer", "explorer"}:
                errors.append(f"Routing references unknown role: {role_id}")
    validate_routing_to_workflows(errors)

    validate_imports_manifest(errors)
    validate_maturity5_baseline(errors)
    validate_imported_hook_reference(errors)
    validate_text_hygiene(errors)

    if errors:
        print("AgentCodex validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("AgentCodex validation passed.")
    print(f"Validated routing manifest: {ROUTING_PATH}")
    print(f"Validated KB domains: {', '.join(domains)}")
    print(f"Validated roles manifest: {ROLES_PATH}")
    print(f"Validated command procedures: {', '.join(command_names)}")
    if IMPORTS_MANIFEST_PATH.exists():
        print(f"Validated imports manifest: {IMPORTS_MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
