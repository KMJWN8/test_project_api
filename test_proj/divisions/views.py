from datetime import date

from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Department, Division, Employee, Service, Team
from .serializers import (
    DepartmentSerializer,
    DivisionSerializer,
    EmployeeSerializer,
    ServiceSerializer,
    TeamSerializer,
)


class EmployeesMixin:
    """
    Миксин для ViewSet, который предоставляет универсальный метод employees.
    """

    @action(detail=True, methods=["get"], url_path="employees")
    def employees(self, request, pk=None):
        """
        Возвращает всех сотрудников, включая дочерние подразделения.
        """
        obj = self.get_object()
        employees = obj.get_all_employees()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet, EmployeesMixin):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    @action(detail=True, methods=["get"], url_path="statistics")
    def statistics(self, request, pk=None):
        service = self.get_object()
        # Получаем всех сотрудников службы
        employees = service.get_all_employees()
        # Используем универсальную функцию для получения статистики
        stats = get_statistics(employees)
        # Возвращаем результат
        return Response(stats)


class DepartmentViewSet(viewsets.ModelViewSet, EmployeesMixin):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=True, methods=["get"], url_path="statistics")
    def statistics(self, request, pk=None):
        department = self.get_object()
        # Получаем всех сотрудников подразделения
        employees = department.get_all_employees()
        # Используем универсальную функцию для получения статистики
        stats = get_statistics(employees)
        # Возвращаем результат
        return Response(stats)


class DivisionViewSet(viewsets.ModelViewSet, EmployeesMixin):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

    @action(detail=True, methods=["get"], url_path="statistics")
    def statistics(self, request, pk=None):
        division = self.get_object()
        # Получаем всех сотрудников службы
        employees = division.get_all_employees()
        # Используем универсальную функцию для получения статистики
        stats = get_statistics(employees)
        # Возвращаем результат
        return Response(stats)


class TeamViewSet(viewsets.ModelViewSet, EmployeesMixin):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=["get"], url_path="statistics")
    def statistics(self, request, pk=None):
        team = self.get_object()
        # Получаем всех сотрудников службы
        employees = team.get_all_employees()
        # Используем универсальную функцию для получения статистики
        stats = get_statistics(employees)
        # Возвращаем результат
        return Response(stats)

    @action(detail=True, methods=["patch"], url_path="add-member")
    def add_member(self, request, pk=None):
        """
        Добавляет сотрудника в группу.
        Принимает JSON с ключом 'member_id'.
        """
        # Получаем объект группы
        team = self.get_object()

        # Получаем ID сотрудника из запроса
        member_id = request.data.get("member_id")

        # Получаем объект сотрудника
        member = Employee.objects.get(id=member_id)

        # Добавляем сотрудника в группу
        team.members.add(member)

        return Response(
            {"message": f"Сотрудник {member.full_name} успешно добавлен в группу."}
        )


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["full_name"]


def get_statistics(employees):
    """
    Возвращает статистику для переданного списка сотрудников:
    - Количество сотрудников.
    - Средний возраст сотрудников.
    - Средний стаж работы.
    """
    employee_count = len(employees)

    if employee_count == 0:
        # Если нет сотрудников, возвращаем нулевые значения
        return {
            "employee_count": 0,
            "average_age": 0,
            "average_tenure": 0,
        }

    # Средний возраст сотрудников
    today = date.today()
    total_age = 0
    total_tenure = 0

    for employee in employees:
        # Возраст сотрудника
        age = today.year - employee.date_of_birth.year
        if (today.month, today.day) < (
            employee.date_of_birth.month,
            employee.date_of_birth.day,
        ):
            age -= 1  # Корректировка возраста, если день рождения ещё не наступил
        total_age += age

        # Стаж работы
        tenure = today.year - employee.start_date.year
        if (today.month, today.day) < (
            employee.start_date.month,
            employee.start_date.day,
        ):
            tenure -= 1  # Корректировка стажа, если год ещё не завершился
        total_tenure += tenure

    # Вычисляем средние значения
    average_age = total_age / employee_count
    average_tenure = total_tenure / employee_count

    # Возвращаем результат
    return {
        "employee_count": employee_count,
        "average_age": round(average_age),
        "average_tenure": round(average_tenure),
    }
