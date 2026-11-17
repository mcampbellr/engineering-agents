#!/usr/bin/env python3
"""Probe report.schema.json with crafted documents; asserts what it must reject, not what it describes."""
import copy
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

VALID={
 'schema_version':'1.0','package_version':'0.1.0','skill':'scalability-audit','run_id':'probe',
 'scope':{'repository':'local','commit':'0'*40,'dirty':False,'mode':'diff','description':'probe scope'},
 'environment':{'stack':'python 3.12','versions':{'python':'3.12.3'},'workload':None,'dataset':None,
   'seed':None,'hardware':None,'limits':None,'instruments':None,'commands':None,'date':'2026-10-26',
   'warmup':None,'duration':None,'repetitions':None,'artifacts':None},
 'verdict':'requires_changes',
 'findings':[{'id':'F1','title':'Retry amplification','area':'resilience','severity':'high',
   'confidence':'high','evidence_state':'static','locations':[{'path':'retry.py','line':12}],
   'mechanism':'nested retries multiply attempts','trigger':'slow dependency','impact':'27x leaf load',
   'existing_mitigations':'none observed','counterevidence':'no retry budget found',
   'recommendation':'single owner of retries','tradeoffs':'slower recovery on transient faults',
   'validation':{'procedure':'count leaf attempts','acceptance':'attempts <= 3','executed':False,
     'artifact':None},'source_ids':['aws-retries']}],
 'controls':[{'id':'C1','status':'pass','criterion':'deadline propagated','evidence':'client.py:40 passes deadline','reason':'checked call chain'},
             {'id':'C2','status':'not_applicable','evidence':None,'criterion':'queue depth bounded','reason':'no queue in scope'}],
 'metrics':[{'name':'leaf_attempts','unit':'attempts','value':None,'baseline':None,'target':3,
   'target_origin':'proposal pending approval','method':'static count','artifact':None,'sample_size':None}],
 'sources':[{'id':'aws-retries','url':'https://docs.aws.amazon.com/','version':None,'accessed_on':'2026-10-26'}],
 'limitations':['no load test executed'],'next_steps':['run the attempt-count experiment']}

def mutate(path,value):
    def apply(doc):
        node=doc
        for key in path[:-1]:node=node[key]
        if value is DELETE:del node[path[-1]]
        else:node[path[-1]]=value
        return doc
    return apply
DELETE=object()

CASES=[
 ('baseline valid report',lambda d:d,True),
 ('measured without executed validation',mutate(['findings',0,'evidence_state'],'measured'),False),
 ('executed=true without artifact',mutate(['findings',0,'validation','executed'],True),False),
 ('executed=false carrying an artifact',mutate(['findings',0,'validation','artifact'],'runs/out.json'),False),
 ('static finding without a location',mutate(['findings',0,'locations'],[]),False),
 ('pass control without evidence',mutate(['controls',0,'evidence'],None),False),
 ('metric with a value but no artifact',mutate(['metrics',0,'value'],2.0),False),
 ('metric without a value but with an artifact',mutate(['metrics',0,'artifact'],'runs/out.json'),False),
 ('metric without a value but with a sample size',mutate(['metrics',0,'sample_size'],30),False),
 ('requires_changes backed only by a hypothesis',mutate(['findings',0,'evidence_state'],'hypothesis'),False),
 ('requires_changes with an empty findings list',mutate(['findings'],[]),False),
 ('no_blocking_findings next to a confirmed high',mutate(['verdict'],'no_blocking_findings'),False),
 ('environment missing a declared key',mutate(['environment','hardware'],DELETE),False),
 ('unknown top-level field',mutate(['health_score'],8.6),False),
]

def main():
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print(json.dumps({'status':'not_run','reason':'jsonschema is required; install requirements-validation.txt'},indent=2));return 2
    schema=json.loads((ROOT/'core/report.schema.json').read_text())
    Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema)
    results=[];failed=0
    for name,apply,should_pass in CASES:
        errors=sorted(validator.iter_errors(apply(copy.deepcopy(VALID))),key=lambda e:e.json_path)
        accepted=not errors
        ok=accepted==should_pass
        failed+=not ok
        results.append({'case':name,'expected':'accept' if should_pass else 'reject',
            'observed':'accept' if accepted else 'reject','outcome':'ok' if ok else 'MISMATCH',
            'first_error':None if accepted else errors[0].message[:160]})
    print(json.dumps({'schema':'urn:engineering-agents:report:1.0','probes':len(CASES),
        'mismatches':failed,'results':results},indent=2,ensure_ascii=False))
    return 1 if failed else 0
if __name__=='__main__':sys.exit(main())
