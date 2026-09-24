#!/usr/bin/env python3
import argparse, sys
from pathlib import Path
MAP={
 'CHANGELOG.md':'docs/codex/CHANGELOG.md',
 'core/AGENTS.template.md':'AGENTS.md','core/SR_ROUTES.json':'docs/codex/SR_ROUTES.json','core/MCP_POLICY.template.yaml':'docs/codex/MCP_POLICY.yaml','core/DESIGN.template.md':'DESIGN.md','core/CURRENT_STATE.template.md':'docs/CURRENT_STATE.md','core/PROJECT_PROFILE.template.yaml':'docs/codex/PROJECT_PROFILE.yaml','core/SKILL_MAP.template.md':'docs/codex/SKILL_MAP.md','core/SKILL_DIGEST.md':'docs/codex/SKILL_DIGEST.md','core/UPGRADE_TEST_PLAN.md':'docs/codex/UPGRADE_TEST_PLAN.md','core/WORKFLOW_CODEX.md':'docs/codex/WORKFLOW_CODEX.md','core/SR_BOOTSTRAP.md':'docs/codex/SR_BOOTSTRAP.md','core/SR_METHOD.md':'docs/codex/SR_METHOD.md','core/SR_DEVELOPMENT_METHOD.md':'docs/codex/SR_DEVELOPMENT_METHOD.md','core/SR_AGENT_METHOD.md':'docs/codex/SR_AGENT_METHOD.md','core/SR_HARNESS_METHOD.md':'docs/codex/SR_HARNESS_METHOD.md','core/LOT_EXECUTION_METHOD.md':'docs/codex/LOT_EXECUTION_METHOD.md','core/SR_PACK_VERSION.json':'docs/codex/SR_PACK_VERSION.json','core/AI_AGENT_RUNTIME_METHOD.md':'docs/codex/AI_AGENT_RUNTIME_METHOD.md','core/DOMAIN_EXPERTISE_BOOTSTRAP.md':'docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md','core/PROJECT_SKILLS_POLICY.md':'docs/codex/PROJECT_SKILLS_POLICY.md','core/TOKEN_OPTIMIZATION.md':'docs/codex/TOKEN_OPTIMIZATION.md','core/REPO_MAP_POLICY.md':'docs/codex/REPO_MAP_POLICY.md','core/CODEBASE_MAP.md':'docs/codex/CODEBASE_MAP.md','core/CODEBASE_MAP.generated.md':'docs/codex/CODEBASE_MAP.generated.md','blueprints/sr_lots.template.yaml':'docs/codex/SR_LOTS.yaml','blueprints/sr_passes.template.yaml':'docs/codex/SR_PASSES.yaml','blueprints/sr_inbox.template.yaml':'docs/codex/SR_INBOX.yaml','blueprints/nexus_context_pack.template.md':'docs/codex/NEXUS_CONTEXT_PACK.template.md','adr/ADR_TEMPLATE.md':'docs/adr/ADR_TEMPLATE.md'}
DIRS={'core/procedures':'docs/codex/procedures','tasks/_TEMPLATE':'docs/codex/tasks/_TEMPLATE','prompts':'docs/codex/prompts','scripts/codex':'scripts/codex','project-skills':'docs/codex/project-skills','skills-method':'docs/codex/skills-method'}
PROJECT_OWNED={
    'AGENTS.md',
    'DESIGN.md',
    'docs/CURRENT_STATE.md',
    'docs/codex/PROJECT_PROFILE.yaml',
    'docs/codex/MCP_POLICY.yaml',
    'docs/codex/SKILL_MAP.md',
    'docs/codex/CODEBASE_MAP.md',
    'docs/codex/CODEBASE_MAP.generated.md',
    'docs/codex/SR_LOTS.yaml',
    'docs/codex/SR_PASSES.yaml',
    'docs/codex/SR_INBOX.yaml',
}
SR_INSTALL_MARKERS=(
    'docs/codex/SR_PACK_VERSION.json',
    'docs/codex/SR_METHOD.md',
    'docs/codex/SR_LOTS.yaml',
)

def existing_sr_markers(target):
    return [rel for rel in SR_INSTALL_MARKERS if (target/rel).exists()]
def agents_sr_block(source):
    """One canonical block for fresh installs and upgrades, from the source template."""
    text=(source/'core/AGENTS.template.md').read_text(encoding='utf-8')
    start='<!-- AURORA_SR_PACK_START -->'; end='<!-- AURORA_SR_PACK_END -->'
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError('AGENTS source template needs one managed block')
    a=text.index(start); b=text.index(end)+len(end)
    if b <= a: raise ValueError('reversed managed block')
    return text[a:b]

AGENTS_SR_BLOCK = agents_sr_block(Path(__file__).resolve().parents[1])
SKILL_MAP_SR_BLOCK = """\

<!-- AURORA_SR_PACK_START -->
## SR Method 4.1 skills

Skills metier Codex et Skills runtime doivent etre declares ici ou dans `PROJECT_PROFILE.yaml`.

Par defaut :

- `aurora-diagnose`
- `aurora-ui-visual-qa`
- `aurora-architecture-check`
- `aurora-lot-runner`

Facultatives :

- `aurora-domain-skill-factory`
- `aurora-to-prd`

Consulter `docs/codex/SKILL_DIGEST.md` seulement quand une de ces specialisations peut s'appliquer. Le planning, la compaction terminal, la revue finale et RepoMap sont des mecanismes du harness, pas des skills cognitives. SR 4.1 n'impose aucun TDD ni test rouge volontaire.

## Knowledge mode

- `core` : utiliser RepoMap puis lecture ciblee du code reel.
- `nexus_kg` : utiliser RepoMap + Nexus KG, puis lecture ciblee du code reel.

Les skills metier Codex restent locales au projet sauf decision explicite. Une skill projet non declaree dans ce fichier ou dans `PROJECT_PROFILE.yaml` est interdite par defaut.
<!-- AURORA_SR_PACK_END -->
"""
def main():
    import json
    from codex.sr_install_transaction import build_plan, apply_plan, restore
    ap=argparse.ArgumentParser(description="SR content-based installer: preview before mutation")
    ap.add_argument('--source', required=True); ap.add_argument('--target', default='.')
    ap.add_argument('--profile', default='default')
    modes=ap.add_mutually_exclusive_group()
    modes.add_argument('--write', action='store_true'); modes.add_argument('--upgrade', action='store_true')
    modes.add_argument('--apply-plan'); modes.add_argument('--restore')
    ap.add_argument('--plan-out', help='Explicitly save the reviewed plan (contains file contents)')
    ap.add_argument('--json', action='store_true')
    a=ap.parse_args(); source=Path(a.source).resolve(); target=Path(a.target).resolve()
    try:
        if a.restore:
            restore(target,Path(a.restore)); print('restored'); return
        if not source.is_dir(): ap.error('missing source')
        if a.write and existing_sr_markers(target):
            ap.error('existing SR installation detected; use --upgrade after audit')
        plan=json.loads(Path(a.apply_plan).read_text()) if a.apply_plan else build_plan(source,target,MAP,DIRS,PROJECT_OWNED,agents_sr_block(source),SKILL_MAP_SR_BLOCK,a.profile)
        if a.plan_out: Path(a.plan_out).write_text(json.dumps(plan,indent=2)+'\n')
        summary={k:v for k,v in plan.items() if k not in ('operations','guards')}
        summary['operations']=[{k:v for k,v in op.items() if k != 'content'} for op in plan['operations']]
        if a.json: print(json.dumps(summary,indent=2))
        else:
            print(f"plan: {len(plan['operations'])} changes; {len(plan['conflicts'])} conflicts; {len(plan['preserved'])} preserved")
            print("Use --json to inspect every planned path; --plan-out explicitly saves file contents.")
            for conflict in plan['conflicts']: print(f"CONFLICT {conflict['path']}: {conflict['reason']}")
        if a.write or a.upgrade or a.apply_plan:
            journal=apply_plan(plan,target)
            print(f'backup dir: {journal.parent}' if journal else 'unchanged: already converged')
            print('Files applied. Run sr_post_install_check.py before claiming installation verified.')
        else: print('dry run: no files written; use --write for a fresh install or --upgrade after audit')
        if plan['conflicts']: raise SystemExit(2)
    except (ValueError, OSError) as exc:
        ap.error(str(exc))

if __name__=='__main__': main()
