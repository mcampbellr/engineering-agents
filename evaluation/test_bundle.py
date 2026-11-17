"""Mechanical integration checks; these do not measure auditor quality."""
import copy
import importlib.util
import json
import tempfile
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
BUILD=load('bundle_builder',ROOT/'scripts/build.py')
PROBES=load('bundle_probes',ROOT/'evaluation/schema_invariants.py')

class Integration(unittest.TestCase):
    def setUp(self):self.catalog=json.loads((ROOT/'catalog.json').read_text())
    def test_deployment_preserves_custom_instructions_and_is_idempotent(self):
        deploy=load('local_deployer',ROOT/'scripts/deploy_local.py')
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp)
            legacy=home/'.claude/skills/ai-audit';legacy.mkdir(parents=True)
            (legacy/'SKILL.md').write_text('old local workflow')
            policy=home/'.claude/CLAUDE.md';policy.write_text('existing custom instructions\n')
            agents=home/'.claude/agents';agents.mkdir()
            (agents/'code-review.md').write_text('retired reviewer')
            (agents/'other-agent.md').write_text('unrelated reviewer')
            state=deploy.plan(ROOT,home);result=deploy.apply(state,home)
            self.assertTrue(result['changed']);self.assertTrue(Path(result['backup_root']).exists())
            self.assertTrue(policy.read_text().startswith('existing custom instructions'))
            self.assertFalse(legacy.exists())
            self.assertFalse((agents/'code-review.md').exists())
            self.assertEqual((agents/'other-agent.md').read_text(),'unrelated reviewer')
            self.assertEqual((home/'.codex/skills/ai-audit').resolve(),(ROOT/'skills/ai-audit').resolve())
            second=deploy.apply(deploy.plan(ROOT,home),home)
            self.assertEqual(second['changed'],[])
    def test_policy_symlink_target_changes_invalidate_plan_fingerprint(self):
        deploy=load('policy_deployer',ROOT/'scripts/deploy_local.py')
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'real.md';target.write_text('first')
            alias=Path(temp)/'alias.md';alias.symlink_to(target)
            before=deploy.fingerprint(alias);target.write_text('second')
            self.assertNotEqual(before,deploy.fingerprint(alias))
    def test_twelve_unique_discoverable_skills(self):
        names=[r['name'] for r in self.catalog['roles']]+[r['name'] for r in self.catalog['bundled_skills']]
        self.assertEqual(len(names),12);self.assertEqual(len(set(names)),12)
        self.assertEqual({p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')},set(names))
    def test_imported_reference_and_asset_bytes_preserved(self):
        for role in self.catalog['bundled_skills']:
            for path in (ROOT/role['source']).rglob('*'):
                if not path.is_file() or path.name=='SKILL.md' or 'agents' in path.relative_to(ROOT/role['source']).parts:continue
                target=ROOT/'skills'/role['name']/path.relative_to(ROOT/role['source'])
                self.assertEqual(path.read_bytes(),target.read_bytes(),str(path))
    def test_each_skill_has_output_schema_validator_and_dependencies(self):
        for path in (ROOT/'skills').iterdir():
            for name in ['references/output-contract.md','references/report.schema.json','scripts/validate_report.py','requirements-validation.txt','references/skill-routing.md']:
                self.assertTrue((path/name).is_file(),str(path/name))
    def test_native_agents_inherit_and_have_unique_names(self):
        names=[]
        for path in (ROOT/'agents').glob('*.md'):
            text=path.read_text();header=text.split('---',2)[1]
            name=next(ln.split(':',1)[1].strip() for ln in header.splitlines() if ln.startswith('name:'))
            names.append(name);self.assertEqual(path.stem,name)
            self.assertNotIn('model: cheap',header);self.assertNotIn('model: mid',header);self.assertNotIn('model: frontier',header)
        self.assertEqual(len(names),25);self.assertEqual(len(set(names)),25)
    def test_only_new_package_entries_are_distributed(self):
        repo=ROOT.parents[1]
        if not (repo/'.git').exists():
            self.skipTest('Legacy aliases belong to the dotfiles source checkout, not the standalone plugin')
        for role in self.catalog['bundled_skills']:
            alias=repo/'claude/.claude/skills'/role['name']
            self.assertFalse(alias.exists() or alias.is_symlink(),str(alias))
        for role in self.catalog['roles']+self.catalog['bundled_skills']:
            alias=repo/'codex/.codex/skills'/role['name']
            self.assertTrue(alias.is_symlink(),str(alias))
            self.assertEqual(alias.resolve(),(ROOT/'skills'/role['name']).resolve())
    def test_missing_imported_reference_fails_build_instead_of_silent_omission(self):
        bad=copy.deepcopy(self.catalog);bad['bundled_skills'][0]['source']='source-skills/not-present'
        with self.assertRaises(ValueError):BUILD.bundled_outputs(bad,set())
    def test_common_envelope_keeps_legacy_detail_without_fake_metrics(self):
        from jsonschema import Draft202012Validator
        schema=json.loads((ROOT/'core/report.schema.json').read_text())
        report=copy.deepcopy(PROBES.VALID)
        report['domain']={'scores':{'overall':73,'kind':'rubric-derived'},'original_verdict':'REQUIRES CHANGES'}
        Draft202012Validator(schema).validate(report)
        self.assertIsNone(report['metrics'][0]['value'])
    def test_resolved_findings_do_not_force_pre_fix_verdict(self):
        from jsonschema import Draft202012Validator
        validator=Draft202012Validator(json.loads((ROOT/'core/report.schema.json').read_text()))
        report=copy.deepcopy(PROBES.VALID);report['findings'][0]['status']='fixed';report['verdict']='no_blocking_findings'
        validator.validate(report)
        report['verdict']='requires_changes';self.assertTrue(list(validator.iter_errors(report)))
        report['findings'][0]['status']='open';report['verdict']='no_blocking_findings';self.assertTrue(list(validator.iter_errors(report)))

if __name__=='__main__':unittest.main()
