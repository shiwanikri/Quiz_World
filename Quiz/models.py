from django.db import models
from django.contrib.auth.models import User

# Info about quiz
class Host(models.Model):
    Field = models.CharField(max_length=30)
    Type_of_question = models.CharField(max_length=35)
    No_of_questions = models.IntegerField()
    Duration = models.DurationField()
    Name_of_competition = models.CharField(max_length=40)
    Last_date = models.DateField()
    date = models.DateTimeField(null=True)
    # Time_of_exam = models.TimeField()
    Created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name_of_competition

# Questions for MCQ
class QuestionsMCQ(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    Question = models.CharField(max_length=300)
    Option1 = models.CharField(max_length=20)
    Option2 = models.CharField(max_length=20)
    Option3 = models.CharField(max_length=20)
    Option4 = models.CharField(max_length=20)
    correct = models.CharField(max_length=20)

    def __str__(self):
        return self.Question

# Questions for TITA
class QuestionsTITA(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    Question = models.CharField(max_length=300)

    def __str__(self):
        return self.Question

# Marks
class Marks_Of_User(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    
    def __str__(self):
        return str(self.user)
