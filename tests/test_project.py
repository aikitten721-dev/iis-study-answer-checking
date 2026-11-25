import unittest
import sys
import json
from io import BytesIO
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import retrieve
from app import search,load_cases,Handler

class EvidenceChecks(unittest.TestCase):
    def test_source_metadata_survives_ranking(self):
        for p in retrieve.retrieve('coursework deadline'):
            self.assertTrue(all(k in p for k in ['file','source','section','date','text','score','superseded']))
    def test_current_penalty_precedes_superseded(self):
        hits=retrieve.retrieve('what is the penalty for late submission',k=14)
        names=[h['file'] for h in hits]
        self.assertLess(names.index('handbook_late.md'),names.index('handbook_2024.md'))
        self.assertTrue(any(h['superseded'] for h in hits))
    def test_deadline_is_still_retrieved(self):
        self.assertEqual(search('when is coursework 1 due')['hits'][0]['file'],'handbook.md')
    def test_unrelated_question_has_no_displayed_evidence(self):
        result=search('quantum entanglement')
        self.assertEqual(result['status'],'Not verified')
        self.assertEqual(result['hits'],[])
    def test_empty_request_withholds_result(self):
        self.assertEqual(search('')['hits'],[])
    def test_missing_source_transition_does_not_invent_support(self):
        cases=load_cases()
        missing=next(c for c in cases if c['id']=='missing')
        self.assertTrue(missing['needs_source'])
        self.assertIn('no source',missing['steps'][0]['status'])
    def test_correction_withdraws_old_label_before_new_result(self):
        cases=load_cases()
        case=next(c for c in cases if c['id']=='mismatch')
        self.assertEqual(case['steps'][1]['status'],'Awaiting recheck')
        self.assertIn('Inconsistent',case['steps'][2]['status'])
    def test_checking_passages_match_searchable_study_notes(self):
        for case in load_cases():
            note=next(p for p in retrieve.load() if p['file']==case['source_file'])
            self.assertEqual(case['source'],note['text'])
            self.assertIn(note['section'],case['location'])
        self.assertEqual(search('capacity chunks grouping rehearsal')['hits'][0]['file'],'sample_notes_n1.md')
        self.assertEqual(search('recall recognition visible option')['hits'][0]['file'],'sample_notes_n2.md')
    def request(self,path):
        handler=object.__new__(Handler)
        handler.path=path
        handler.wfile=BytesIO()
        handler.send_response=lambda code:setattr(handler,'test_status',code)
        handler.send_header=lambda name,value:None
        handler.end_headers=lambda:None
        handler.do_GET()
        self.assertEqual(handler.test_status,200)
        return json.loads(handler.wfile.getvalue().decode('utf-8'))
    def test_fixture_http_route_returns_resolved_sources(self):
        result=self.request('/fixtures.json')
        self.assertEqual(len(result),3)
        self.assertIn('grouping',result[1]['source'])
        self.assertTrue(result[2]['needs_source'])
    def test_search_http_route_returns_version_adjustment_notice(self):
        result=self.request('/api/search?q=what+is+the+penalty+for+late+submission')
        self.assertIn('×0.3',result['source_status_note'])
        self.assertEqual(result['hits'][0]['file'],'handbook_late.md')
        self.assertTrue(any(h['superseded'] for h in result['hits']))
    def test_page_loads_single_fixture_endpoint(self):
        page=(Path(__file__).resolve().parents[1]/'index.html').read_text(encoding='utf-8')
        self.assertIn("fetch('/fixtures.json')",page)
        self.assertNotIn('Everyone can hold exactly four items.',page)

if __name__=='__main__': unittest.main(verbosity=2)
