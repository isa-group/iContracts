from mongoengine import Document
from mongoengine import StringField, ListField

class Report(Document):
    name = StringField(max_length=100, required=True, unique=True)
    document = StringField(min_length=100)
    obligations = ListField()
    rights = ListField()
    obligations_actors = ListField()
    rights_actors = ListField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name