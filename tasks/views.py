from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Task
from django.http import HttpResponse, StreamingHttpResponse
from .serializers import TaskSerializer
from .utils import get_user_from_token
import pandas as pd
from io import BytesIO
import xlsxwriter
import base64
from django.utils.encoding import smart_str


class TaskDataProcessView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        access_token = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        user = get_user_from_token(access_token)
        tasks = Task.objects.filter(user=user)
        serializer = TaskSerializer(tasks, many=True)

        data = serializer.data

        output = BytesIO()

        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        for row, item in enumerate(data):
            worksheet.write(row, 0, item['title'])
            worksheet.write(row, 1, item['description'])
            worksheet.write(row, 2, item['completed'])

        workbook.close()
        output.seek(0)

        base64_encoded = base64.b64encode(output.getvalue()).decode()
            
        response = StreamingHttpResponse(
            smart_str(base64_encoded),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="tasks.xlsx"'

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
                df = pd.read_excel(file, header=None, names=['title', 'description', 'completed'])
        except pd.errors.ParserError:
            return Response({'error': 'Falha ao ler o arquivo'}, status=status.HTTP_400_BAD_REQUEST)

        df['user'] = user.id

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
        queryset = self.get_queryset().filter(user=user).order_by('id')
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
