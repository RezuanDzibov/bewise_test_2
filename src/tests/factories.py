import factory
from faker import Faker

from models import User, AudioTrack

fake = Faker()


def slugify(name: str) -> str:
    return name.replace(" ", "_").lower()



class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda obj: slugify(fake.name()))


class AudioTrackFactory(factory.Factory):
    class Meta:
        model = AudioTrack
