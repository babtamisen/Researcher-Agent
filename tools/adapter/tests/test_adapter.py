import sys,unittest,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from adapter import adapt

def fixture():
    rows=[]
    for id,v in zip(['G','R','P','A','D','C'],['684','76','28','561','902','341']):
        rows.append(dict(row_id=id,locator='fixture:'+id,original_label=id,excerpt='Source '+id,value=v,currency='USD',scale='million',as_of='2026-06-30'))
    return dict(evidence=rows,mapping=dict(gross='G',restricted='R',pledged='P',available='A',debt='D'),supplied_claim=dict(row_id='C',places=0))
class Tests(unittest.TestCase):
    def test_million_and_unresolved(self):
        out=adapt(fixture());self.assertEqual(out['record']['claim']['value'],'341000000');self.assertEqual(out['validation']['status'],'unable_to_verify');self.assertNotIn('result',out['validation'])
    def test_billion(self):
        d=fixture();d['evidence'][-1].update(value='0.341',scale='billion');self.assertEqual(adapt(d)['record']['claim']['value'],'341000000.000')
    def test_missing_scale(self):
        d=fixture();del d['evidence'][0]['scale'];self.assertEqual(adapt(d)['status'],'unable_to_adapt')
    def test_currency(self):
        d=fixture();d['evidence'][0]['currency']='EUR';self.assertEqual(adapt(d)['status'],'unable_to_adapt')
    def test_period(self):
        d=fixture();d['evidence'][-1]['as_of']='2025';self.assertEqual(adapt(d)['status'],'unable_to_adapt')
    def test_duplicate_row(self):
        d=fixture();d['evidence'].append(copy.deepcopy(d['evidence'][0]));self.assertEqual(adapt(d)['status'],'unable_to_adapt')
    def test_model_converted_field_rejected(self):
        d=fixture();d['supplied_claim']['calculator_value_USD']='341';self.assertEqual(adapt(d)['status'],'unable_to_adapt')
    def test_preserves_evidence(self):
        d=fixture();before=copy.deepcopy(d);self.assertEqual(adapt(d)['evidence'],d['evidence']);self.assertEqual(d,before)
    def test_valid_bridge(self):
        d=fixture();d['evidence'][3]['value']='580';d['evidence'][5]['value']='322';self.assertEqual(adapt(d)['validation']['result'],'322000000')
if __name__=='__main__':unittest.main()
