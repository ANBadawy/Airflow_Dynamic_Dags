from rest_framework import serializers
from .models import KPI, Asset, Attribute

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = ['id', 'name', 'expression', 'description']

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'asset', 'attribute_id', 'kpi']

class AssetSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = ['id', 'asset_id', 'name', 'attributes']
