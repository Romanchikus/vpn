from sites.models import Site
from user.models import User


import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")


def get_admin_user() -> User:
    return User.objects.filter(
        username="admin", is_superuser=True, is_staff=True
    ).first()


def run():

    admin = get_admin_user()
    url = "https://zaxid.net/"
    zaxid, was_created = Site.objects.get_or_create(
        url=url, name="zaxid", defaults={"creator": admin}
    )
    print(zaxid.id)
