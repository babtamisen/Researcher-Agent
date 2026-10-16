import json,subprocess,sys,unittest
from pathlib import Path
SCRIPT=Path(__file__).resolve().parents[1]/'render.py'
class RenderTests(unittest.TestCase):
 def run_render(self,obj):
  return subprocess.run([sys.executable,str(SCRIPT)],input=json.dumps(obj),capture_output=True,text=True)
 def test_preserves_exact_blocks(self):
  a={'blocks':['EPS: 3.47 USD/share. [fictional:source#income]','Unable to verify. [fictional:source#period]']}
  p=self.run_render(a);self.assertEqual(p.returncode,0);self.assertEqual(p.stdout,'\n\n'.join(a['blocks'])+'\n')
 def test_invalid_block_no_partial_output(self):
  p=self.run_render({'blocks':['valid',None]});self.assertEqual(p.returncode,2);self.assertEqual(p.stdout,'')
 def test_unknown_fields(self):
  self.assertEqual(self.run_render({'blocks':['ok'],'rewrite':True}).returncode,2)
if __name__=='__main__':unittest.main()
