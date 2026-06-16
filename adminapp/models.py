from django.db import models

# Create your models here.
class manage_users_model(models.Model):
    User_id = models.AutoField(primary_key = True)
    user_Profile = models.FileField(upload_to = 'images/')
    User_Email = models.EmailField(max_length = 50)
    User_Status = models.CharField(max_length = 10)
    
    class Meta:
        db_table = 'manage_users'

from django.db import models

# Create your models here.

class Upload_dataset_model(models.Model):
    user_id = models.AutoField(primary_key = True)
    Dataset = models.FileField(null=True)
    File_size = models.CharField(max_length = 100) 
    Date_Time = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'upload_dataset'

# dataset
class DATASET(models.Model):
    DS_ID = models.AutoField(primary_key = True)
    Age = models.IntegerField()
    PHYSICAL_SCORE = models.FloatField() 
    TEST_RESULTS = models.IntegerField()
    Pregnancies = models.IntegerField()
    
    class Meta:
        db_table = 'Dataset'




class ADA_ALGO(models.Model):
    ADA_ID = models.AutoField(primary_key = True)
    Accuracy = models.TextField(max_length = 100)
    Precession = models.TextField(max_length = 100) 
    F1_Score = models.TextField(max_length = 100)
    Recall = models.TextField(max_length = 100)
    Name = models.TextField(max_length = 100)
    
    class Meta:
        db_table = 'ADA_algo'

class DECISSION_ALGO(models.Model):
    DECISSION_ID = models.AutoField(primary_key = True)
    Accuracy = models.TextField(max_length = 100)
    Precession = models.TextField(max_length = 100) 
    F1_Score = models.TextField(max_length = 100)
    Recall = models.TextField(max_length = 100)
    Name = models.TextField(max_length = 100)
    
    class Meta:
        db_table = 'DECISSION_algo'

class KNN_ALGO(models.Model):
    KNN_ID = models.AutoField(primary_key = True)
    Accuracy = models.TextField(max_length = 100)
    Precession = models.TextField(max_length = 100) 
    F1_Score = models.TextField(max_length = 100)
    Recall = models.TextField(max_length = 100)
    Name = models.TextField(max_length = 100)
    
    class Meta:
        db_table = 'KNN_algo'

class SXM_ALGO(models.Model):
    SXM_ID = models.AutoField(primary_key = True)
    Accuracy = models.TextField(max_length = 100)
    Precession = models.TextField(max_length = 100) 
    F1_Score = models.TextField(max_length = 100)
    Recall = models.TextField(max_length = 100)
    Name = models.TextField(max_length = 100)
    
    class Meta:
        db_table = 'SVC_algo'

class XG_ALGO(models.Model):
    XG_ID = models.AutoField(primary_key = True)
    Accuracy = models.TextField(max_length = 100)
    Precession = models.TextField(max_length = 100) 
    F1_Score = models.TextField(max_length = 100)
    Recall = models.TextField(max_length = 100)
    Name = models.TextField(max_length = 100)
    
    class Meta:
        db_table = 'XG_algo'


class RandomForest(models.Model):
    Random_ID = models.AutoField(primary_key = True)
    Accuracy = models.TextField(max_length = 100)
    Precession = models.TextField(max_length = 100) 
    F1_Score = models.TextField(max_length = 100)
    Recall = models.TextField(max_length = 100)
    Name = models.TextField(max_length = 100)
    
    class Meta:
        db_table = 'RandomForest'

class Logistic(models.Model):
    Logistic_ID = models.AutoField(primary_key = True)
    Accuracy = models.TextField(max_length = 100)
    Precession = models.TextField(max_length = 100) 
    F1_Score = models.TextField(max_length = 100)
    Recall = models.TextField(max_length = 100)
    Name = models.TextField(max_length = 100)
    
    class Meta:
        db_table = 'Logistic'

class GradientBoosting(models.Model):
    Logistic_ID = models.AutoField(primary_key = True)
    Accuracy = models.TextField(max_length = 100)
    Precession = models.TextField(max_length = 100) 
    F1_Score = models.TextField(max_length = 100)
    Recall = models.TextField(max_length = 100)
    Name = models.TextField(max_length = 100)
    
    class Meta:
        db_table = 'Gradient'