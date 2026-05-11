from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import Message
from .serializers import DelayTaskSerializer, EmailTaskSerializer
from .tasks import delay_task, email_task


@api_view(["POST"])
def start_delay_task(request):
    serializer = DelayTaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        delay_task.delay(serializer.validated_data["text"])
    except Exception:
        return Response(
            {"error": "Could not connect to Celery broker"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return Response({
        "message": "Task started successfully"
    }, status=status.HTTP_202_ACCEPTED)


class StartEmailTaskView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = EmailTaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        try:
            email_task.delay(message.email_address)
        except Exception:
            return Response(
                {"error": "Could not connect to Celery broker"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({
            "message": "Task started successfully",
            "data": EmailTaskSerializer(message).data,
        }, status=status.HTTP_202_ACCEPTED)
