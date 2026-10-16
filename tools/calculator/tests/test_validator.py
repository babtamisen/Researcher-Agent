import copy, json, subprocess, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
try:
 from validate import validate
except ImportError:
 def validate(record): return {'status':'not_implemented'}

def quantity(v, unit='USD', scale='million'):
 return dict(value=v,unit=unit,scale=scale,period='FY2024',source='fixture:A')
def eps():
 return dict(operation='eps',inputs={'income':quantity('87000'),'shares':quantity('12480','shares')},claim={'value':'6.97','places':2})
class Tests(unittest.TestCase):
 def test_eps(self): self.assertEqual(validate(eps())['status'],'verified')
 def test_wrong_denominator(self):
  r=eps();r['inputs']['shares']['value']='1248';self.assertEqual(validate(r)['status'],'unable_to_verify')
 def test_scale_conversion(self):
  r=eps();r['inputs']['income']=quantity('87',scale='billion');self.assertEqual(validate(r)['status'],'verified')
 def test_currency(self):
  r=eps();r['inputs']['income']['unit']='EUR';self.assertEqual(validate(r)['status'],'unable_to_verify')
 def test_period(self):
  r=eps();r['inputs']['shares']['period']='FY2023';self.assertEqual(validate(r)['status'],'unable_to_verify')
 def test_missing_source(self):
  r=eps();r['inputs']['income']['source']='';self.assertEqual(validate(r)['status'],'unable_to_verify')
 def test_nonfinite(self):
  r=eps();r['inputs']['income']['value']='NaN';self.assertEqual(validate(r)['status'],'unable_to_verify')
 def test_zero_shares(self):
  r=eps();r['inputs']['shares']['value']='0';self.assertEqual(validate(r)['status'],'unable_to_verify')
 def test_unknown_fields(self):
  r=eps();r['formula']='arbitrary';self.assertEqual(validate(r)['status'],'unable_to_verify')
 def test_liquidity(self):
  r=liquidity();self.assertEqual(validate(r)['status'],'verified')
 def test_bridge_blocks_result(self):
  r=liquidity();r['inputs']['available']['value']='208';o=validate(r);self.assertEqual(o['status'],'unable_to_verify');self.assertNotIn('result',o)
 def test_rate(self): self.assertEqual(validate(rate())['status'],'verified')
 def test_rate_percent_literal(self):
  r=rate();r['inputs']['rate']['value']='5.8%';self.assertEqual(validate(r)['status'],'unable_to_verify')
 def test_rate_domain(self):
  r=rate();r['inputs']['rate']['value']='-101';self.assertEqual(validate(r)['status'],'unable_to_verify')
 def test_reverse_rate(self):
  r=rate();r['operation']='annualize';r['inputs']['rate']['value']='1.419488742901';r['claim']['value']='5.80';self.assertEqual(validate(r)['status'],'verified')
 def test_malformed_cli(self):
  p=subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'validate.py')],input='{',text=True,capture_output=True);self.assertEqual(p.returncode,2);self.assertEqual(json.loads(p.stdout)['status'],'unable_to_verify')
def liquidity():
 return dict(operation='net_debt',inputs={k:quantity(v) for k,v in dict(gross='280',restricted='38',pledged='17',available='225',debt='427').items()},claim={'value':'202000000','places':0})
def rate():
 return dict(operation='deannualize',inputs={'rate':quantity('5.8','percent','one')},claim={'value':'1.41949','places':5})
if __name__=='__main__': unittest.main()
