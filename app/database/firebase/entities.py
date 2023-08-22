from fireo.models import Model
from fireo.fields import TextField


class User(Model):
    username = TextField()
    password = TextField()