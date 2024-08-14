"""Repair command tests"""

from django.core import management

from kalabash.lib.permissions import ObjectAccess, get_object_owner
from kalabash.lib.tests import KbashTestCase
from .. import factories, models


class RepairTestCase(KbashTestCase):
    """TestCase for repair command."""

    @classmethod
    def setUpTestData(cls):  # NOQA:N802
        """Create some data."""
        super(RepairTestCase, cls).setUpTestData()
        factories.populate_database()

    def test_management_command(self):
        """Check that command works fine."""
        ObjectAccess.objects.all().delete()
        mbox = models.Mailbox.objects.first()
        alias = models.Alias.objects.first()
        # assert mbox has no owner
        self.assertIs(get_object_owner(mbox), None)
        # fix it. run in quiet mode because we dont want output in tests
        ret = management.call_command("kbash", "repair", "--quiet")
        assert ret is None
        # assert it's fixed
        self.assertIsNot(get_object_owner(mbox), None)
        self.assertIsNot(get_object_owner(alias), None)

    def test_management_command_with_dry_run(self):
        """Check that command works fine."""
        ObjectAccess.objects.all().delete()
        mbox = models.Mailbox.objects.first()
        # assert mbox has no owner
        self.assertIs(get_object_owner(mbox), None)
        # show problems. run in quiet mode because we dont want output in tests
        ret = management.call_command("kbash", "repair", "--quiet", "--dry-run")
        assert ret is None
        # assert its not fixed
        self.assertIs(get_object_owner(mbox), None)

    def test_management_command_with_nul_domain(self):
        """Just assume nothing raise when an alias has no domain."""
        models.Alias.objects.create(address="@kalabash.xxx")
        ret = management.call_command("kbash", "repair", "--quiet")
        assert ret is None

    def test_management_command_with_no_alias(self):
        """Check that problem is fixed."""
        count, detail = models.Alias.objects.filter(
            address="user@test.com", internal=True
        ).delete()
        self.assertEqual(count, 3)
        ret = management.call_command("kbash", "repair", "--quiet")
        assert ret is None
        self.assertTrue(
            models.Alias.objects.filter(address="user@test.com", internal=True).exists()
        )
