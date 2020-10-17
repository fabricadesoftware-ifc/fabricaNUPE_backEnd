from django.test import TestCase
from model_bakery import baker

from nupe.account.models import Account


class AccountTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Account, "_safedelete_policy"), True)
        self.assertIs(hasattr(Account, "email"), True)
        self.assertIs(hasattr(Account, "person"), True)
        self.assertIs(hasattr(Account, "local_job"), True)
        self.assertIs(hasattr(Account, "function"), True)
        self.assertIs(hasattr(Account, "sector"), True)
        self.assertIs(hasattr(Account, "date_joined"), True)
        self.assertIs(hasattr(Account, "updated_at"), True)
        self.assertIs(hasattr(Account, "is_active"), True)
        self.assertIs(hasattr(Account, "is_staff"), True)
        self.assertIs(hasattr(Account, "is_superuser"), True)
        self.assertIs(hasattr(Account, "full_name"), True)
        self.assertIs(hasattr(Account, "short_name"), True)
        self.assertIs(hasattr(Account, "account_attendances"), True)

    def test_return_str(self):
        account = baker.prepare("account.Account")

        self.assertEqual(str(account), account.email)

    def test_return_properties(self):
        account = baker.prepare("account.Account", person=baker.prepare("core.Person"))

        self.assertEqual(account.full_name, account.person.full_name)
        self.assertEqual(account.short_name, account.person.first_name)
