#!/usr/bin/env python3
"""Confirm four local fixture mechanisms; does not evaluate any AI agent."""
import gc
import importlib.util
import json
import platform
import sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'fixtures'/f'{name}.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def main():
    result={'python':platform.python_version(),'fixture_checks':[]}
    retry=load('retry');counts=[]
    for fn in [retry.layered,retry.single_owner]:
        c=[0]
        try:fn(c)
        except TimeoutError:pass
        counts.append(c[0])
    assert counts==[27,3],counts
    result['fixture_checks'].append({'case':'S1/S2','leaf_attempts':counts})
    tenant=load('tenant');session={'tenant':'A'}
    assert tenant.unsafe_get(session,'b1')['tenant']=='B'
    for fn in [tenant.leaky_get,tenant.safe_get]:
        try:fn(session,'b1')
        except PermissionError:pass
        else:raise AssertionError(fn.__name__+' allowed another tenant')
    # The negative control must be clean: absent and forbidden are indistinguishable,
    # only the contracted field comes back, and the caller cannot reach shared state.
    try:tenant.safe_get(session,'zz9')
    except PermissionError:pass
    else:raise AssertionError('safe_get distinguished an absent id')
    assert tenant.safe_get(session,'a1')=={'text':'A synthetic'}
    tenant.safe_get(session,'a1')['text']='MUTATED'
    assert tenant.DOCS['a1']['text']=='A synthetic'
    # leaky_get compares tenants and still leaks: oracle plus a writable handle.
    try:tenant.leaky_get(session,'zz9')
    except KeyError:oracle=True
    else:oracle=False
    assert oracle
    tenant.leaky_get(session,'a1')['text']='MUTATED'
    aliased=tenant.DOCS['a1']['text']=='MUTATED';assert aliased
    tenant.DOCS['a1']['text']='A synthetic'
    result['fixture_checks'].append({'case':'W1/W2','unsafe_cross_tenant':True,'safe_cross_tenant':False,
        'safe_hides_existence':True,'safe_returns_copy':True,'legitimate_access':True})
    result['fixture_checks'].append({'case':'W9','leaky_cross_tenant':False,'leaky_existence_oracle':oracle,
        'leaky_returns_shared_reference':aliased,'leaky_exposes_internal_field':'internal_note' in tenant.leaky_get(session,'a1')})
    conn=sqlite3.connect(':memory:');conn.executescript((ROOT/'fixtures/schema.sql').read_text())
    for _ in range(2):conn.execute('INSERT INTO unsafe_membership VALUES (?,?)',('A','x@example.test'))
    conn.execute('INSERT INTO safe_membership VALUES (?,?)',('A','x@example.test'))
    try:conn.execute('INSERT INTO safe_membership VALUES (?,?)',('A','x@example.test'))
    except sqlite3.IntegrityError:pass
    else:raise AssertionError('unique constraint failed')
    conn.execute('INSERT INTO safe_membership VALUES (?,?)',('B','x@example.test'))
    count=conn.execute('SELECT count(*) FROM unsafe_membership').fetchone()[0];assert count==2
    result['fixture_checks'].append({'case':'D1/D2','unsafe_duplicates':count,'safe_duplicate_rejected':True,'other_tenant_allowed':True})
    # A UNIQUE over a nullable column does not restrict rows whose value is null.
    for _ in range(2):conn.execute('INSERT INTO nullable_membership VALUES (?,?)',('A',None))
    nulls=conn.execute('SELECT count(*) FROM nullable_membership').fetchone()[0];assert nulls==2,nulls
    conn.execute('INSERT INTO nullable_membership VALUES (?,?)',('A','x@example.test'))
    try:conn.execute('INSERT INTO nullable_membership VALUES (?,?)',('A','x@example.test'))
    except sqlite3.IntegrityError:pass
    else:raise AssertionError('non-null duplicate accepted')
    result['fixture_checks'].append({'case':'D6','null_duplicates_accepted':nulls,'non_null_duplicate_rejected':True,'sqlite_version':sqlite3.sqlite_version})
    bulk=load('bulk')
    # CPython reference-counting observations are intentionally not RSS claims.
    if platform.python_implementation()!='CPython':
        result['fixture_checks'].append({'case':'M1/M2','status':'skipped','reason':'live-object assertions target CPython'})
    else:
        peaks={}
        for fn in [bulk.eager,bulk.streaming]:
            peaks[fn.__name__]=[]
            for n in [1000,10000]:
                gc.collect();bulk.Tracked.live=0;bulk.Tracked.max_live=0
                assert fn(n)==n
                peaks[fn.__name__].append(bulk.Tracked.max_live)
                gc.collect();assert bulk.Tracked.live==0
        assert peaks['eager']==[1000,10000],peaks
        assert max(peaks['streaming'])<=2,peaks
        result['fixture_checks'].append({'case':'M1/M2','peak_live_objects':peaks,'unit':'objects, not bytes or RSS'})
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
