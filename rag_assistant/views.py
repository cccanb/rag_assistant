import logging

from openai import APIError, RateLimitError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.qa_service import QAService

logger = logging.getLogger(__name__)


class AssistantAPIView(APIView):
    def post(self, request, *args, **kwargs):
        query = request.data.get("query")

        if not query:
            return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)

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
