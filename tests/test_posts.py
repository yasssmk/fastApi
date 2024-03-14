from typing import List
from app import schema
import pytest

# CLI: pytest tests\test_posts.py --disable-warnings -v -s

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts = list(map(lambda post: schema.PostResponse(**post), res.json()))
    # print(posts)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_getone_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_unexisted_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/99999")
    assert res.status_code == 404

def test_get_one_posts(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schema.PostResponse(**res.json())
    assert post.id == test_posts[0].id
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("ABC", "content", True ),
    ("DEF", "content", False )
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json = {"title": title,"content": content, "published": published})
    created_post = schema.PostBase(**res.json())
    assert res.status_code == 201

def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json = {"title": "aaaaa","content": "bbbbbb", "published": True})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_unexisted_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/99999")
    assert res.status_code == 404