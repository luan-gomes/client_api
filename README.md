# client_api

This is a Rest API to manage the clients of BHub. The project was built using [Django](https://docs.djangoproject.com/en/4.0/) and [Django Rest Framework](https://www.django-rest-framework.org/).
The project is hosted at Heroku. And you can make yours requests using the following URL: https://bhub-client-api.herokuapp.com/clients/. 

## Documentation

The API's documentation is available [here](https://bhub-client-api.herokuapp.com/swagger/) and it was created using [Swagger](https://swagger.io/).

## Tests

#### Functional tests

You can make functional tests of this API sending request to https://bhub-client-api.herokuapp.com/clients/ using Postman or Insomnia. You can use the following JSON as an example for the POST and PUT method's tests. 

```
{
    "company_name": "My company",
    "phone": "5571998989898",
    "address": {
        "address": "Rua Amaralina",
        "number": 780,
        "zip_code": "44000000",
        "city": "Salvador",
        "state": "Bahia",
        "country": "Brazil"
    },
    "registration_date": "1996-07-16",
    "declared_billing": 100000.20,
    "bank_accounts": [
        {
            "agency": "0002",
            "account_number": "000254",
            "bank": "Pag bank"
        }
    ]

}
```

#### Unit tests

To run the unit tests, you must fork or clone this repository, install all the dependencies (better use a virtual environment for that) and run the following command where there's the manage.py file:

```
python manage.py test
```
