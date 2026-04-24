# Privacy Policy

This Privacy Policy describes how AgentCodex is intended to handle data when distributed as a Codex plugin or packaged runtime.

## Scope

AgentCodex installs and maintains a project-local scaffold inside a target repository. Its primary outputs are files written into that repository, including:

- `AGENTS.md`
- `.codex/`
- `.agentcodex/`

This policy covers the AgentCodex plugin, the packaged CLI, and the bundled runtime assets distributed with them.

## Data AgentCodex Processes

AgentCodex may process:

- repository file paths and directory structure
- repository-local configuration files
- prompts or instructions given by the user in Codex
- scaffold files written into the target repository

AgentCodex is designed to operate on repository-local files and explicit user requests.

## Data AgentCodex Does Not Intend to Collect

AgentCodex is not intended to operate as an analytics, advertising, or profile-building system. It is not designed to collect:

- marketing profiles
- ad identifiers
- unrelated personal browsing history
- unrelated device telemetry

## Storage Model

AgentCodex is designed around project-local state. Runtime artifacts are intended to be written into the target repository rather than hidden plugin state where possible.

Examples include:

- `.agentcodex/features/`
- `.agentcodex/reports/`
- `.agentcodex/archive/`
- `.agentcodex/history/`

If a Codex workspace, plugin host, package index, or CI platform stores logs, audit entries, or package metadata, that storage is governed by the operator of that platform in addition to this project policy.

## External Services

AgentCodex may be distributed through third-party services such as:

- Codex plugin or library surfaces
- package registries
- source code hosting platforms
- CI/CD systems

Those services may collect operational metadata such as download counts, access logs, authentication events, or upload records under their own terms and privacy policies.

## User Responsibility

Users and publishers are responsible for:

- reviewing repository contents before running scaffold installation or sync
- avoiding inclusion of secrets or regulated data in prompts when that is not appropriate
- configuring any organizational retention, access, and compliance controls required for their environment

## Security

AgentCodex is designed to favor:

- explicit file-based state
- reproducible validation commands
- deterministic routing
- project-local artifacts

Security fixes and operational controls are tracked in the repository documentation and reports.

## Changes

This policy may be updated as AgentCodex publication and hosting surfaces become more concrete. Material changes should be reflected in repository history and release notes.

## Contact

The publisher of AgentCodex should provide a public contact address before marketplace publication.
