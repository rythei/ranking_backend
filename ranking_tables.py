#table for gathering peer rankings:
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
import select2.fields
import select2.models
import pickle
from phonenumber_field.modelfields import PhoneNumberField
import trueskill

class PeerRanks(models.Model):
    competition = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    ranks = ListField()

class PlayerSkills(models.Model):
    user = models.OneToOneField(SparkUser, on_delete=models.CASCADE)
    subskill = models.OneToOneField(Skill, on_delete=models.CASCADE)
    skill = models.CharField()
    mu = models.FloatField(null=True)
    sigma = models.FloatField(null=True)
    #### note: a player's rating will be (mu - 3*sigma)

#creates a ListField datatype to be used for the "ranks" attribute in PeerRanks
class ListField(models.TextField, metaclass=models.SubfieldBase):
    description = "ListField store List of element"

    SPLIT_CHAR= ';'

    def __init__(self, *args, list_choices=None, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
        if list_choices is None:
            list_choices = []
        self.list_choices = list_choices

    def to_python(self, value):
        res = []
        if value is None:
            res = []

        if isinstance(value, list):
            res = value

        if isinstance(value, builtins.str):
            res = value.split(self.SPLIT_CHAR)
        try:
            if "[" in value and "]" in value:
                res = eval(value)
        except:
            pass
        return res

    def get_prep_value(self, value):
        if value is None or value == "":
            return None
        res = self.SPLIT_CHAR.join(value)
        return res

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        return forms.MultipleChoiceField(choices=self.list_choices)
