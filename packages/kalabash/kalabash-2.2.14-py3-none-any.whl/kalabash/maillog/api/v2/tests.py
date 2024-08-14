"""API v2 tests."""

from django.urls import reverse

from kalabash.lib.tests import KbashAPITestCase


class StatisticsViewSetTestCase(KbashAPITestCase):

    def test_list(self):
        url = reverse("v2:statistics-list")
        resp = self.client.get(url + "?gset=mailtraffic&period=day")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(url + "?gset=mailtraffic&period=custom&start=2021-05-01")
        self.assertEqual(resp.status_code, 400)

        resp = self.client.get(
            url + "?gset=mailtraffic&period=custom&start=2021-05-01&end=2021-05-02"
        )
        self.assertEqual(resp.status_code, 200)


class MaillogViewSetTestCase(KbashAPITestCase):

    def test_list(self):
        url = reverse("v2:maillog-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
