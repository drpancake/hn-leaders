from concurrent.futures import ThreadPoolExecutor

import arrow
import requests
from bs4 import BeautifulSoup

MAX_LEADERS = 50
MAX_FEED_LENGTH = 100


def get_karma(username):
    print("--> getting karma: %s" % username)
    obj = requests.get(f"http://hn.algolia.com/api/v1/users/{username}").json()
    return (username, obj["karma"])


def get_leaders():
    print("fetching leaders")
    b = requests.get("https://news.ycombinator.com/leaders").content
    soup = BeautifulSoup(b, "html.parser")
    leaders = {}
    for i, a in enumerate(soup.select("a.hnuser")):
        rank = i + 1
        username = a.text.strip()
        karma_str = a.parent.parent.select("td")[-1].text.strip()
        karma = int(karma_str) if karma_str else None
        leaders[username] = dict(karma=karma, rank=rank)
    missing = [u for u, obj in leaders.items() if obj["karma"] is None]
    with ThreadPoolExecutor(max_workers=25) as executor:
        for username, karma in executor.map(
            lambda u: list(get_karma(u)), missing
        ):
            leaders[username]["karma"] = karma
    res = sorted(leaders.items(), key=lambda x: x[1]["karma"], reverse=True)
    return res[:MAX_LEADERS]


def get_comments(username, karma, rank):
    print(f"getting comments: {username}")
    ts = int(arrow.get().shift(days=-14).timestamp())
    url = "https://hn.algolia.com/api/v1/search_by_date"
    url += f"?tags=comment,author_{username}"
    url += f"&numericFilters=created_at_i>={ts}"
    seen_stories = set()
    hits = requests.get(url).json()["hits"]  # so first one is kept per story
    hits.reverse()
    for hit in hits:
        content = hit["comment_text"]
        story_id = hit["story_id"]
        if story_id in seen_stories:
            continue
        if len(content) < 30:
            continue
        yield dict(
            created=arrow.get(hit["created_at"]).datetime,
            created_i=hit["created_at_i"],
            author=hit["author"],
            author_karma=karma,
            author_rank=rank,
            content=content,
            story_id=story_id,
            story_title=hit["story_title"],
            comment_url="https://news.ycombinator.com/item?id=%s"
            % hit["objectID"],
            parent_url="https://news.ycombinator.com/item?id=%s"
            % hit["parent_id"],
        )
        seen_stories.add(story_id)


def get_feed():
    leaders = get_leaders()
    comments = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for arr in executor.map(
            lambda x: list(get_comments(x[0], x[1]["karma"], x[1]["rank"])),
            leaders,
        ):
            comments.extend(arr)
    comments.sort(key=lambda c: c["created_i"], reverse=True)
    return comments[:MAX_FEED_LENGTH]
