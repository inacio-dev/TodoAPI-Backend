from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Task
from django.http import HttpResponse
from .serializers import TaskSerializer
from .utils import get_user_from_token
import pandas as pd


class TaskDataProcessView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        access_token = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        user = get_user_from_token(access_token)
        tasks = Task.objects.filter(user=user)
        serializer = TaskSerializer(tasks, many=True)

        df = pd.DataFrame(serializer.data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="tasks.xlsx"'
        df.to_excel(response, index=False)

        return response

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({'error': 'Arquivo não encontrado'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        user = get_user_from_token(access_token)

        tasks_imported = 0
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        except pd.errors.ParserError:
            return Response({'error': 'Falha ao ler o arquivo'}, status=status.HTTP_400_BAD_REQUEST)

        df['user'] = user.id  # Adiciona o usuário à informação da tarefa

        for index, row in df.iterrows():
            task_serializer = TaskSerializer(data=row.to_dict())
            if task_serializer.is_valid():
                task_serializer.save()
                tasks_imported += 1

        return Response({'tasks_imported': tasks_imported}, status=status.HTTP_201_CREATED)


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        access_token = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        user = get_user_from_token(access_token)
        return Task.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        access_token = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        user = get_user_from_token(access_token)
        queryset = self.get_queryset().filter(user=user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        access_token = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        user = get_user_from_token(access_token)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
