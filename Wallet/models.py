from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Wallet(models.Model):
    balance = models.FloatField()
    number = models.CharField(max_length=15, unique=True)
    date_opened = models.DateTimeField()
    date_closed = models.DateTimeField(null=True)
    pay_limit = models.FloatField()

    def __unicode__(self):
        return str(self.id)


class Client(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=13)
    phone_verified = models.BooleanField(default=False)
    client_wallet = models.OneToOneField(Wallet, null=True)
    user_id = models.OneToOneField(User)

    def __unicode__(self):
        return self.name

    def set_user_id(self, user):
        self.user_id = user


class Transaction(models.Model):
    title = models.CharField(max_length=20)
    from_user = models.ForeignKey(Client)
    to_wallet = models.ForeignKey(Wallet)
    money = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    #is_closed = models.BooleanField(default=False)
    #message = models.CharField(max_length=140)
    def __unicode__(self):
        result = self.title + " from " + self.from_user.client_wallet.number + " to " + self.to_wallet.number + "; amount: " + str(self.money) + " nuts was sent "+ " at " + \
                 str(self.end_time)
        return result


class Session(models.Model):
    ip_address = models.IPAddressField()
    user = models.ForeignKey(Client)

class Confirmation(models.Model):
    title = models.CharField(max_length=20)
    client = models.ForeignKey(Client)
    transaction = models.ForeignKey(Transaction)
    confirm_code = models.CharField(max_length=6)
    conf_date = models.DateTimeField()
    confirmed = models.BooleanField(default=False)
    #failed = models.BooleanField(default=False)