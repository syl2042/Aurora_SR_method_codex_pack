import copy
import json
import unittest
from pathlib import Path
from render_sr_state import project

ROOT=Path(__file__).resolve().parents[2]

class DerivedViewTests(unittest.TestCase):
    def contract(self):
        return json.loads((ROOT/'tasks/_TEMPLATE/sr_contract.json').read_text())

    def test_partial_implementation_never_becomes_user_testing(self):
        data=self.contract();r=data['validated_requests'][0];r['implementation_status']='partial'
        r['expected_evidence']=[{'kind':'e2e','required':True,'description':'real E2E'}]
        before=copy.deepcopy(data);view=project(data)
        self.assertEqual(view['status'],'repair');self.assertEqual(data,before)

    def test_complete_missing_human_acceptance_remains_open(self):
        data=self.contract();r=data['validated_requests'][0];r['implementation_status']='complete'
        r['expected_evidence']=[{'kind':'human_acceptance','required':True,'description':'human'}]
        view=project(data);self.assertEqual(view['status'],'user_testing');self.assertEqual(view['open_requirement_ids'],[r['id']])
        self.assertEqual(r['obtained_evidence'],[])

    def test_no_requests_is_not_success(self):
        data=self.contract();data['validated_requests']=[]
        with self.assertRaises(ValueError):project(data)

    def test_legacy_view_does_not_convert_schema(self):
        data=self.contract();data['schema_version']='3.0.0'
        with self.assertRaises(ValueError):project(data)
        self.assertEqual(data['schema_version'],'3.0.0')

if __name__=='__main__':unittest.main()
