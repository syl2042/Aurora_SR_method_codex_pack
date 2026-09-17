import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def module(name):
    spec=importlib.util.spec_from_file_location(name, ROOT/'scripts/codex'/f'{name}.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class SR4ToolsTests(unittest.TestCase):
    def test_short_output_stays_short(self):
        self.assertEqual(module('aurora_token_run').compact('OK\n'), 'OK\n')

    def test_unique_middle_error_survives_repeated_warnings(self):
        text='\n'.join(['info']*40+['warning repeated']*100+['fatal UNIQUE_MIDDLE']+['info']*100)
        out=module('aurora_token_run').compact(text)
        self.assertIn('fatal UNIQUE_MIDDLE',out)
        self.assertLess(out.count('warning repeated'),4)

    def test_wrapper_keeps_exit_code_and_distinct_raw_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            cmd=[sys.executable,str(ROOT/'scripts/codex/aurora_token_run.py'),'--',sys.executable,'-c',"print('fatal diagnostic'); raise SystemExit(7)"]
            for _ in range(2):
                result=subprocess.run(cmd,cwd=tmp,capture_output=True,text=True)
                self.assertEqual(result.returncode,7)
                self.assertIn('fatal diagnostic',result.stdout)
            logs=list((Path(tmp)/'output/codex/raw').glob('*.log'))
            self.assertEqual(len(logs),2)
            self.assertTrue(all('fatal diagnostic' in p.read_text() for p in logs))

    def test_multiple_resume_candidates_require_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ['a','b']:
                p=root/'tasks'/name/'NEXT_SESSION_PROMPT.md';p.parent.mkdir(parents=True);p.write_text(name)
            cmd=[sys.executable,str(ROOT/'scripts/codex/find_next_session_prompt.py'),'--root',tmp,'--json']
            result=json.loads(subprocess.check_output(cmd))
            self.assertTrue(result['ambiguous']);self.assertIsNone(result['selected'])
            result=json.loads(subprocess.check_output(cmd+['--prompt','tasks/a/NEXT_SESSION_PROMPT.md']))
            self.assertEqual(result['selected']['path'],'tasks/a/NEXT_SESSION_PROMPT.md')

    def test_resume_rejects_outside_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'root';root.mkdir();p=Path(tmp)/'NEXT_SESSION_PROMPT.md';p.write_text('outside')
            result=subprocess.run([sys.executable,str(ROOT/'scripts/codex/find_next_session_prompt.py'),'--root',str(root),'--prompt',str(p),'--json'],capture_output=True)
            self.assertNotEqual(result.returncode,0)

    def test_routes_exist_and_cover_guarantees(self):
        data=json.loads((ROOT/'core/SR_ROUTES.json').read_text())
        sources={s for r in data['routes'] for s in r['sources']}
        for name in ['fact','evidence','design-evidence','impact','propagation','ui','passes','runtime-goal','completion','context','contracts','resume']:
            self.assertIn(f'procedures/{name}.md',sources)
        for rel in sources:self.assertTrue((ROOT/'core'/rel).is_file(),rel)

    def test_lossless_rule_moves(self):
        rows=json.loads((ROOT/'scripts/codex/fixtures/context_refactor/rule_witnesses.json').read_text())
        for row in rows:
            self.assertIn(row['text'],(ROOT/row['destination']).read_text(),row['id'])

if __name__=='__main__':unittest.main()
