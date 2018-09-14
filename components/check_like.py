from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from wall.models import TopicLike

MAX_TIME_OF_LIKE_LIVING = 1  # day


def check_like(user=None, topic=None):
    try:
        like = TopicLike.objects.get(creator=user, topic=topic)
        if (like.liked - datetime.now()).days <= 1:
            print(like.liked, datetime.now())
            if like.is_active:
                like.is_active = False
            else:
                like.is_active = True
            return like
        return False
    except ObjectDoesNotExist:
        like = TopicLike(creator=user, topic=topic)
        like.is_active = True
    return like
