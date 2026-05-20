import unittest


class PackageImportTests(unittest.TestCase):
    def test_package_exposes_version(self):
        import rk1126b_assistant

        self.assertEqual(rk1126b_assistant.__version__, "0.1.0")


if __name__ == "__main__":
    unittest.main()
