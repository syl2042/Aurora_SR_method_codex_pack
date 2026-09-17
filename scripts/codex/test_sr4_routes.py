import json
import shutil
import tempfile
import unittest
from pathlib import Path
from sr_route_check import check, select
ROOT=Path(__file__).resolve().parents[2]
class RoutingTests(unittest.TestCase):
    def test_eight_scenarios_and_late_discovery(self):
        cases={
            'simple':([],set()),
            'small_change':(['mutation','fact','recommendation','memory','verification','closure','context'],{'authority','fact','evidence','memory','contracts','verification','completion','context'}),
            'business':(['lot','structural'],{'design-evidence','execution','impact'}),
            'ui':(['ui','verification'],{'ui','verification'}),
            'resume':(['resume','context'],{'resume','context'}),
            'agent':(['agent','shared'],{'skills','propagation'}),
            'lot':(['lot','closure'],{'design-evidence','execution','completion','contracts'}),
            'pass':(['lot','pass','goal'],{'design-evidence','execution','passes','runtime-goal'}),
        }
        for name,(events,expected) in cases.items():
            with self.subTest(name=name):
                actual={Path(p).stem for p in select(ROOT,events)['sources']};self.assertEqual(actual,expected)
                if events:
                    expanded={Path(p).stem for p in select(ROOT,events+['shared','structural'])['sources']}
                    self.assertTrue(actual<=expanded);self.assertTrue({'propagation','impact'}<=expanded)

    def test_unknown_trigger_cannot_silently_drop_a_gate(self):
        with self.assertRaises(ValueError):select(ROOT,['unknown'])

    def test_missing_gate_module_is_rejected_in_installed_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);base=root/'docs/codex';base.mkdir(parents=True)
            shutil.copy(ROOT/'core/SR_ROUTES.json',base/'SR_ROUTES.json')
            shutil.copytree(ROOT/'core/procedures',base/'procedures')
            for name in ['fact','propagation','completion','authority']:
                p=base/'procedures'/f'{name}.md';data=p.read_bytes();p.unlink()
                self.assertTrue(any(name in error for error in check(root)))
                p.write_bytes(data)
            self.assertEqual(check(root),[])

if __name__=='__main__':unittest.main()
