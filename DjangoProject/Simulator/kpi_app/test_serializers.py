from django.test import TestCase
from kpi_app.models import KPI, Asset, Attribute
from kpi_app.serializers import KPISerializer, AssetSerializer, AttributeSerializer

class KPIAppSerializerTests(TestCase):

    def setUp(self):
        self.kpi = KPI.objects.create(name="Test KPI", expression="ATTR * 2", description="Sample KPI")
        self.asset = Asset.objects.create(asset_id="123", name="Test Asset")
        self.attribute = Attribute.objects.create(asset=self.asset, attribute_id="attr1", kpi=self.kpi)

    def test_kpi_serializer(self):
        serializer = KPISerializer(self.kpi)
        data = serializer.data
        self.assertEqual(data["name"], "Test KPI")
        self.assertEqual(data["expression"], "ATTR * 2")

    def test_asset_serializer(self):
        serializer = AssetSerializer(self.asset)
        data = serializer.data
        self.assertEqual(data["asset_id"], "123")
        self.assertEqual(data["name"], "Test Asset")
        self.assertEqual(len(data["attributes"]), 1)

    def test_attribute_serializer(self):
        serializer = AttributeSerializer(self.attribute)
        data = serializer.data
        self.assertEqual(data["asset"], self.asset.id)
        self.assertEqual(data["attribute_id"], "attr1")
        self.assertEqual(data["kpi"], self.kpi.id)
