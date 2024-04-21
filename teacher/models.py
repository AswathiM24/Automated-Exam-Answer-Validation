from django.db import models
from django.db.models import Max


class Teacher(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    admin_code = models.CharField(max_length=200, default="EXAM-Controller")

    def __str__(self):
        return self.name


class Paper(models.Model):
    paper_code = models.CharField(max_length=200)
    std = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.paper_code


# Create your models here.
class Questions(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=2000)
    std = models.CharField(max_length=200)
    paper_code = models.ForeignKey(Paper, on_delete=models.CASCADE)
    question_num = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:
            # If the instance is new, get the maximum question_num for the paper_code
            max_question_num = Questions.objects.filter(paper_code=self.paper_code).aggregate(Max('question_num'))[
                'question_num__max']
            if max_question_num is None:
                # If this is the first question for the paper_code, start from 1
                self.question_num = 1
            else:
                # Otherwise, increment the max question_num by 1
                self.question_num = max_question_num + 1
        super(Questions, self).save(*args, **kwargs)

    def __str__(self):
        return self.question