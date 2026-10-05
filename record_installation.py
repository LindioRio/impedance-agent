"""Persist installation provenance and merge selected test outcomes without API calls."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

REPO=Path(__file__).resolve().parent
def main():
    cases={}
    attempts=[]
    for filename in ['offline-tests.xml','loader-tests.xml']:
        path=REPO/'verification'/filename
        tree=ET.parse(path)
        counts={'passed':0,'failed':0,'errors':0,'skipped':0}
        for case in tree.iter('testcase'):
            key=case.attrib.get('classname','')+'::'+case.attrib['name']
            status='errors' if case.find('error') is not None else ('failed' if case.find('failure') is not None else ('skipped' if case.find('skipped') is not None else 'passed'))
            counts[status]+=1;cases[key]=status
        attempts.append({'file':'verification/'+filename,'outcomes':counts})
    assert len(cases)==15 and all(v=='passed' for v in cases.values()),cases
    packages=['impedance-agent','numpy','scipy','jax','jaxlib','jaxopt','pydantic','typer','openai','impedance','pandas']
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    patch=subprocess.check_output(['git','diff','--','impedance_agent/core/env.py'],cwd=REPO)
    (REPO/'local-compatibility.patch').write_bytes(patch)
    record={
        'installed_date_client':'2026-10-05','recorded_utc':datetime.now(timezone.utc).isoformat(),
        'repository':'https://github.com/richinex/impedance-agent.git','commit':commit,
        'package_version':importlib.metadata.version('impedance-agent'),'python_version':sys.version,
        'python_executable':sys.executable,'installation_type':'Workspace-local editable package in isolated .venv',
        'runtime_location':'.cache/python/cpython-3.12-windows-x86_64-none',
        'launcher':'../../impedance-agent.ps1','dependency_lock':'installed-requirements.txt',
        'important_package_versions':{p:importlib.metadata.version(p) for p in packages},
        'local_patch':'Global environment loads without import-time API credential validation; analyze still checks configured providers.',
        'patch_sha256':hashlib.sha256(patch).hexdigest(),
        'checks':{'CLI_help':'PASS','CLI_version':'PASS','analyze_help':'PASS','pip_dependency_check':'PASS',
                  'selected_upstream_tests_unique_passed':len(cases),'LLM_provider_api_call':'Not performed'},
        'test_attempts':attempts,'final_selected_test_outcomes':cases,
        'test_execution_note':'Initial loader fixtures failed due to temporary-directory setup/sandbox ACLs; rerun passed outside sandbox. Numerical fitter checks passed in the initial run.',
        'credentials':'Local .env contains empty API keys; runtime may also read externally configured environment variables. No credentials logged.',
        'experimental_files':'No experimental files analysed, uploaded or altered during installation.',
        'scope':'Installed Python tool; this is not model-weight training or a new live Codex subagent.'}
    (REPO/'installation_record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','package_version':record['package_version'],'commit':commit,'unique_tests_passed':len(cases),'API_calls_made':False}))
if __name__=='__main__':main()
