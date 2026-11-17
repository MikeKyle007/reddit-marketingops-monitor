"""Read-only Reddit monitoring bot for MOPs, Marketing Operations, and related topics.

Requires Reddit Data API authorization. Does not post, reply, DM, or vote.
Stores only post IDs and aggregate topic labels for short-term deduplication.
"""
from __future__ import annotations

import os
import sqlite3
import sys
import time
from pathlib import Path

import praw
from dotenv import load_dotenv
from prawcore.exceptions import PrawcoreException

from topics import categorize

load_dotenv(Path(__file__).with_name(".env"))

DEFAULT_SUBREDDITS = "marketingops,MarketingAutomation,marketo,revops"
DATABASE = Path(__file__).with_name("seen_posts.db")
RETENTION_SECONDS = 48 * 60 * 60


def reddit_client() -> praw.Reddit:
    credentials = {
        "REDDIT_CLIENT_ID": os.getenv("REDDIT_CLIENT_ID", "").strip(),
        "REDDIT_CLIENT_SECRET": os.getenv("REDDIT_CLIENT_SECRET", "").strip(),
        "REDDIT_USER_AGENT": os.getenv("REDDIT_USER_AGENT", "").strip(),
    }
    missing = [name for name, value in credentials.items() if not value]
    if missing:
        raise ValueError(
            "Missing credentials in .env: " + ", ".join(missing)
            + ". Copy .env.example to .env and fill it after API approval."
        )

    return praw.Reddit(
        client_id=credentials["REDDIT_CLIENT_ID"],
        client_secret=credentials["REDDIT_CLIENT_SECRET"],
        user_agent=credentials["REDDIT_USER_AGENT"],
        # This three-field configuration is always read-only.
    )


def requested_subreddits() -> list[str]:
    # Only use communities approved for your app and relevant to your scope.
    raw = os.getenv("SUBREDDITS", DEFAULT_SUBREDDITS)
    return [name.strip().removeprefix("r/") for name in raw.split(",") if name.strip()]


def post_limit() -> int:
    value = int(os.getenv("POSTS_PER_SUBREDDIT", "25"))
    if not 1 <= value <= 100:
        raise ValueError("POSTS_PER_SUBREDDIT must be from 1 to 100")
    return value


def open_database() -> sqlite3.Connection:
    db = sqlite3.connect(DATABASE)
    db.execute(
        "CREATE TABLE IF NOT EXISTS seen_posts ("
        "post_id TEXT PRIMARY KEY, seen_at INTEGER NOT NULL, topics TEXT NOT NULL)"
    )
    # Expiration is not a substitute for Reddit's deletion and privacy obligations.
    db.execute(
        "DELETE FROM seen_posts WHERE seen_at < ?",
        (int(time.time()) - RETENTION_SECONDS,),
    )
    db.commit()
    return db


def scan() -> None:
    reddit = reddit_client()
    limit = post_limit()
    print("Read-only mode:", reddit.read_only)
    print("Topics include: MOPs, Marketing Operations, Marketing Ops, Marketo, RevOps, AI")

    total_checked = 0
    new_matches = 0
    with open_database() as db:
        for community in requested_subreddits():
            print(f"\nChecking r/{community} ...")
            try:
                for post in reddit.subreddit(community).new(limit=limit):
                    total_checked += 1
                    # Read API content in memory; do not persist text or usernames.
                    text = f"{post.title}\n{post.selftext}"
                    topics = categorize(text)
                    if not topics:
                        continue
                    if db.execute(
                        "SELECT 1 FROM seen_posts WHERE post_id = ?", (post.id,)
                    ).fetchone():
                        continue

                    print(f"\n  Title: {post.title}")
                    print(f"  Topics: {', '.join(topics)}")
                    print(f"  Link: https://www.reddit.com{post.permalink}")
                    db.execute(
                        "INSERT OR IGNORE INTO seen_posts (post_id, seen_at, topics) "
                        "VALUES (?, ?, ?)",
                        (post.id, int(time.time()), ", ".join(topics)),
                    )
                    new_matches += 1
                db.commit()
            except (PrawcoreException, Exception) as exc:
                # A bad subreddit or temporary API error should not abort other communities.
                print(f"Could not read r/{community}: {type(exc).__name__}: {exc}", file=sys.stderr)

    print(f"\nFinished. Checked {total_checked} posts; found {new_matches} new matching posts.")


if __name__ == "__main__":
    try:
        scan()
    except (ValueError, sqlite3.Error) as exc:
        print(f"Configuration or local database error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
