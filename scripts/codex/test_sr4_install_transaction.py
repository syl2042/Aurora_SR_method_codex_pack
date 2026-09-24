import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
import sr_install_transaction as tx

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('installer',ROOT/'scripts/install_codex_pack.py')
installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)

def plan(target):
    return tx.build_plan(ROOT,target,installer.MAP,installer.DIRS,installer.PROJECT_OWNED,installer.AGENTS_SR_BLOCK,installer.SKILL_MAP_SR_BLOCK)

class TransactionTests(unittest.TestCase):
    def test_fresh_and_repeated_upgrade_converge(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp);p=plan(target);self.assertFalse(p['conflicts']);self.assertEqual(list(target.iterdir()),[])
            with self.assertRaises(ValueError):
                tx.build_plan(ROOT,target,installer.MAP,installer.DIRS,installer.PROJECT_OWNED,installer.AGENTS_SR_BLOCK,installer.SKILL_MAP_SR_BLOCK,profile='../escape')
            tx.apply_plan(p,target)
            self.assertEqual(plan(target)['operations'],[])
            self.assertEqual((target/'scripts/codex/sr_ui_verify.mjs').stat().st_mode & 0o777, (ROOT/'scripts/codex/sr_ui_verify.mjs').stat().st_mode & 0o777)

    def test_unknown_custom_script_blocks_without_mutating(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp);path=target/'scripts/codex/context_budget_report.py';path.parent.mkdir(parents=True);path.write_text('# custom\n')
            p=plan(target);self.assertTrue(p['conflicts'])
            with self.assertRaises(ValueError):tx.apply_plan(p,target)
            self.assertEqual(path.read_text(),'# custom\n');self.assertFalse((target/'AGENTS.md').exists())

    def test_user_rules_and_open_tasks_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp);(target/'AGENTS.md').write_text('LOCAL_RULE: no external writes\n')
            task=target/'docs/codex/tasks/open/sr_contract.json';task.parent.mkdir(parents=True);task.write_text('{"open":["REQ-1"]}')
            tx.apply_plan(plan(target),target)
            self.assertIn('LOCAL_RULE',(target/'AGENTS.md').read_text());self.assertEqual(task.read_text(),'{"open":["REQ-1"]}')

    def test_stale_plan_checks_unchanged_files_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp);tx.apply_plan(plan(target),target);p=plan(target)
            (target/'AGENTS.md').write_text('new user edit')
            with self.assertRaisesRegex(ValueError,'stale'):tx.apply_plan(p,target)

    def test_restore_and_later_edit_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp);(target/'AGENTS.md').write_text('local')
            journal=tx.apply_plan(plan(target),target)
            (target/'AGENTS.md').write_text('later edit')
            with self.assertRaisesRegex(ValueError,'post-install'):tx.restore(target,journal)
            data=json.loads(journal.read_text());entry=next(e for e in data['entries'] if e['path']=='AGENTS.md')
            # Restore the applied bytes from another deterministic source, then restore backup.
            (target/'AGENTS.md').write_text('local\n\n'+installer.AGENTS_SR_BLOCK.strip()+'\n')
            tx.restore(target,journal);self.assertEqual((target/'AGENTS.md').read_text(),'local')
            self.assertFalse((target/'docs/codex/SR_BOOTSTRAP.md').exists())

    def test_symlink_cannot_escape_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'repo';target.mkdir();outside=Path(tmp)/'outside';outside.mkdir();(target/'docs').symlink_to(outside)
            with self.assertRaisesRegex(ValueError,'symlink'):plan(target)

    def test_version_number_does_not_select_algorithm(self):
        for version in ['unknown','0.0.1','99.0.0']:
            with self.subTest(version=version),tempfile.TemporaryDirectory() as tmp:
                target=Path(tmp);p=target/'docs/codex/SR_PACK_VERSION.json';p.parent.mkdir(parents=True);p.write_text(json.dumps({'version':version}))
                self.assertFalse(plan(target)['conflicts'])

    def test_obsolete_managed_file_is_removed_but_custom_one_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp);tx.apply_plan(plan(target),target)
            obsolete=target/'docs/codex/skills-method/aurora-tdd/SKILL.md';obsolete.parent.mkdir(parents=True)
            known=json.loads((ROOT/'core/SR_MANAGED_HASHES.json').read_text())
            old_hash=known['docs/codex/skills-method/aurora-tdd/SKILL.md'][0]
            # Use a known historical byte payload from the repository baseline when available.
            baseline=ROOT/'tasks/2026-09-17_sr4-context/baseline/skills-method/aurora-tdd/SKILL.md'
            if baseline.exists() and tx.digest(baseline.read_bytes()) == old_hash:
                obsolete.write_bytes(baseline.read_bytes())
                p=plan(target);self.assertEqual(p['classifications'][str(obsolete.relative_to(target))],'obsolete_exact')
                tx.apply_plan(p,target);self.assertFalse(obsolete.exists())
            obsolete.parent.mkdir(parents=True,exist_ok=True);obsolete.write_text('local custom TDD notes\n')
            p=plan(target);self.assertEqual(p['classifications'][str(obsolete.relative_to(target))],'obsolete_modified_preserved')
            self.assertTrue(any(item['path']==str(obsolete.relative_to(target)) for item in p['preserved']))

    def test_profile_capabilities_converge_without_losing_local_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp);profile=target/'docs/codex/PROJECT_PROFILE.yaml';profile.parent.mkdir(parents=True)
            profile.write_text('project:\n  local_key: keep\nskills:\n  method:\n    - aurora-tdd\ncontext_budget:\n  cached_input_weight_percent: 10\n')
            p=plan(target);self.assertFalse(p['conflicts']);tx.apply_plan(p,target)
            text=profile.read_text();self.assertIn('local_key: keep',text);self.assertNotIn('aurora-tdd',text)
            self.assertIn('mode: separate_dimensions',text);self.assertNotIn('cached_input_weight_percent',text)

if __name__=='__main__':unittest.main()
