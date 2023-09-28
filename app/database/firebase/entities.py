from fireo.fields import TextField
from fireo.models import Model


class FireUser(Model):
    username = TextField()
    password = TextField()
