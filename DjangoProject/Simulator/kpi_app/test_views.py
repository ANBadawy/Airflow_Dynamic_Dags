from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from kpi_app.models import KPI, Asset, Attribute

class KPIAppViewTests(APITestCase):

    def setUp(self):
        self.kpi = KPI.objects.create(name="Test KPI", expression="ATTR * 2", description="Sample KPI")
        self.asset = Asset.objects.create(asset_id="123", name="Test Asset")
        self.attribute = Attribute.objects.create(asset=self.asset, attribute_id="attr1", kpi=self.kpi)

    def test_list_kpis(self):
        url = reverse("kpi-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_kpi(self):
        url = reverse("kpi-list")
        data = {"name": "New KPI", "expression": "ATTR + 1", "description": "New KPI description"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_assets(self):
        url = reverse("asset-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_asset(self):
        url = reverse("asset-list")
        data = {"asset_id": "456", "name": "Another Asset"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_attributes(self):
        url = reverse("attribute-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_attribute(self):
        url = reverse("attribute-list")
        data = {"asset": self.asset.id, "attribute_id": "attr2", "kpi": self.kpi.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
