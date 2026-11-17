# Reddit Marketing Operations & MOPs Monitor (Python)

**Read-only Python proof of concept** for reviewing approved Reddit discussions about:

- **MOPs / Marketing Operations**: `MOPs`, `marketing operations`, `marketing ops`, `marketing operation`, `marketingops`
- **Marketo**: `Marketo`, `Adobe Marketo Engage`
- **Marketing Automation**: `marketing automation`, `lead scoring`, `lead nurturing`, `nurture campaign`
- **RevOps**: `RevOps`, `revenue operations`, `revenue ops`
- **AI in Marketing**: `AI agents`, `agentic AI`, `AI in marketing`, `marketing AI`, `LLM`

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

- `topics.py` contains case-insensitive regex keywords, including **MOPs** and **Marketing Operations**.
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

## How to add more topics

Edit `TOPIC_PATTERNS` in `topics.py`. Each regex is searched case-insensitively. Test with:

```powershell
py -m unittest discover -s tests -v
```

## API request field: source code URL

Publish this repository to GitHub, then paste your real public repository URL into Reddit's **Provide a link to source code or platform that will access the API** field. It should look like `https://github.com/YOUR_USERNAME/reddit-marketingops-monitor` (replace the placeholder with your real GitHub username).

This repository is a proof of concept, not evidence of existing Reddit approval or a tested production integration.
