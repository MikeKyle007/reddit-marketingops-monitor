"""Run with: python -m unittest discover -s tests -v"""
import unittest

from topics import TOPIC_PATTERNS, categorize


class TopicTests(unittest.TestCase):
    def test_existing_topics(self):
        examples = {
            "MOPs / Marketing Operations": [
                "Any MOPs best practices?",
                "Marketing Operations career path",
                "Marketing Ops lead lifecycle",
            ],
            "Marketo": ["Marketo tokens", "Adobe Marketo Engage tips"],
            "Marketing Automation": ["Automating lead scoring"],
            "RevOps": ["RevOps process", "Revenue Operations org"],
            "AI in Marketing": ["AI agents for email", "AI in Marketing"],
        }
        for topic, phrases in examples.items():
            for phrase in phrases:
                with self.subTest(topic=topic, phrase=phrase):
                    self.assertIn(topic, categorize(phrase))

    def test_new_topics(self):
        examples = {
            "Marketo Migration": [
                "Marketo migration planning",
                "Migrating from Marketo to HubSpot",
                "How to consolidate Marketo workspaces?",
            ],
            "Preference Center": [
                "Build an email preference center",
                "Subscription management best practices",
                "Communication preferences form",
            ],
            "GDPR Discussions": [
                "GDPR compliance questions",
                "Data subject access request process",
                "Handling a DSAR",
            ],
            "Marketing Strategy": [
                "Marketing Strategy review",
                "GTM strategy discussion",
                "Campaign strategy for B2B",
            ],
            "AI Services": [
                "AI services for marketing teams",
                "Finding an AI consulting agency",
                "AI as a service options",
            ],
            "Martech Solutions": [
                "Martech Solutions for B2B",
                "How should we evaluate our martech stack?",
                "Marketing technology platforms comparison",
            ],
            "Inboxing": [
                "Email deliverability suddenly dropped",
                "Inbox placement with Gmail",
                "DKIM authentication configuration",
            ],
            "AI-Driven Automation & Personalization": [
                "AI-driven automation for campaigns",
                "AI-powered personalization at scale",
                "Predictive personalization ideas",
            ],
            "Platform Implementation & Integration": [
                "Marketo Salesforce integration troubleshooting",
                "How do I set up HubSpot?",
                "Marketing Cloud Next implementation",
                "Integrating HubSpot with Salesforce",
            ],
        }
        for topic, phrases in examples.items():
            for phrase in phrases:
                with self.subTest(topic=topic, phrase=phrase):
                    self.assertIn(topic, categorize(phrase))

    def test_multiple_topics(self):
        topics = categorize("MOPs teams using Marketo for lead scoring and GDPR")
        self.assertIn("MOPs / Marketing Operations", topics)
        self.assertIn("Marketo", topics)
        self.assertIn("Marketing Automation", topics)
        self.assertIn("GDPR Discussions", topics)

    def test_no_overbroad_integration_matches(self):
        self.assertNotIn(
            "Platform Implementation & Integration",
            categorize("We enjoy using Marketo every day"),
        )

    def test_irrelevant_text(self):
        self.assertEqual([], categorize("My new keyboard is great"))

    def test_expected_topic_count(self):
        self.assertEqual(14, len(TOPIC_PATTERNS))


if __name__ == "__main__":
    unittest.main()
