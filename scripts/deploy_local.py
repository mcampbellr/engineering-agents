#!/usr/bin/env python3
"""Retire legacy Claude entries and deploy the new Codex links and routing policy.

Default is a read-only plan. --apply requires a saved --expected-state plan to
avoid replacing a source or instruction file edited since the plan was made.
Existing skill folders are backed up under ~/.local/state/engineering-agents/.
This does not install runtimes, run audits, or change permissions/models.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys


def fingerprint(path):
    if path.is_symlink():
        target=path.resolve()
        return 'symlink:'+str(path.readlink())+':'+str(fingerprint(target) if target.exists() else None)
    if not path.exists():return None
    if path.is_file():return hashlib.sha256(path.read_bytes()).hexdigest()
    digest=hashlib.sha256()
    for item in sorted(path.rglob('*')):
        if '__pycache__' in item.parts or item.suffix in ('.pyc','.pyo'):continue
        if item.is_file():
            digest.update(str(item.relative_to(path)).encode());digest.update(item.read_bytes())
    return digest.hexdigest()


def plan(root,home):
    catalog=json.loads((root/'catalog.json').read_text())
    links=[]
    retired=[home/'.claude/skills'/skill['name'] for skill in catalog.get('bundled_skills',[])]
    retired += [home/'.claude/agents'/(name+'.md') for name in
                ['code-review','superreview-correctness-security-subagent','superreview-code-quality-subagent']]
    for skill in catalog['roles']+catalog.get('bundled_skills',[]):
        links.append((home/'.codex/skills'/skill['name'],root/'skills'/skill['name']))
    for _,target in links:
        if not (target/'SKILL.md').is_file():raise ValueError('Missing target skill: '+str(target))
    policies=[home/'.claude/CLAUDE.md',home/'.codex/AGENTS.md']
    return {'root':str(root),'version':catalog['version'],
            'retire':[{'path':str(path),'before':fingerprint(path)} for path in retired],
            'links':[{'path':str(path),'target':str(target),'before':fingerprint(path)} for path,target in links],
            'policies':[{'path':str(path),'before':fingerprint(path)} for path in policies]}


def apply(state,home):
    root=Path(state['root']);policy=(root/'core/routing-policy.md').read_text().strip()
    marker='<!-- BEGIN ENGINEERING AUDIT ROUTING -->';end='<!-- END ENGINEERING AUDIT ROUTING -->'
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup=home/'.local/state/engineering-agents/migrations'/stamp
    changes=[]
    for entry in state['retire']:
        path=Path(entry['path'])
        if path.exists() or path.is_symlink():
            destination=backup/path.relative_to(home)
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.move(str(path),str(destination));changes.append(str(path))
    for entry in state['links']:
        path=Path(entry['path']);target=Path(entry['target'])
        if path.is_symlink() and path.resolve()==target.resolve():continue
        path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists() or path.is_symlink():
            destination=backup/path.relative_to(home)
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.move(str(path),str(destination))
        path.symlink_to(os.path.relpath(target,path.parent.resolve()),target_is_directory=True);changes.append(str(path))
    for entry in state['policies']:
        path=Path(entry['path']);previous=path.read_text() if path.exists() else ''
        if marker in previous:
            begin=previous.index(marker);finish=previous.index(end,begin)+len(end)
            updated=previous[:begin]+policy+previous[finish:]
        else:updated=previous.rstrip()+'\n\n'+policy+'\n'
        if updated!=previous:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(updated);changes.append(str(path))
    return {'version':state['version'],'changed':changes,'backup_root':str(backup) if backup.exists() else None}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True,help='permanent, updated plugin source directory')
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--expected-state',help='saved JSON plan required by --apply')
    args=parser.parse_args();home=Path.home();state=plan(Path(args.root).resolve(),home)
    if args.apply:
        if not args.expected_state:parser.error('--apply requires --expected-state')
        expected=json.loads(Path(args.expected_state).read_text())
        if state!=expected:raise SystemExit('State changed since the plan; review a fresh plan before applying.')
        print(json.dumps(apply(state,home),indent=2))
    else:print(json.dumps(state,indent=2))
if __name__=='__main__':main()
