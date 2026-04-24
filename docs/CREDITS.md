# Credits

AgentCodex is a Codex-native adaptation built from two primary upstream influences:

- [AgentSpec](/home/user/Projetos/agentspec/README.md)
- [everything-claude-code (ECC)](/home/user/Projetos/everything-claude-code/README.md)

## Upstream Sources

### AgentSpec

- source path: `/home/user/Projetos/agentspec`
- public repository: `https://github.com/luanmorenommaciel/agentspec`
- license: MIT
- license file: `/home/user/Projetos/agentspec/LICENSE`
- contribution to AgentCodex:
  - workflow and SDD structure
  - data-engineering domain guidance
  - KB-first operating mindset
  - command and role source material

### everything-claude-code (ECC)

- source path: `/home/user/Projetos/everything-claude-code`
- public repository: `https://github.com/affaan-m/everything-claude-code`
- license: MIT
- license file: `/home/user/Projetos/everything-claude-code/LICENSE`
- contribution to AgentCodex:
  - Codex operating patterns
  - `.codex` runtime conventions
  - multi-agent role structure
  - skills, rules, and plugin-oriented runtime ideas

## Attribution Model

AgentCodex contains three classes of upstream usage:

1. imported reference material preserved under `.agentcodex/imports/`
2. Codex-native ports and adaptations of upstream concepts, commands, roles, and templates
3. original AgentCodex glue code, scaffolding, packaging, and project-standard work

Where practical, Codex-native ports are labeled in-file or in the surrounding documentation as ports or adaptations from AgentSpec or ECC.

## Imported Reference Layer

Raw imported upstream material is preserved under:

- `.agentcodex/imports/agentspec/`
- `.agentcodex/imports/ecc/`

This separation exists to keep upstream reference material auditable and distinct from AgentCodex-native rewrites.

## License Note

Both upstream repositories were verified locally as MIT-licensed:

- `/home/user/Projetos/agentspec/LICENSE`
- `/home/user/Projetos/everything-claude-code/LICENSE`

MIT permits reuse, modification, and redistribution, provided the copyright notice and permission notice are preserved in copies or substantial portions of the software.
