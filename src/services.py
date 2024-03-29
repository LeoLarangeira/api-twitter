from typing import Any, Dict, List
from dotenv import load_dotenv
import tweepy
import os
from src.connection import trends_collection


def _get_trends(woe_id: int, api: tweepy.API) -> List[Dict[str, Any]]:
    """Get treending topics from Twitter API.

    Args:
        woe_id (int): Identifier of location.

    Returns:
        List[Dict[str, Any]]: Trends list.
    """
    trends = api.trends_place(woe_id)

    return trends[0]["trends"]


def get_trends() -> List[Dict[str, Any]]:
    """Get treending topics persisted in MongoDB.

    Args:
        woe_id (int): Identifier of location.

    Returns:
        List[Dict[str, Any]]: Trends list.
    """
    trends = trends_collection.find({})
    return list(trends)


def save_trends() -> None:
    """Get trends topics and save on MongoDB."""
    auth = tweepy.OAuthHandler(consumer_key=os.getenv('CONSUMER_KEY'), consumer_secret=os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'),os.getenv('ACCESS_TOKEN_SECRET'))

    api = tweepy.API(auth)

    trends = _get_trends(woe_id=os.getenv('WOE_ID'), api=api)
    trends_collection.insert_many(trends)