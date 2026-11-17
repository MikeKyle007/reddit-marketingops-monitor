# Reddit Marketing Operations & MOPs Monitor (Python)

**Read-only Python proof of concept** for reviewing approved Reddit discussions. It categorizes posts into **14 topic areas** (five original areas and nine newly added areas):

| Topic | Examples of matching keywords or phrases |
| --- | --- |
| **MOPs / Marketing Operations** | MOPs, marketing operations, marketing ops, marketingops |
| **Marketo** | Marketo, Adobe Marketo Engage |
| **Marketing Automation** | Marketing automation, lead scoring, lead nurturing |
| **RevOps** | RevOps, revenue operations, revenue ops |
| **AI in Marketing** | AI agents, agentic AI, AI in marketing, LLM |
| **Marketo Migration** | Marketo migration, migrating from/to Marketo, Marketo workspace consolidation |
| **Preference Center** | Preference center/centre, subscription management, communication preferences |
| **GDPR Discussions** | GDPR, data subject access request, DSAR, lawful basis |
| **Marketing Strategy** | Marketing strategy, GTM strategy, campaign strategy, ABM strategy |
| **AI Services** | AI services, AI consulting, AI as a service, LLM consulting |
| **Martech Solutions** | Martech solutions, martech stack, marketing technology platforms |
| **Inboxing** | Inbox placement, email deliverability, sender reputation, SPF, DKIM, DMARC |
| **AI-Driven Automation & Personalization** | AI-driven automation, AI-powered personalization, predictive personalization |
| **Platform Implementation & Integration** | Marketo integration, HubSpot setup, Marketing Cloud Next, platform implementation |

Matching uses case-insensitive regular expressions. **A post may match more than one topic.** The platform implementation topic focuses on technical setup/integration for Marketo and HubSpot; the distinctive term Marketing Cloud Next is also tracked on its own. This is rule-based keyword matching, not semantic understanding, so review false positives and adjust phrases as needed.

The bot finds matching posts, prints their titles, topic labels, and URLs, and uses an automatically expiring SQLite table of post IDs to avoid reporting the same match repeatedly. **It does not post, comment, send messages, or vote.**

## Reddit API approval is required

This repository is prepared for a Reddit Data API access request. Do not use it to access Reddit's API until Reddit explicitly approves your use case and you have valid credentials. Use only subreddits and data types within your approved scope. Commercial research and business intelligence may need additional authorization.

- Responsible Builder Policy: https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy
- Reddit Data API guidance: https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki
- Reddit developer FAQ: https://developers.reddit.com/docs/guides/faq
- PRAW documentation: https://praw.readthedocs.io/en/stable/getting_started/quick_start.html

## Setup (Windows PowerShell)

1. Install Python 3.10+.
2. Clone or download this repository and open PowerShell in its folder.
3. Create the environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. Once you are approved, copy the example configuration to a private local `.env` file:

   ```powershell
   Copy-Item .env.example .env
   ```

5. Edit `.env` with your approved Reddit `client_id`, `client_secret`, a descriptive `user_agent`, and the communities you are allowed to access. **Never upload `.env` or share credentials.**
6. Run the bot:

   ```powershell
   .\.venv\Scripts\python.exe reddit_monitor.py
   ```

7. Run offline keyword tests (works without API credentials):

   ```powershell
   .\.venv\Scripts\python.exe -m unittest discover -s tests -v
   ```

## How it works

- `topics.py` contains case-insensitive regex keywords, covering all **14 research categories**, including **MOPs**, **Marketing Operations**, migrations, GDPR, and integrations.
- `reddit_monitor.py` loops through the configured communities, reads recent posts with PRAW, and tags any keyword matches.
- The local `seen_posts.db` stores only post IDs, timestamps, and category labels for deduplication, with a 48-hour automatic expiration.
- The source text stays in memory only; no usernames, bodies, or full post URLs are saved to disk by the script. Console output can contain post titles, so handle terminal logs accordingly.

**Privacy limitation:** Automatic expiration is not a complete deletion reconciliation mechanism. If you extend this prototype into a persistent production system, implement deletion/erasure reconciliation and follow every Reddit data retention and privacy condition in your approval. Avoid using Reddit content for AI model training without express authorization.

## Code layout

```text
reddit-marketingops-monitor/
├── reddit_monitor.py       # Main read-only monitoring application
├── topics.py               # Keywords and topic categorization
├── requirements.txt        # Python dependencies
├── .env.example            # Safe example config (no real credentials)
├── .gitignore              # Protect credentials and local data
├── tests/
│   └── test_topics.py      # Offline keyword tests
└── README.md               # This document
```

## Current monitoring coverage

The application checks the subreddits listed in the local `.env` setting `SUBREDDITS` (see `.env.example`). Topic labels are **keywords searched within the fetched posts**, not additional subreddits or Reddit-wide search queries. To cover more communities, explicitly add only communities within your approved Reddit API scope.

## How to add more topics

Edit `TOPIC_PATTERNS` in `topics.py`. Each regex is searched case-insensitively. Test with:

```powershell
py -m unittest discover -s tests -v
```

## API request field: source code URL

Publish this repository to GitHub, then paste your real public repository URL into Reddit's **Provide a link to source code or platform that will access the API** field. It should look like `https://github.com/YOUR_USERNAME/reddit-marketingops-monitor` (replace the placeholder with your real GitHub username).

This repository is a proof of concept, not evidence of existing Reddit approval or a tested production integration.
