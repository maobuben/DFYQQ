import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import installer
import snowluma
from store import State


class SnowLumaTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_account(self, qq):
        path = snowluma.account_path(self.root, qq)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"networks": {"wsClients": []}}), encoding="utf-8")

    def test_detect_account_excludes_owner_and_prefers_known(self):
        self.write_account("111111")
        self.write_account("222222")
        self.write_account("333333")
        found = snowluma.detect_account(self.root, owner_qq="111111")
        self.assertIsNone(found["qq"])
        self.assertEqual(found["candidates"], ["222222", "333333"])
        found = snowluma.detect_account(self.root, owner_qq="111111", known_qq="333333")
        self.assertEqual(found["qq"], "333333")

    def test_login_state_waits_for_desktop_qq_login(self):
        with mock.patch.object(snowluma, "connected_to_astrbot", return_value=False), \
             mock.patch.object(snowluma, "desktop_qq_path", return_value=Path("C:/QQ/QQ.exe")), \
             mock.patch.object(snowluma, "desktop_qq_running", return_value=True):
            state = snowluma.login_state(self.root, 6199, running=True)
            self.assertEqual(state["status"], "need_scan")
            self.write_account("222222")
            state = snowluma.login_state(self.root, 6199, running=True)
            self.assertEqual(state["status"], "scanned")
            self.assertEqual(state["account"], "222222")
            with mock.patch.object(snowluma, "connected_to_astrbot", return_value=True):
                self.assertEqual(snowluma.login_state(self.root, 6199, running=True)["status"], "online")
        self.assertEqual(snowluma.login_state(self.root, 6199, running=False)["status"], "starting")

    def test_ensure_installed_accepts_a_local_official_zip(self):
        archive = self.root / snowluma.ASSET
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("index.mjs", "console.log('snowluma')")
            z.writestr("node.exe", b"MZ")
            z.writestr("EULA.md", "个人使用")
        with mock.patch.object(snowluma, "SHA256", ""):
            base = snowluma.ensure_installed(self.root, None)
        self.assertEqual(base, self.root / "snowluma")
        self.assertTrue((base / "index.mjs").is_file())
        self.assertTrue(snowluma.installed(self.root))
        self.assertTrue(snowluma.eula_path(self.root).name == "EULA.md")

    def test_desktop_qq_probe_is_cached(self):
        exe = self.root / "QQ.exe"
        exe.write_bytes(b"MZ")
        snowluma._QQ_CACHE.update(path_at=0.0, path=None, run_at=0.0, running=False)
        with mock.patch.object(snowluma, "_registry_qq_paths", return_value=[exe]) as registry:
            self.assertEqual(snowluma.desktop_qq_path(), exe)
            self.assertEqual(snowluma.desktop_qq_path(), exe)
            self.assertEqual(registry.call_count, 1)
        fake = mock.Mock(stdout=b'"QQ.exe","1234"\n')
        with mock.patch.object(snowluma.subprocess, "run", return_value=fake) as run:
            self.assertTrue(snowluma.desktop_qq_running())
            self.assertTrue(snowluma.desktop_qq_running())
            self.assertEqual(run.call_count, 1)

    def test_progress_step_names_the_selected_protocol(self):
        state = State.load(self.root)
        state.data["platform"] = "snowluma"
        inst = installer.Installer(self.root, state, resume=False)
        titles = {step["key"]: step["title"] for step in inst.progress()["steps"]}
        self.assertIn("SnowLuma", titles["protocol"])
        state.data["platform"] = "napcat"
        titles = {step["key"]: step["title"] for step in inst.progress()["steps"]}
        self.assertIn("NapCat", titles["protocol"])

    def test_zip_path_traversal_is_rejected(self):
        archive = self.root / snowluma.ASSET
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("../evil.txt", "x")
        with mock.patch.object(snowluma, "SHA256", ""):
            with self.assertRaises(snowluma.SnowLumaError):
                snowluma.ensure_installed(self.root, None)


if __name__ == "__main__":
    unittest.main()
