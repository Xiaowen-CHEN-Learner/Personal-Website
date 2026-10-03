import contextlib
import io
import unittest
from unittest.mock import patch
from tools.finish_github_setup import OWNER, PROFILE, check_owner, merged_topics, optional_get, preview, apply


class ProfileSetupTests(unittest.TestCase):
    def test_correct_account(self):
        check_owner({"login": OWNER.lower()})

    def test_wrong_account_stops(self):
        with self.assertRaises(RuntimeError):
            check_owner({"login": "someone-else"})

    def test_topics_are_additive(self):
        self.assertEqual(merged_topics(["existing"], ["python"]), ["existing", "python"])

    def test_duplicate_topics_removed(self):
        self.assertEqual(merged_topics(["python"], ["python"]), ["python"])

    def test_topic_limit(self):
        with self.assertRaises(ValueError):
            merged_topics([f"topic-{i}" for i in range(20)], ["new"])

    def test_invalid_topic(self):
        with self.assertRaises(ValueError):
            merged_topics([], ["Invalid Topic"])

    def test_bio_fits(self):
        self.assertLessEqual(len(PROFILE["bio"]), 160)

    def test_no_email_or_photo_publication(self):
        self.assertNotIn("email", PROFILE)
        self.assertNotIn("avatar_url", PROFILE)

    def test_preview_has_no_network(self):
        with patch("tools.finish_github_setup.api") as api, contextlib.redirect_stdout(io.StringIO()):
            preview()
        api.assert_not_called()

    def test_only_404_is_missing(self):
        with patch("tools.finish_github_setup.api", side_effect=RuntimeError("gh: Not Found (HTTP 404)")):
            self.assertIsNone(optional_get("test"))
        with patch("tools.finish_github_setup.api", side_effect=RuntimeError("HTTP 403")), self.assertRaises(RuntimeError):
            optional_get("test")

    def test_missing_cli_stops_before_network(self):
        with patch("tools.finish_github_setup.shutil.which", return_value=None), patch("tools.finish_github_setup.api") as api, self.assertRaises(RuntimeError):
            apply()
        api.assert_not_called()


if __name__ == "__main__":
    unittest.main()
