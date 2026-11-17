"""Regression checks for portable reports, fail-closed validation and clean builds."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
PROBE=load('schema_probes',ROOT/'evaluation/schema_invariants.py')

class ReportValidation(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.repo=Path(self.temp.name)
        (self.repo/'retry.py').write_text('# sample\n'*20)
        self.report=copy.deepcopy(PROBE.VALID)
        self.report['scope'].update(commit=None,dirty=True)
    def run_report(self,report=None,script=None,without_dependencies=False):
        path=self.repo/'report.json';path.write_text(json.dumps(self.report if report is None else report))
        args=[sys.executable]+(['-S'] if without_dependencies else [])
        return subprocess.run(args+[str(script or ROOT/'scripts/validate_report.py'),str(path),'--repo',str(self.repo)],capture_output=True,text=True,cwd=self.repo)
    def test_valid_report(self):
        self.assertEqual(self.run_report().returncode,0)
    def test_missing_location_is_failure_by_default(self):
        self.report['findings'][0]['locations'][0]['path']='absent.py'
        result=self.run_report();self.assertEqual(result.returncode,1);self.assertIn('cannot read',result.stdout)
    def test_past_end_and_path_escape_rejected(self):
        for path,line in [('retry.py',21),('../outside.py',1),(str(self.repo/'retry.py'),1)]:
            with self.subTest(path=path):
                self.report['findings'][0]['locations']=[{'path':path,'line':line}]
                self.assertEqual(self.run_report().returncode,1)
    def test_missing_schema_field_rejected(self):
        del self.report['verdict'];self.assertEqual(self.run_report().returncode,1)
    def test_dependency_absence_cannot_pass(self):
        result=self.run_report(without_dependencies=True)
        self.assertEqual(result.returncode,2);self.assertIn('NOT performed',result.stderr)
    def test_schema_probes_dependency_absence_cannot_pass(self):
        result=subprocess.run([sys.executable,'-S',str(ROOT/'evaluation/schema_invariants.py')],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
    def test_standalone_skill_works_without_package_core(self):
        skill=self.repo/'standalone'
        shutil.copytree(ROOT/'skills/scalability-audit',skill)
        self.assertFalse((skill/'core').exists())
        self.assertEqual(self.run_report(script=skill/'scripts/validate_report.py').returncode,0)

class BuildPortability(unittest.TestCase):
    def test_runtime_bytecode_does_not_change_checksums(self):
        build=load('builder',ROOT/'scripts/build.py')
        with tempfile.TemporaryDirectory() as temp:
            old=build.ROOT;build.ROOT=Path(temp)
            try:
                (build.ROOT/'source.md').write_text('canonical')
                baseline=build.checksums({'SHA256SUMS'})
                cache=build.ROOT/'evaluation/__pycache__';cache.mkdir(parents=True)
                (cache/'probe.cpython-399.pyc').write_bytes(b'local bytecode')
                (build.ROOT/'scratch.pyo').write_bytes(b'optimized')
                self.assertEqual(build.checksums({'SHA256SUMS'}),baseline)
            finally:build.ROOT=old
    def test_fixture_prompts_include_exact_source_for_both_arms(self):
        build=load('eval_builder',ROOT/'scripts/build.py')
        generated=build.eval_suite(json.loads((ROOT/'catalog.json').read_text()))
        case=generated['evals/web-security-audit-w9/case.yaml']
        prompt=json.loads(next(ln.split(': ',1)[1] for ln in case.splitlines() if ln.startswith('  prompt: ')))
        self.assertIn((ROOT/'evaluation/fixtures/tenant.py').read_text(),prompt)
        self.assertNotIn('localízalo con Glob',prompt)
        self.assertNotIn('context:',case)

if __name__=='__main__':unittest.main()
