from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from kpi_app.models import Asset, Attribute
from interpreter_app.interpreter_engine import SimpleInterpreterFactory

class ComputeValueAPIView(APIView):
    name = "Message Ingester"
    def post(self, request):

        # Extracting data from the request
        asset_id = request.data.get("asset_id")
        attribute_id = request.data.get("attribute_id")
        timestamp = request.data.get("timestamp")
        value = request.data.get("value")

        # Fetching the Asset and Attribute to get the KPI equation
        asset = get_object_or_404(Asset, asset_id=asset_id)
        attribute = get_object_or_404(Attribute, asset=asset, attribute_id=attribute_id)

        # Ensuring that the attribute has a linked KPI with an equation
        if not attribute.kpi:
            return Response({"error": "No KPI linked to this attribute"}, status=400)

        equation = attribute.kpi.expression
        equation = equation.replace("\\\"", "\"").replace("\\\\", "\\")

        try:
            value = float(value)
        except ValueError:
            pass

        context = {"ATTR": value}

        interpreter_factory = SimpleInterpreterFactory()
        lexer = interpreter_factory.create_lexer(equation)
        parser = interpreter_factory.create_parser(lexer, context)
        interpreter = interpreter_factory.create_interpreter(parser, context)

        try:
            computed_value = interpreter.interpret()
        except Exception as e:
            return Response({"error": f"Interpreter Error: {str(e)} (Equation: {equation}, Context: {context})"},
                            status=400)

        response_data = {
            "asset_id": asset_id,
            "attribute_id": f"output_{attribute_id}",
            "timestamp": timestamp,
            "value": computed_value
        }
        return Response(response_data)



