import json
import tempfile
import unittest
from pathlib import Path
from tools.new_mod import create
from tools.package import package
from tools.validate import ROOT, validate, check_project


class RepositoryTests(unittest.TestCase):
    def test_existing_repository(self):
        count, issues = validate(ROOT)
        self.assertGreaterEqual(count, 1)
        self.assertEqual(issues, [])

    def test_new_feature_is_independent_and_valid(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            f = create("feature", "test-tweak", "Test Tweak", root=root)
            self.assertEqual(check_project("feature", f), [])
            project = json.loads((f / "mod.project.json").read_text())
            meta = json.loads((f / "about/metadata.json").read_text())
            self.assertEqual(meta["assemblies"], ["TestTweak.dll"])
            self.assertEqual(meta["id"], project["modId"])
            with self.assertRaises(FileExistsError):
                create("feature", "test-tweak", "Again", root=root)

    def test_packager_refuses_uncompiled_stub(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            create("character", "new-hero", "New Hero", root=root)
            with self.assertRaises(FileNotFoundError):
                package("characters/new-hero", root=root)

    def test_independent_zip_contains_only_target_mod(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            f = create("feature", "one-feature", "One Feature", root=root)
            create("feature", "other-feature", "Other Feature", root=root)
            dll = f / "src/bin/Release/netstandard2.1/OneFeature.dll"
            dll.parent.mkdir(parents=True)
            dll.write_bytes(b"fake-build-output-for-zip-test")
            from zipfile import ZipFile
            output = package("features/one-feature", root=root)
            with ZipFile(output) as archive:
                entries = archive.namelist()
            self.assertIn("one-feature/OneFeature.dll", entries)
            self.assertIn("one-feature/about/metadata.json", entries)
            self.assertFalse(any("other-feature" in path for path in entries))


if __name__ == "__main__":
    unittest.main()
