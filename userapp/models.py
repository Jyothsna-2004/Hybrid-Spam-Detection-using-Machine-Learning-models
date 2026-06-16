from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetails(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_username = models.TextField(max_length=50, null = True)
    user_email = models.TextField(max_length=50, null = True)
    user_password = models.TextField(max_length=50, null=True)
    user_contact = models.TextField(max_length=50, null = True)
    user_file = models.FileField(upload_to='images', null = True)
    user_status = models.TextField(max_length=30, default='pending', null=True)
    otp_status = models.TextField(max_length=20, default='pending')
    otp = models.IntegerField(null = True)

    user_dates = models.DateField(auto_now=True, null = True)
    Last_Login_Time = models.TimeField(null = True)
    Last_Login_Date = models.DateField(auto_now_add=True,null = True)
    No_Of_Times_Login = models.IntegerField(default = 0, null = True)
    class Meta:
        db_table = 'hearing_table'

class PredictionCount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prediction_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - Predictions: {self.prediction_count}'

class Predict_details(models.Model):
    predict_id = models.AutoField(primary_key=True)
    Field_1 = models.CharField(max_length = 60, null = True)
    Field_2 = models.CharField(max_length = 60, null = True)
    Field_3 = models.CharField(max_length = 60, null = True)
    Field_4 = models.CharField(max_length = 60, null = True)
    Field_5 = models.CharField(max_length = 60, null = True)
    Field_6 = models.CharField(max_length = 60, null = True)
    Field_7 = models.CharField(max_length = 60, null = True)
    Field_8 = models.CharField(max_length = 60, null = True)
    Field_9 = models.CharField(max_length = 60, null = True)
    Field_10 = models.CharField(max_length = 60, null = True)
    
    class Meta:
        db_table = "predict_detail"


class UserFeedbackModels(models.Model):
    feed_id = models.AutoField(primary_key=True)
    star_feedback = models.TextField(max_length=900)
    star_rating = models.IntegerField()
    star_Date = models.DateTimeField(auto_now_add=True, null=True)
    user_details = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    sentment = models.TextField(max_length=20,null=True)
    class Meta:
        db_table = 'feedback_table'



class Last_login(models.Model):
    Id = models.AutoField(primary_key = True)
    Login_Time = models.DateTimeField(auto_now = True, null = True)

    class Meta:
        db_table = "last_login"
