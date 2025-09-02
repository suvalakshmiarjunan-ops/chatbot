from django.db import models

class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.TextField()
    password=models.TextField()
    whatsapp_phone_id=models.TextField()
    whatsapp_token=models.TextField()
    pinecone_token=models.TextField()
    # openai_api_key = models.TextField()  # New field to store API key
    created_at=models.DateTimeField(auto_now_add=True)
    display_phone_no=models.TextField()
    goolgle_calendar=models.TextField()
    
    
    class Meta:
        managed=False
        db_table='admins'

class User(models.Model):
    id = models.AutoField(primary_key=True)
    admin_id=models.ForeignKey(Admin,on_delete=models.DO_NOTHING,db_column='admin_id')
    name = models.CharField(max_length=100)
    phone_no= models.CharField(max_length=20)
    created_at = models.DateTimeField()

    class Meta:
        managed = False  # This tells Django: don't create or modify this table
        db_table = 'users'  # Must exactly match your phpMyAdmin table name

class Message(models.Model):
    WHO_CHOICES=[
        ('user','User'),
        ('bot','Bot')
    ]
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    # user_id = models.ForeignKey('newapp.User', on_delete=models.DO_NOTHING, db_column='user_id')
    messages = models.TextField()
    created_at = models.DateTimeField()
    who=models.CharField(max_length=10, choices=WHO_CHOICES)

    class Meta:
        managed = False
        db_table = 'conversations'  # Ensure this matches your MySQL table


# Create your models here.
# models.py (add these below your existing models)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tags'  # You can create this new table via migrations later


class UserTag(models.Model):
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey('newapp.User', on_delete=models.CASCADE, db_column='user_id')
    # tag = models.ForeignKey('newapp.Tag', on_delete=models.CASCADE, db_column='tag_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='tag_id')

    class Meta:
        db_table = 'user_tags'  # New table for user-tag relationships
        unique_together = ('user', 'tag')  # prevent duplicate mappings

# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     admin_id = models.ForeignKey(Admin, on_delete=models.DO_NOTHING, db_column='admin_id')
#     name = models.CharField(max_length=100)
#     phone_no = models.CharField(max_length=20)
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'users'

#     def __str__(self):
#         return f"{self.name} ({self.phone_no})"
     
