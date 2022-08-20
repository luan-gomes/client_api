from rest_framework import serializers
from client_api.models import Address, BankAccount, Client


class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Address
        fields = ['id', 'address', 'number', 'zip_code', 'city', 'state', 'country']


class BankAccountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = BankAccount
        fields = ['id', 'agency', 'account_number', 'bank']


class ClientSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    bank_accounts = BankAccountSerializer(many=True)

    class Meta:
        model = Client
        fields = [
            'id', 'company_name', 'phone', 'address',
            'registration_date', 'declared_billing', 'bank_accounts'
        ]

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        bank_accounts_data = validated_data.pop('bank_accounts')

        address_obj = Address.objects.create(**address_data)
        client = Client.objects.create(**validated_data, address=address_obj)
        for bank_account_data in bank_accounts_data:
            BankAccount.objects.create(**bank_account_data, client=client)

        return client

    def update(self, instance, validated_data):
        # Updating the address
        address_data = validated_data.pop('address')
        try:
            address_data_id = address_data['id']
        except KeyError:
            address_data_id = None

        if address_data_id == instance.address.id:
            instance.address.address = address_data.get('address', instance.address.address)
            instance.address.number = address_data.get('number', instance.address.number)
            instance.address.zip_code = address_data.get('zip_code', instance.address.zip_code)
            instance.address.city = address_data.get('city', instance.address.city)
            instance.address.state = address_data.get('address', instance.address.state)
            instance.address.country = address_data.get('address', instance.address.country)
        else:
            old_address = instance.address
            new_address = Address.objects.create(**address_data)
            instance.address = new_address
            instance.save()
            old_address.delete()

        # Updating the bank accounts
        bank_accounts_data = validated_data.pop('bank_accounts')
        keep_bank_accounts = []
        for bank_account_data in bank_accounts_data:
            if 'id' in bank_account_data.keys():
                try:
                    bank_account_obj = BankAccount.objects.get(pk=bank_account_data['id'])
                except BankAccount.DoesNotExist:
                    bank_account_obj = None
                if bank_account_obj:
                    bank_account_obj.agency = bank_account_data.get('agency', bank_account_obj.agency)
                    bank_account_obj.account_number = bank_account_data.get(
                        'account_number', bank_account_obj.account_number
                    )
                    bank_account_obj.bank = bank_account_data.get('bank', bank_account_obj.bank)
                    bank_account_obj.save()
                    keep_bank_accounts.append(bank_account_obj.id)
            else:
                new_bank_account = BankAccount.objects.create(**bank_account_data, client=instance)
                keep_bank_accounts.append(new_bank_account.id)
        for existing_account in instance.bank_accounts.all():
            if existing_account.id not in keep_bank_accounts:
                existing_account.delete()

        # Updating client
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.registration_date = validated_data.get('registration_date', instance.registration_date)
        instance.declared_billing = validated_data.get('declared_billing', instance.declared_billing)
        instance.save()

        return instance
