from django.db import models


class Address(models.Model):
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return (self.address + ', ' + self.number + ', ' +
                self.zip_code + ', ' + self.city + ', ' +
                self.state + ', ' + self.country)


class Client(models.Model):
    company_name = models.CharField(max_length=115)
    phone = models.CharField(max_length=15)
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='client'
    )
    registration_date = models.DateField()
    declared_billing = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.company_name


class BankAccount(models.Model):
    agency = models.CharField(max_length=15)
    account_number = models.CharField(max_length=15)
    bank = models.CharField(max_length=150)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='bank_accounts'
    )

    def __str__(self):
        return 'AG: ' + self.agency + ' / Account: ' + self.account_number

