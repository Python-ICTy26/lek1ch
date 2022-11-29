import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    user_friends = get_friends(user_id, fields=["bdate"]).items
    users_bdate: tp.List[str] = [friend.get("bdate") for friend in user_friends]
    users_bdate = [bdate for bdate in users_bdate if bdate is not None]
    users_bdate = [bdate for bdate in users_bdate if bdate.count(".") == 2]
    users_bdate: tp.List[dt.datetime] = [
        dt.datetime.strptime(bdate, "%d.%m.%Y") for bdate in users_bdate
    ]
    now = dt.datetime.now()
    friends_age_days = [(now - bd).days for bd in users_bdate]
    if len(friends_age_days) == 0:
        return None
    return statistics.median(friends_age_days) // 365.25
