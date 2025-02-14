from rest_framework.test import APITestCase
from django.urls import reverse
from kpi_app.models import Asset, Attribute, KPI

class ComputeValueAPIViewTest(APITestCase):
    def setUp(self):
        self.asset = Asset.objects.create(asset_id="43", name="Test Asset")
        self.kpi = KPI.objects.create(name="Test KPI", expression="Regex(ATTR, \".*dog.*\")")
        self.attribute = Attribute.objects.create(asset=self.asset, attribute_id="6", kpi=self.kpi)
        self.url = reverse('message-ingester')

    def test_compute_value_valid_regex(self):
        response = self.client.post(self.url, {
            "asset_id": "43",
            "attribute_id": "6",
            "timestamp": "2022-07-31T23:28:47Z[UTC]",
            "value": "I have a Dog"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['value'], True)

    def test_compute_value_invalid_regex(self):
        response = self.client.post(self.url, {
            "asset_id": "43",
            "attribute_id": "6",
            "timestamp": "2022-07-31T23:28:47Z[UTC]",
            "value": "I have a cat"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['value'], False)

    def test_compute_value_no_kpi(self):
        attribute_no_kpi = Attribute.objects.create(asset=self.asset, attribute_id="7")
        response = self.client.post(self.url, {
            "asset_id": "43",
            "attribute_id": "7",
            "timestamp": "2022-07-31T23:28:47Z[UTC]",
            "value": "Test value"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "No KPI linked to this attribute")
