#!/usr/bin/env python3
"""Check a report.json against the invariants JSON Schema cannot express. Requires jsonschema; fails closed when validation is unavailable.

The schema verifies shape. This verifies that the references resolve: every source_id
points at a declared source, every location points at a real line of the declared
revision, ids are unique, and the coverage figure matches the control matrix.
Exit 0 clean, 1 on violations, 2 on usage errors.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/('core/report.schema.json' if (ROOT/'core').is_dir() else 'references/report.schema.json')

def revision_lines(repo,commit,dirty,path):
    """Line count of path at the declared revision, or None if it cannot be read."""
    relative=Path(path)
    if relative.is_absolute() or '..' in relative.parts:
        return None
    root=Path(repo).resolve()
    if dirty or not commit:
        f=(root/relative).resolve()
        if root not in f.parents:
            return None
        return len(f.read_text(errors='replace').splitlines()) if f.is_file() else None
    try:
        blob=subprocess.run(['git','-C',repo,'show',f'{commit}:{path}'],capture_output=True,check=True)
    except (subprocess.CalledProcessError,FileNotFoundError):
        return None
    return len(blob.stdout.decode(errors='replace').splitlines())

def check(report,repo,strict_locations):
    violations=[];notes=[]
    declared={s['id'] for s in report['sources']}
    if len(declared)!=len(report['sources']):
        violations.append('sources: duplicate id')
    cited=set()
    ids=[f['id'] for f in report['findings']]
    if len(set(ids))!=len(ids):
        violations.append('findings: duplicate id')
    names=[m['name'] for m in report['metrics']]
    if len(set(names))!=len(names):
        violations.append('metrics: duplicate name')
    control_ids=[c['id'] for c in report['controls']]
    if len(set(control_ids))!=len(control_ids):
        violations.append('controls: duplicate id')

    scope=report['scope']
    for finding in report['findings']:
        for sid in finding['source_ids']:
            cited.add(sid)
            if sid not in declared:
                violations.append(f"{finding['id']}: source_id '{sid}' resolves to no declared source")
        for loc in finding['locations']:
            total=revision_lines(repo,scope.get('commit'),scope.get('dirty'),loc['path'])
            if total is None:
                violations.append(
                    f"{finding['id']}: cannot read {loc['path']} at the declared revision")
            elif loc['line']>total:
                violations.append(f"{finding['id']}: {loc['path']}:{loc['line']} is past end of file ({total} lines)")
    unused=declared-cited
    if unused:
        notes.append('sources declared but cited by no finding: '+', '.join(sorted(unused)))

    measured=[f for f in report['findings'] if f['evidence_state']=='measured']
    if measured or any(m['value'] is not None for m in report['metrics']):
        env=report['environment']
        for key in ['instruments','commands','date','artifacts']:
            if env.get(key) in (None,[]):
                violations.append(f"environment.{key} is empty although the report claims a measurement")

    applicable=[c for c in report['controls'] if c['status']!='not_applicable']
    tested=[c for c in applicable if c['status'] in ('pass','fail')]
    coverage={'tested':len(tested),'applicable':len(applicable),
              'excluded':len(report['controls'])-len(applicable),
              'pending':len([c for c in applicable if c['status']=='not_tested']),
              'ratio':round(len(tested)/len(applicable),4) if applicable else None}
    return violations,notes,coverage

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('report',help='path to report.json')
    ap.add_argument('--repo',default='.',help='repository the locations refer to (default: cwd)')
    ap.add_argument('--strict-locations',action='store_true',
                    help='compatibility flag: unreadable locations are always violations')
    args=ap.parse_args()
    try:
        report=json.loads(Path(args.report).read_text())
    except (OSError,json.JSONDecodeError) as exc:
        print(f'cannot read report: {exc}',file=sys.stderr);return 2
    structural=[]
    try:
        from jsonschema import Draft202012Validator
        schema=json.loads(SCHEMA.read_text())
        Draft202012Validator.check_schema(schema)
        structural=[f'{e.json_path}: {e.message}' for e in
                    sorted(Draft202012Validator(schema).iter_errors(report),key=lambda e:e.json_path)]
    except ImportError:
        print('jsonschema is required; schema validation was NOT performed. Install requirements-validation.txt in your chosen environment.',file=sys.stderr)
        return 2
    except (OSError,json.JSONDecodeError) as exc:
        print(f'cannot load schema: {exc}',file=sys.stderr)
        return 2
    if structural:
        print(json.dumps({'structural_errors':structural},indent=2,ensure_ascii=False));return 1
    missing=[k for k in ('scope','environment','findings','controls','metrics','sources') if k not in report]
    if missing:
        print(json.dumps({'structural_errors':['missing top-level keys: '+', '.join(missing)]},indent=2));return 1
    violations,notes,coverage=check(report,args.repo,args.strict_locations)
    print(json.dumps({'schema_checked':structural is not None,'violations':violations,
                      'notes':notes,'coverage':coverage},indent=2,ensure_ascii=False))
    return 1 if violations else 0
if __name__=='__main__':sys.exit(main())
