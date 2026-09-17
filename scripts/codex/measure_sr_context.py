#!/usr/bin/env python3
"""Reproducible document-load estimates, NOT measured model/API consumption."""
import argparse
import json
from pathlib import Path

BASE=['AGENTS.template.md','SR_BOOTSTRAP.md','PROJECT_PROFILE.template.yaml','CURRENT_STATE.template.md',
      'WORKFLOW_CODEX.md','SR_METHOD.md','SR_DEVELOPMENT_METHOD.md','SR_AGENT_METHOD.md',
      'SKILL_MAP.template.md','SKILL_DIGEST.md','CODEBASE_MAP.md','CODEBASE_MAP.generated.md']
START=['AGENTS.template.md','SR_BOOTSTRAP.md','PROJECT_PROFILE.template.yaml','SKILL_DIGEST.md',
       'procedures/fact.md','procedures/evidence.md']
MUTATION=['procedures/authority.md','procedures/memory.md','procedures/contracts.md']
CLOSE=['procedures/verification.md','procedures/completion.md','procedures/context.md']
SCENARIOS={
    'simple':(['AGENTS.template.md'],['AGENTS.template.md']),
    'small_change':(BASE,START+MUTATION+CLOSE),
    'business':(BASE+['DOMAIN_EXPERTISE_BOOTSTRAP.md'],START+MUTATION+CLOSE+['DOMAIN_EXPERTISE_BOOTSTRAP.md','procedures/skills.md']),
    'ui':(BASE+['SR_HARNESS_METHOD.md','LOT_EXECUTION_METHOD.md'],START+MUTATION+CLOSE+['procedures/ui.md','procedures/design-evidence.md','procedures/execution.md']),
    'resume':(['AGENTS.template.md','SR_BOOTSTRAP.md'],['AGENTS.template.md','SR_BOOTSTRAP.md','procedures/resume.md']),
    'agent':(BASE+['AI_AGENT_RUNTIME_METHOD.md','DOMAIN_EXPERTISE_BOOTSTRAP.md'],START+MUTATION+CLOSE+['AI_AGENT_RUNTIME_METHOD.md','DOMAIN_EXPERTISE_BOOTSTRAP.md','procedures/skills.md','procedures/propagation.md']),
    'lot':(BASE+['SR_HARNESS_METHOD.md','LOT_EXECUTION_METHOD.md'],START+MUTATION+CLOSE+['procedures/design-evidence.md','procedures/execution.md','procedures/impact.md']),
    'pass':(BASE+['SR_HARNESS_METHOD.md','LOT_EXECUTION_METHOD.md'],START+MUTATION+CLOSE+['procedures/design-evidence.md','procedures/execution.md','procedures/impact.md','procedures/passes.md','procedures/runtime-goal.md']),
    'initial_nontrivial':(BASE,START),
}

def measure(before,after):
    results=[]
    for name,(old,new) in SCENARIOS.items():
        old=list(dict.fromkeys(old));new=list(dict.fromkeys(new))
        a=sum(len((before/p).read_text()) for p in old);b=sum(len((after/p).read_text()) for p in new)
        results.append({'scenario':name,'before_characters':a,'after_characters':b,
                        'before_tokens_proxy':round(a/4),'after_tokens_proxy':round(b/4),
                        'reduction_percent':round(100*(a-b)/a,2),'before_documents':old,'after_documents':new})
    return {'measurement':'exact characters of specified document sets; tokens=characters/4 proxy',
            'limits':['No model execution or billing measurement','Project-specific files, selected skills, code, logs and active task contracts excluded on both sides','Routes cumulate with new findings; tables are declared scenarios, not automatic proof of equivalent behavior','Resume baseline uses narrow strict-resume rule, not the contradictory broad reload'],
            'scenarios':results}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--baseline',required=True);ap.add_argument('--root',default='.')
    a=ap.parse_args();print(json.dumps(measure(Path(a.baseline)/'core',Path(a.root)/'core'),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
