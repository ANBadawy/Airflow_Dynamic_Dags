from django.test import TestCase
from kpi_app.models import KPI, Asset, Attribute

class KPIAppModelTests(TestCase):

    def setUp(self):
        self.kpi = KPI.objects.create(name="Test KPI", expression="ATTR * 2", description="Sample KPI")
        self.asset = Asset.objects.create(asset_id="123", name="Test Asset")

    def test_kpi_creation(self):
        self.assertEqual(self.kpi.name, "Test KPI")
        self.assertEqual(self.kpi.expression, "ATTR * 2")

    def test_asset_creation(self):
        self.assertEqual(self.asset.asset_id, "123")
        self.assertEqual(self.asset.name, "Test Asset")

    def test_attribute_creation_with_kpi(self):
        attribute = Attribute.objects.create(asset=self.asset, attribute_id="attr1", kpi=self.kpi)
        self.assertEqual(attribute.asset, self.asset)
        self.assertEqual(attribute.kpi, self.kpi)
        self.assertEqual(attribute.attribute_id, "attr1")

    def test_attribute_creation_without_kpi(self):
        attribute = Attribute.objects.create(asset=self.asset, attribute_id="attr2")
        self.assertEqual(attribute.asset, self.asset)
        self.assertIsNone(attribute.kpi)
