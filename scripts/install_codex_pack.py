#!/usr/bin/env python3
import argparse, copy, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
MAP={
 'CHANGELOG.md':'docs/codex/CHANGELOG.md',
 'core/AGENTS.template.md':'AGENTS.md','core/DESIGN.template.md':'DESIGN.md','core/CURRENT_STATE.template.md':'docs/CURRENT_STATE.md','core/PROJECT_PROFILE.template.yaml':'docs/codex/PROJECT_PROFILE.yaml','core/SKILL_MAP.template.md':'docs/codex/SKILL_MAP.md','core/SKILL_DIGEST.md':'docs/codex/SKILL_DIGEST.md','core/V3_UPGRADE_TEST_PLAN.md':'docs/codex/V3_UPGRADE_TEST_PLAN.md','core/WORKFLOW_CODEX.md':'docs/codex/WORKFLOW_CODEX.md','core/SR_BOOTSTRAP.md':'docs/codex/SR_BOOTSTRAP.md','core/SR_METHOD.md':'docs/codex/SR_METHOD.md','core/SR_DEVELOPMENT_METHOD.md':'docs/codex/SR_DEVELOPMENT_METHOD.md','core/SR_AGENT_METHOD.md':'docs/codex/SR_AGENT_METHOD.md','core/SR_HARNESS_METHOD.md':'docs/codex/SR_HARNESS_METHOD.md','core/LOT_EXECUTION_METHOD.md':'docs/codex/LOT_EXECUTION_METHOD.md','core/SR_PACK_VERSION.json':'docs/codex/SR_PACK_VERSION.json','core/AI_AGENT_RUNTIME_METHOD.md':'docs/codex/AI_AGENT_RUNTIME_METHOD.md','core/DOMAIN_EXPERTISE_BOOTSTRAP.md':'docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md','core/PROJECT_SKILLS_POLICY.md':'docs/codex/PROJECT_SKILLS_POLICY.md','core/TOKEN_OPTIMIZATION.md':'docs/codex/TOKEN_OPTIMIZATION.md','core/REPO_MAP_POLICY.md':'docs/codex/REPO_MAP_POLICY.md','core/CODEBASE_MAP.md':'docs/codex/CODEBASE_MAP.md','core/CODEBASE_MAP.generated.md':'docs/codex/CODEBASE_MAP.generated.md','blueprints/sr_lots.template.yaml':'docs/codex/SR_LOTS.yaml','blueprints/sr_passes.template.yaml':'docs/codex/SR_PASSES.yaml','blueprints/sr_inbox.template.yaml':'docs/codex/SR_INBOX.yaml','blueprints/nexus_context_pack.template.md':'docs/codex/NEXUS_CONTEXT_PACK.template.md','adr/ADR_TEMPLATE.md':'docs/adr/ADR_TEMPLATE.md'}
DIRS={'tasks/_TEMPLATE':'docs/codex/tasks/_TEMPLATE','prompts':'docs/codex/prompts','scripts/codex':'scripts/codex','project-skills':'docs/codex/project-skills','skills-method':'docs/codex/skills-method'}
PROJECT_OWNED={
    'AGENTS.md',
    'DESIGN.md',
    'docs/CURRENT_STATE.md',
    'docs/codex/PROJECT_PROFILE.yaml',
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
AGENTS_SR_BLOCK = """\

<!-- AURORA_SR_PACK_START -->
## SR Bootstrap obligatoire
- Au debut de chaque nouvelle conversation, apres compact, apres resume ou apres handoff, relire `docs/codex/SR_BOOTSTRAP.md` avant toute tache non triviale.
- Pour une tache non triviale, annoncer l'objectif verifiable, les hypotheses, l'approche simple suffisante, les skills selectionnees et la verification prevue avant de coder.
- Si le contexte precedent semble connu, verifier quand meme `docs/CURRENT_STATE.md` et la derniere memoire de tache pertinente.
- Au demarrage ou apres compact/resume, chercher le dernier `NEXT_SESSION_PROMPT.md` avec `python3 scripts/codex/find_next_session_prompt.py --root . --json` si disponible, puis le lire s'il existe.
- Validation humaine stricte : Codex peut analyser sans validation, mais ne modifie aucun fichier et ne lance aucune action de mutation tant que l'utilisateur n'a pas ecrit exactement `je valide`; cette validation ne couvre que le perimetre decrit juste avant.
- Annoncer systematiquement le statut de memoire sous la forme : `Memoire SR : existante / absente a creer / non creee car simple question`.
- Fact Gate obligatoire : avant toute conclusion factuelle non triviale, lire la source locale ou officielle qui peut trancher ; sinon marquer explicitement l'hypothese et la verification minimale restante.
- Evidence gate obligatoire avant recommandation : lire les fichiers verifiables quand ils peuvent trancher.
- Ne pas proposer une recommandation technique ou un plan engageant sans avoir lu les fichiers verifiables quand ils peuvent trancher.
- Declarer les skills utilisees dans `task_plan.md`; utiliser `aurora-lot-runner` pour roadmap, gros brief, plusieurs lots, reprise longue ou phase autonome bornee.
- Pour une UI/UX significative, utiliser `aurora-ui-visual-qa`, appliquer le Design Gate, le UI Test Readiness Gate et le UI Visual Evidence Gate, puis executer `node scripts/codex/sr_ui_verify.mjs` sur les routes et viewports requis.
- Utiliser `docs/codex/SKILL_DIGEST.md` comme routeur court pour choisir les skills, puis lire uniquement les `SKILL.md` selectionnes.
- Avant de creer ou modifier un agent IA applicatif, lire `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.
- SR Contract 3.1.0 : creer ou mettre a jour `docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json` quand `PROJECT_PROFILE.yaml` declare `require_sr_contract`, suivre chaque demande granulaire, separer implementation et preuve, heriter des exigences ouvertes, puis verifier avec `python3 scripts/codex/validate_sr_contract.py --file <chemin>`. Lire les contrats 3.0.0 en compatibilite.
- Reprise consolidee : un retour sur une exigence validee rouvre par defaut le lot d'origine ; ne creer un nouveau lot que pour un scope reellement nouveau avec justification explicite.
- Lot Completion Gate obligatoire : verifier chaque demande validee separement ; une implementation absente, partielle ou defectueuse impose `repair`, tandis que `user_testing` exige une implementation technique complete et seulement une preuve E2E ou acceptation manquante.
- Loop Contract obligatoire pour toute tache non triviale : creer ou mettre a jour `docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json`, declarer `conversation_transition` et `resume_protocol`, puis verifier avec `python3 scripts/codex/validate_loop_contract.py --file <chemin>`.
- Pour les skills metier Codex, lire `docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md` et `docs/codex/PROJECT_SKILLS_POLICY.md`.
- Pour les lots SR-Harness, lire `docs/codex/SR_HARNESS_METHOD.md`, `docs/codex/LOT_EXECUTION_METHOD.md`, `docs/codex/SR_LOTS.yaml` et `docs/codex/SR_INBOX.yaml`.
- Lot Design Evidence Gate : avant de creer ou promouvoir un lot en `planned`, `validated`, `in_progress`, `repair` ou `reopened`, remplir `design_evidence` avec fichiers candidats, fichiers reellement lus, hypotheses et questions; sans preuve suffisante, garder le lot en `proposed`.
- Pour une execution multi-lots, creer ou verifier une passe dans `docs/codex/SR_PASSES.yaml` avant codage : lots inclus, ordre, preflight, validations humaines, secrets/actions externes, criteres d'arret et E2E groupe.
- Backlog Mutation Gate : si une demande, une decouverte ou une reparation introduit une fonction structurante ou un impact durable, classer l'evenement, analyser les implications globales, puis mettre a jour `SR_INBOX.yaml` ou `SR_LOTS.yaml`, ou documenter pourquoi aucune mutation n'est requise.
- Global Impact Gate : avant de cadrer ou coder une fonction structurante, analyser son impact sur le produit global, les parcours, donnees, permissions, API/services, UI, tests, lots existants, dependances, migrations et risques, de facon agnostique au domaine.
- Lot Dependency Reconciliation : classer les lots existants pertinents comme `unaffected`, `impacted`, `blocked_by`, `reopened`, `superseded`, `split_required` ou `depends_on` avant codage significatif.
- Propagation Gate : si un changement touche un symbole ou contrat partage, annoncer avant mutation les consommateurs et surfaces a risque, demander validation humaine si le risque depasse le local, puis verifier apres mutation les references, appels, imports/exports, signatures, tests et smokes proportionnes avant toute cloture `done`.
- Knowledge gate : utiliser `RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs`; sans Nexus, `SR Core = RepoMap only`; avec Nexus, `SR Nexus = RepoMap + Nexus KG`.
- Politique multi-lots par defaut : traiter les lots `repair`/`reopened` puis `validated`, jusqu'a 3 lots si les gates restent verts; stopper sur gate rouge, validation humaine requise ou contexte a risque.
- Pass Planning Gate : avant toute passe, verifier que les dependances directes sont terminees ou incluses plus tot dans la passe; utiliser `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml` si disponible.
- Pass Runtime Goal : pour une passe `validated`/`in_progress`/`repair`/`reopened` executee avec `/goal`, generer `pass_runtime_goal.md` avec `python3 scripts/codex/build_pass_runtime_goal.py`, appliquer le Goal Length Gate (`max_goal_command_chars: 1000`, `hard_limit: 4000`) et ne pas enchainer une passe suivante sans validation utilisateur.
- Context budget gate : executer `python3 scripts/codex/context_budget_report.py --root .` si disponible avant nouveau lot long; creer `NEXT_SESSION_PROMPT.md` au statut orange/rouge, apres 2 lots ou 20 tours utilisateur; declarer si la prochaine action continue ici ou exige une nouvelle conversation.
- Self Evaluation Gate : apres patch, relire diff/fichiers critiques, verifier objectif, preuves, risques, oublis possibles, puis decider `done`, `user_testing`, `repair` ou `blocked`.
- En fin de tache non triviale, indiquer la memoire SR utilisee, les fichiers SR mis a jour, les gates, les tests E2E utilisateur a faire et le prochain lot recommande.
- Tests E2E utilisateur : les distinguer des tests unitaires et du build ; une implementation technique incomplete reste en `repair` meme si un E2E ou une acceptation manque aussi.
- Backlog Contract : apres modification de `SR_LOTS.yaml`, executer `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` avant cloture.
- En fin de tache non triviale, indiquer `NEXT_SESSION_PROMPT.md : cree / mis a jour / non requis` avec la raison, puis `Conversation : continuer ici / recommander nouvelle conversation / stopper pour nouvelle conversation`, et donner le prompt exact de reprise si une nouvelle conversation est recommandee.
- Cloture standard de lot : commencer par `Demande utilisateur | Etat | Preuve | Reste a faire`, puis resultat, verifications, memoire SR et prochaine etape. Ne jamais dire termine/complet/livre/implemente avec un Completion Gate rouge.
<!-- AURORA_SR_PACK_END -->
"""
SKILL_MAP_SR_BLOCK = """\

<!-- AURORA_SR_PACK_START -->
## SR Method required skills

Skills metier Codex et Skills runtime doivent etre declares ici ou dans `PROJECT_PROFILE.yaml`.

Consulter `docs/codex/SKILL_DIGEST.md` pour choisir les skills sans charger tous les `SKILL.md`.

- `aurora-planning-with-files`
- `aurora-diagnose`
- `aurora-review-diff`
- `aurora-ui-visual-qa`
- `aurora-architecture-check`
- `aurora-repomap-maintainer`
- `aurora-domain-skill-factory`
- `aurora-lot-runner`
- `aurora-terminal-token-optimizer`
- `aurora-tdd`
- `aurora-to-prd`

## Knowledge mode

- `core` : utiliser RepoMap puis lecture ciblee du code reel.
- `nexus_kg` : utiliser RepoMap + Nexus KG, puis lecture ciblee du code reel.

Les skills metier Codex restent locales au projet sauf decision explicite. Une skill projet non declaree dans ce fichier ou dans `PROJECT_PROFILE.yaml` est interdite par defaut.
<!-- AURORA_SR_PACK_END -->
"""
def backup_path(target, rel, stamp):
    return target/'docs/codex/upgrade_backups'/stamp/rel
def backup_existing(d,target,rel,stamp):
    if not d.exists(): return
    b=backup_path(target,rel,stamp); b.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(d,b)
def ensure_agents_sr_block(d,target,rel,stamp):
    if not d.exists(): return
    text=d.read_text(encoding='utf-8',errors='ignore')
    if '<!-- AURORA_SR_PACK_START -->' in text and '<!-- AURORA_SR_PACK_END -->' in text:
        start=text.index('<!-- AURORA_SR_PACK_START -->')
        end=text.index('<!-- AURORA_SR_PACK_END -->') + len('<!-- AURORA_SR_PACK_END -->')
        current=text[start:end]
        desired=AGENTS_SR_BLOCK.strip()
        if current.strip()==desired:
            return
        backup_existing(d,target,rel,stamp)
        d.write_text(text[:start].rstrip()+'\n\n'+desired+'\n'+text[end:].lstrip(),encoding='utf-8')
        print('updated SR block:',d)
        return
    backup_existing(d,target,rel,stamp)
    d.write_text(text.rstrip()+AGENTS_SR_BLOCK+'\n',encoding='utf-8')
    print('merged SR block:',d)
def ensure_markdown_sr_block(d,target,rel,stamp,block,label):
    if not d.exists(): return
    text=d.read_text(encoding='utf-8',errors='ignore')
    if '<!-- AURORA_SR_PACK_START -->' in text and '<!-- AURORA_SR_PACK_END -->' in text:
        start=text.index('<!-- AURORA_SR_PACK_START -->')
        end=text.index('<!-- AURORA_SR_PACK_END -->') + len('<!-- AURORA_SR_PACK_END -->')
        desired=block.strip()
        if text[start:end].strip()==desired:
            return
        backup_existing(d,target,rel,stamp)
        d.write_text(text[:start].rstrip()+'\n\n'+desired+'\n'+text[end:].lstrip(),encoding='utf-8')
        print(f'updated {label} block:',d)
        return
    backup_existing(d,target,rel,stamp)
    d.write_text(text.rstrip()+block+'\n',encoding='utf-8')
    print(f'merged {label} block:',d)
def deep_merge_missing(current, defaults):
    changed=False
    if not isinstance(current,dict) or not isinstance(defaults,dict):
        return current, False
    for key,value in defaults.items():
        if key not in current:
            current[key]=copy.deepcopy(value)
            changed=True
            continue
        if isinstance(current[key],dict) and isinstance(value,dict):
            current[key],nested=deep_merge_missing(current[key],value)
            changed=changed or nested
        elif isinstance(current[key],list) and isinstance(value,list):
            for item in value:
                if item not in current[key]:
                    current[key].append(copy.deepcopy(item))
                    changed=True
    return current, changed
def merge_project_profile(d,defaults_path,target,rel,stamp):
    if not d.exists() or not defaults_path.exists(): return
    try:
        import yaml  # type: ignore
    except Exception:
        print('WARNING: PyYAML unavailable, profile merge skipped:',d)
        return
    current=yaml.safe_load(d.read_text(encoding='utf-8')) or {}
    defaults=yaml.safe_load(defaults_path.read_text(encoding='utf-8')) or {}
    merged,changed=deep_merge_missing(current,defaults)
    if not changed: return
    backup_existing(d,target,rel,stamp)
    d.write_text(yaml.safe_dump(merged,sort_keys=False,allow_unicode=False),encoding='utf-8')
    print('merged project profile:',d)
def ensure_playwright_gitignore(target,stamp,upgrade=False):
    d=target/'.gitignore'
    entry='.playwright/.auth/'
    if d.exists():
        text=d.read_text(encoding='utf-8',errors='ignore')
        if entry in text:
            return
        if upgrade:
            backup_existing(d,target,'.gitignore',stamp)
        suffix='' if text.endswith('\n') or not text else '\n'
        d.write_text(text+suffix+'\n# Aurora SR UI auth state must never be committed\n'+entry+'\n',encoding='utf-8')
        print('updated gitignore:',d)
        return
    d.write_text('# Aurora SR UI auth state must never be committed\n'+entry+'\n',encoding='utf-8')
    print('created gitignore:',d)
def cp_file(s,d,write,upgrade=False,target=None,rel=None,stamp=None):
    d.parent.mkdir(parents=True,exist_ok=True)
    if upgrade and rel in PROJECT_OWNED and d.exists():
        if rel == 'AGENTS.md':
            ensure_agents_sr_block(d,target,rel,stamp)
        if rel == 'docs/codex/SKILL_MAP.md':
            ensure_markdown_sr_block(d,target,rel,stamp,SKILL_MAP_SR_BLOCK,'SR skill map')
        print('preserved project file:',d); return
    if d.exists() and upgrade:
        backup_existing(d,target,rel,stamp); shutil.copy2(s,d); print('upgraded:',d); return
    if d.exists() and not write: print('exists:',d); return
    shutil.copy2(s,d); print('copied:',d)
def cp_dir(s,d,write,upgrade=False,target=None,rel=None,stamp=None):
    if d.exists() and upgrade and rel == 'docs/codex/project-skills':
        for src in s.rglob('*'):
            if not src.is_file(): continue
            dst=d/src.relative_to(s)
            if dst.exists(): continue
            dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst); print('added project-skills file:',dst)
        print('preserved project-skills dir:',d); return
    if d.exists() and upgrade:
        b=backup_path(target,rel,stamp)
        if b.exists(): shutil.rmtree(b)
        b.parent.mkdir(parents=True,exist_ok=True); shutil.copytree(d,b)
        shutil.rmtree(d); shutil.copytree(s,d); print('upgraded dir:',d); return
    if d.exists() and not write: print('exists dir:',d); return
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(s,d); print('copied dir:',d)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',required=True); ap.add_argument('--target',default='.'); ap.add_argument('--profile',default='default')
    modes=ap.add_mutually_exclusive_group(); modes.add_argument('--write',action='store_true'); modes.add_argument('--upgrade',action='store_true'); a=ap.parse_args()
    source=Path(a.source).resolve(); target=Path(a.target).resolve()
    if not source.exists(): sys.exit('missing source')
    markers=existing_sr_markers(target)
    if a.write and not a.upgrade and markers:
        joined=', '.join(markers)
        sys.exit(
            'existing SR installation detected; use --upgrade after a per-project audit '
            f'instead of --write (markers: {joined})'
        )
    if not a.write and not a.upgrade:
        for src,rel in MAP.items(): print('would copy:',source/src,'->',target/rel)
        for src,rel in DIRS.items(): print('would copy dir:',source/src,'->',target/rel)
        print('dry run: no files written; use --write for a fresh install or --upgrade after audit')
        return
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    for s,d in MAP.items(): cp_file(source/s,target/d,a.write,a.upgrade,target,d,stamp)
    for s,d in DIRS.items(): cp_dir(source/s,target/d,a.write,a.upgrade,target,d,stamp)
    prof=source/'profiles'/a.profile/'PROJECT_PROFILE.yaml'
    if prof.exists() and not a.upgrade: cp_file(prof,target/'docs/codex/PROJECT_PROFILE.yaml',True)
    if prof.exists() and a.upgrade: merge_project_profile(target/'docs/codex/PROJECT_PROFILE.yaml',prof,target,'docs/codex/PROJECT_PROFILE.yaml',stamp)
    ensure_playwright_gitignore(target,stamp,a.upgrade)
    (target/'docs/domain').mkdir(parents=True,exist_ok=True); (target/'docs/adr').mkdir(parents=True,exist_ok=True)
    if a.upgrade: print('backup dir:',target/'docs/codex/upgrade_backups'/stamp)
    print('done')
if __name__=='__main__': main()
