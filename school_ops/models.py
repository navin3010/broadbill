from django.db import models


class Groups(models.Model):
    name = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = "school_groups"

class Subjects(models.Model):
    title = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = "school_subjects"

class Teachers(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = "school_teachers"

class Students(models.Model):
    first_name = models.CharField(max_length=522)
    last_name = models.CharField(max_length=522)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = "school_students"

class Marks(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    mark = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = "school_marks"


