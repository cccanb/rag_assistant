import logging

from openai import APIError, RateLimitError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AssistantRequestSerializer
from .services.qa_service import QAService

logger = logging.getLogger(__name__)


class AssistantAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AssistantRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        query = serializer.validated_data["query"]

        try:
            answer = QAService().get_answer(query)
            return Response({"answer": answer})
        except RateLimitError:
            return Response(
                {"error": "Service temporarily unavailable. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except APIError:
            return Response(
                {"error": "AI service error. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception:
            logger.exception("Unhandled error in AssistantAPIView")
            return Response(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
