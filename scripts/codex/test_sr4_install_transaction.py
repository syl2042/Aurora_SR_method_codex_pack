import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
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

    def test_failure_rolls_back_applied_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp);p=plan(target);original=tx.atomic_write;failed=False
            def fail_once(path,data):
                nonlocal failed
                if path.name=='SR_BOOTSTRAP.md' and not failed:
                    failed=True;raise OSError('injected disk error')
                return original(path,data)
            with patch.object(tx,'atomic_write',side_effect=fail_once):
                with self.assertRaises(OSError):tx.apply_plan(p,target)
            self.assertFalse((target/'AGENTS.md').exists())
            journal=next(target.glob('docs/codex/upgrade_backups/*/transaction.json'))
            self.assertEqual(json.loads(journal.read_text())['status'],'restored')

    def test_symlink_cannot_escape_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'repo';target.mkdir();outside=Path(tmp)/'outside';outside.mkdir();(target/'docs').symlink_to(outside)
            with self.assertRaisesRegex(ValueError,'symlink'):plan(target)

    def test_version_number_does_not_select_algorithm(self):
        for version in ['unknown','0.0.1','99.0.0']:
            with self.subTest(version=version),tempfile.TemporaryDirectory() as tmp:
                target=Path(tmp);p=target/'docs/codex/SR_PACK_VERSION.json';p.parent.mkdir(parents=True);p.write_text(json.dumps({'version':version}))
                self.assertFalse(plan(target)['conflicts'])

if __name__=='__main__':unittest.main()
