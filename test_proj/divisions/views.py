from datetime import date

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Department, Division, Employee, Service, Team
from .serializers import (
    DepartmentSerializer,
    DivisionSerializer,
    EmployeeSerializer,
    ServiceSerializer,
    TeamSerializer,
)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    @action(detail=True, methods=["get"], url_path="employees")
    def employees(self, request, pk=None):
        """
        Возвращает всех сотрудников службы, включая дочерние подразделения.
        """
        service = self.get_object()
        employees = service.get_all_employees()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=True, methods=["get"], url_path="employees")
    def employees(self, request, pk=None):
        """
        Возвращает всех сотрудников управления, включая дочерние подразделения.
        """
        department = self.get_object()
        employees = department.get_all_employees()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="statistics")
    def statistics(self, request, pk=None):
        """
        Возвращает статистику для выбранного управления:
        - Количество сотрудников.
        - Средний возраст сотрудников.
        - Средний стаж работы в подразделении.
        """
        department = self.get_object()

        # Получаем всех сотрудников подразделения
        employees = department.get_all_employees()

        # Количество сотрудников
        employee_count = len(employees)

        if employee_count == 0:
            # Если нет сотрудников, возвращаем нулевые значения
            return Response(
                {"employee_count": 0, "average_age": 0, "average_tenure": 0}
            )

        # Средний возраст сотрудников
        today = date.today()
        # Ручной расчет среднего возраста и стажа
        total_age = 0
        total_tenure = 0

        for employee in employees:
            # Возраст сотрудника
            age = today.year - employee.date_of_birth.year
            total_age += age

            # Стаж работы
            tenure = today.year - employee.start_date.year
            total_tenure += tenure

        # Вычисляем средние значения
        average_age = total_age / employee_count
        average_tenure = total_tenure / employee_count

        # Возвращаем результат
        return Response(
            {
                "employee_count": employee_count,
                "average_age": round(average_age, 2),
                "average_tenure": round(average_tenure, 2),
            }
        )


class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

    @action(detail=True, methods=["get"], url_path="employees")
    def employees(self, request, pk=None):
        """
        Возвращает всех сотрудников отдела, включая его руководителя
        и всех сотрудников групп.
        """
        division = self.get_object()
        employees = division.get_all_employees()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=["get"], url_path="employees")
    def employees(self, request, pk=None):
        """
        Возвращает всех сотрудников группы.
        """
        team = self.get_object()
        employees = team.get_all_employees()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
