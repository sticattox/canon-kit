from pathlib import Path
import shutil
import unittest

from canonkit.intake import intake_note
from canonkit.validate import validate_pack

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "examples" / "harbor-lab"


class PackTests(unittest.TestCase):
    def test_example_pack_is_valid(self) -> None:
        report = validate_pack(PACK)
        self.assertEqual(report.errors, [])

    def test_intake_verifies_readback(self) -> None:
        scratch = Path("/tmp/canonkit-harbor-test")
        if scratch.exists():
            shutil.rmtree(scratch)
        shutil.copytree(PACK, scratch)
        result = intake_note(scratch, "The mortiser chuck key walks off the bench.")
        self.assertEqual(result["write_status"], "VERIFIED")
        report = validate_pack(scratch)
        self.assertEqual(report.errors, [])


if __name__ == "__main__":
    unittest.main()
