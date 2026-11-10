"""Rebuild from archived data by default. Network refresh only with --acquire."""
from pathlib import Path
import argparse,subprocess,sys,os
ROOT=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--acquire',action='store_true');ap.add_argument('--test',action='store_true');args=ap.parse_args()
    env=os.environ.copy();env['PYTHONPATH']=str(ROOT)+os.pathsep+env.get('PYTHONPATH','')
    stages=[]
    if args.acquire: stages+=['project_a/acquire.py','project_b/acquire_rules.py','project_b/evidence/acquire.py','project_c/collect.py']
    stages+=['project_a/process.py','project_b/evidence/process.py','project_b/evidence/finalize_evidence.py','project_c/process.py','project_c/concordance.py','project_a/export.py','project_b/export.py','project_c/export.py','build_handoff.py']
    for stage in stages:
        print(f'Running {stage}',flush=True)
        subprocess.run([sys.executable,'-m',stage.removesuffix('.py').replace('/','.')],cwd=ROOT,env=env,check=True)
    if args.test:
        subprocess.run([sys.executable,'-m','pytest','-q','--junitxml=reports/pytest_results.xml'],cwd=ROOT,env=env,check=True)
        subprocess.run([sys.executable,'build_handoff.py'],cwd=ROOT,env=env,check=True)
if __name__=='__main__':main()
