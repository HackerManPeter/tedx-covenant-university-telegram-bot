import os

from dotenv import load_dotenv

from pymongo import MongoClient

load_dotenv()
CONNECTION_STRING = os.environ["CONNECTION_STRING"]

client = MongoClient(CONNECTION_STRING)

db = client.get_default_database()
leader_board = db.leaderboard
bot_users = db.botUsers


def __check_kwargs(**kwargs) -> tuple:
    """
    Validated keyword arguments
    """
    if kwargs["username"]:
        username = kwargs["username"]
    else:
        username = None

    if kwargs["last_name"]:
        last_name = kwargs["last_name"]
    else:
        last_name = None

    first_name = kwargs["first_name"]

    return username, first_name, last_name


def insert_new_participant(id: int, **kwargs) -> None:
    """
    Adds a participant to the leaderboard
    """
    username, first_name, last_name = __check_kwargs(**kwargs)
    try:
        leader_board.insert_one(
            {
                "_id": str(id),
                "username": f"{username}",
                "first_name": f"{first_name}",
                "last_name": f"{last_name}",
                "referrals": [],
            }
        )
    except:
        return


def insert_new_user(id: int, **kwargs) -> None:
    """
    Adds user to the database
    """
    username, first_name, last_name = __check_kwargs(**kwargs)
    try:
        bot_users.insert_one(
            {
                "_id": str(id),
                "username": f"{username}",
                "first_name": f"{first_name}",
                "last_name": f"{last_name}",
            }
        )
    except:
        return


def update_referral(referrer_string: str, user_id: int) -> None:
    """
    Updates the leader board
    """
    referrer_id = referrer_string.split("_")[-2]

    # Checks if the user is trying to refer themself
    if int(referrer_id) == user_id:
        return

    # Checks if the user has already been referred by someone else
    if leader_board.count_documents({"referrals": f"{user_id}"}) > 0:
        return

    # Checks if the user already has a referral link
    if leader_board.count_documents({"_id": f"{user_id}"}) > 0:
        return

    # Update leader board
    leader_board.update_one(
        {"_id": referrer_id}, {"$push": {"referrals": str(user_id)}}
    )


def get_ids():
    """
    Get's the telegram Id's for all bot users
    """
    all_users = bot_users.find({})
    return [user["_id"] for user in all_users]
