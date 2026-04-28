from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.qa_service import QAService


class AssistantAPIView(APIView):
    def post(self, request, *args, **kwargs):
        query = request.data.get("query")

        if not query:
            return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)

        answer = QAService().get_answer(query)
        return Response({"answer": answer})
