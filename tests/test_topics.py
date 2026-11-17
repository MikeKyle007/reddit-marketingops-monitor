"""Run with: python -m unittest discover -s tests -v"""
import unittest

from topics import categorize


class TopicTests(unittest.TestCase):
    def test_mops(self):
        self.assertIn("MOPs / Marketing Operations", categorize("Any MOPs best practices?"))

    def test_marketing_operations(self):
        self.assertIn("MOPs / Marketing Operations", categorize("Marketing Operations career path"))

    def test_marketing_ops(self):
        self.assertIn("MOPs / Marketing Operations", categorize("Marketing Ops lead lifecycle"))

    def test_multiple_topics(self):
        topics = categorize("MOPs teams using Marketo for lead scoring")
        self.assertIn("MOPs / Marketing Operations", topics)
        self.assertIn("Marketo", topics)
        self.assertIn("Marketing Automation", topics)

    def test_irrelevant_text(self):
        self.assertEqual([], categorize("My new keyboard is great"))


if __name__ == "__main__":
    unittest.main()
