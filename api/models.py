from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=360)
    public = models.BooleanField(blank=False, default=True)
    sdate = models.DateField(blank=False)
    edate = models.DateField(blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.sdate > self.edate:
            return {'message': 'EndDate needs to be after StartDate'}
        else:
            super().save(*args, **kwargs)

    class Meta:
        unique_together = (('title', 'created_by'),)
        index_together = (('title', 'created_by'),)


class DailyCheck(models.Model):
    date = models.DateField(blank=False)
    done = models.BooleanField(max_length=7, default=False)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)


    class Meta:
        unique_together = (('date', 'habit'),)
        index_together = (('date', 'habit'),)
