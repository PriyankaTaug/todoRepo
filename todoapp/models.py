from django.db import models


class Todotable(models.Model):
    taskname = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.TextField(blank=True, null=True)
    userid = models.ForeignKey('UserTbl', models.DO_NOTHING, db_column='userid', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    isdelete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'todotable'


class UserTbl(models.Model):
    username = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_tbl'