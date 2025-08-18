from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
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
    messages = models.TextField()
    created_at = models.DateTimeField()
    who=models.CharField(max_length=10, choices=WHO_CHOICES)

    class Meta:
        managed = False
        db_table = 'conversations'  # Ensure this matches your MySQL table

class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.TextField()
    password=models.TextField()
    whatsapp_phone_id=models.TextField()
    whatsapp_token=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    display_phone_no=models.TextField()
    
    class Meta:
        managed=False
        db_table='admins'
# Create your models here.
