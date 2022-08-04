from concurrent.futures import ThreadPoolExecutor
import arrow
import requests
from bs4 import BeautifulSoup

MAX_LEADERS = 50
MAX_FEED_LENGTH = 100


def get_leaders():
    print("fetching leaders")
    b = requests.get("https://news.ycombinator.com/leaders").content
    soup = BeautifulSoup(b, "html.parser")
    return [a.text.strip() for a in soup.select("a.hnuser")[:MAX_LEADERS]]


def get_comments(username):
    print(f"getting comments: {username}")
    ts = int(arrow.get().shift(days=-14).timestamp())
    url = "https://hn.algolia.com/api/v1/search_by_date"
    url += f"?tags=comment,author_{username}"
    url += f"&numericFilters=created_at_i>={ts}"
    for hit in requests.get(url).json()["hits"]:
        content = hit["comment_text"]
        if len(content) < 50:
            continue
        yield dict(
            created=arrow.get(hit["created_at"]).datetime,
            created_i=hit["created_at_i"],
            author=hit["author"],
            content=content,
            story_id=hit["story_id"],
            story_title=hit["story_title"],
            story_url=hit["story_url"],
            comment_url="https://news.ycombinator.com/item?id=%s"
            % hit["objectID"],
            parent_url="https://news.ycombinator.com/item?id=%s"
            % hit["parent_id"],
        )


def get_feed():
    usernames = get_leaders()
    comments = []

    # # TODO
    # usernames = usernames[:5]

    with ThreadPoolExecutor(max_workers=20) as executor:
        for arr in executor.map(lambda u: list(get_comments(u)), usernames):
            comments.extend(arr)

    comments.sort(key=lambda c: c["created_i"], reverse=True)
    return comments[:MAX_FEED_LENGTH]
