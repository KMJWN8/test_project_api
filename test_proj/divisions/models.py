from django.db import models


class EmployeeContainerMixin:
    """
    Миксин для моделей, которые содержат сотрудников и дочерние подразделения.
    Предоставляет метод get_all_employees для получения всех сотрудников.
    """

    def get_all_employees(self):
        """
        Возвращает всех сотрудников, включая дочерние подразделения.
        """
        employees = []
        # Определяем связь с дочерними подразделениями
        child_relation = None
        if hasattr(self, "departments"):  # Для Service
            child_relation = self.departments.all()
        elif hasattr(self, "divisions"):  # Для Department
            child_relation = self.divisions.all()
        elif hasattr(self, "teams"):  # Для Division
            child_relation = self.teams.all()

        # Рекурсивно добавляем сотрудников из дочерних подразделений
        if child_relation:
            for child in child_relation:
                employees += child.get_all_employees()

        return employees


class Service(models.Model, EmployeeContainerMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model, EmployeeContainerMixin):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Division(models.Model, EmployeeContainerMixin):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="divisions"
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Employee(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.CharField(max_length=255, verbose_name="Должность")
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    photo = models.ImageField(
        upload_to="employee_photos/", blank=True, null=True, verbose_name="Фотография"
    )
    start_date = models.DateField(verbose_name="Дата начала работы")
    
    @property
    def team(self):
        return self.team_members.first().name
    
    def __str__(self):
        return self.full_name

class Team(models.Model):
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="teams"
    )
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Employee, related_name="team_members", blank=True)

    def get_all_employees(self):
        """
        Возвращает всех сотрудников группы.
        """
        return list(self.members.all())

    def __str__(self):
        return self.name


