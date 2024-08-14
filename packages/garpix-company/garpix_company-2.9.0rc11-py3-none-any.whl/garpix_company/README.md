# Garpix Company

Company module for Django/DRF projects.


## Quickstart

Install with pip:

```bash
pip install garpix_company
```

Add the `garpix_company` to your `INSTALLED_APPS`:

```python
# settings.py

# ...
INSTALLED_APPS = [
    # ...
    'garpix_company',
]
```

and to migration modules:

```python
# settings.py

# ...
MIGRATION_MODULES = {
    'garpix_company': 'app.migrations.garpix_company',
}
```

Add to `urls.py`:

```python

# ...
urlpatterns = [
    # ...
    # garpix_company
    path('', include(('garpix_company.urls', 'garpix_company'), namespace='garpix_company')),

]
```

Add Company model to your project using abstract `AbstractCompany` from the model:
```python
from garpix_company.models import AbstractCompany


class Company(AbstractCompany):
    pass

```

Add UserCompanyRole model to your project using abstract `AbstractUserCompanyRole` from the model:
```python
from garpix_company.models import AbstractUserCompanyRole


class UserCompanyRole(AbstractUserCompanyRole):
    pass


```

Add `GARPIX_COMPANY_MODEL`, `GARPIX_USER_COMPANY_MODEL` and `GARPIX_COMPANY_ROLE_MODEL` to `settings.py`:

```python
# settings.py

GARPIX_COMPANY_MODEL = 'app.Company'
GARPIX_COMPANY_ROLE_MODEL = 'app.UserCompanyRole'
GARPIX_USER_COMPANY_MODEL = 'garpix_company.UserCompany'

```

Use `CompanyAdmin` as base in your admin panel:
```python
from django.contrib import admin

from app.models import Company
from garpix_company.admin import CompanyAdmin


@admin.register(Company)
class CompanyAdmin(CompanyAdmin):
    pass

```

## Invite and create user

You can add fields to `company_invite/create_and_invite` endpoint.  

To do it override `CreateAndInviteToCompanySerializer` by adding field and add it to `settings`:

```python
# settings.py

GARPIX_COMPANY_CREATE_AND_INVITE_SERIALIZER = 'app.serializers.CustomInviteCompanySerializer'

```

```python
# app.serializers.py

from rest_framework import serializers

from garpix_company.serializers import CreateAndInviteToCompanySerializer


class CustomInviteCompanySerializer(CreateAndInviteToCompanySerializer):
    username = serializers.CharField(write_only=True)

    class Meta(CreateAndInviteToCompanySerializer.Meta):
        fields = CreateAndInviteToCompanySerializer.Meta.fields + ('username',)


```

You also can override `UserSerializer` and `CompanyRoleSerializer` to add custom fields to `user` and `role` fields of `/company/{pk}/user/` endpoints:

```python
# settings.py

GARPIX_COMPANY_USER_SERIALIZER = 'app.serializers.UserSerializer'
GARPIX_COMPANY_ROLE_SERIALIZER = 'app.serializers.CompanyRoleSerializer'

```

You can also set `GARPIX_COMPANY_INVITE_NOT_USERS` setting to True (False is default) to allow to invite not registered users

## Companies count limit

If you need to add some limitations on companies count the user can be a part of, you can override `check_user_companies_limit` class method of `Company` class:

```python
from garpix_company.models import AbstractCompany, get_user_company_model


class Company(AbstractCompany):

    @classmethod
    def check_user_companies_limit(cls, user):
        UserCompany = get_user_company_model()
        return UserCompany.objects.filter(user=user).count() < 1

```

See `garpix_company/tests/test_company.py` for examples.

# Changelog

Смотри [CHANGELOG.md](https://github.com/garpixcms/garpix_company/blob/master/CHANGELOG.md).

# Contributing

Смотри [CONTRIBUTING.md](https://github.com/garpixcms/garpix_company/blob/master/CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)