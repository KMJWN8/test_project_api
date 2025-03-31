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

        # Добавляем руководителя, если он есть
        if hasattr(self, "leader") and self.leader:
            employees.append(self.leader)

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


class Employee(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.CharField(max_length=255, verbose_name="Должность")
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    photo = models.ImageField(
        upload_to="employee_photos/", blank=True, null=True, verbose_name="Фотография"
    )
    start_date = models.DateField(verbose_name="Дата начала работы")

    def __str__(self):
        return self.full_name

    @property
    def subdivision_name(self):
        """
        Возвращает название подразделения, в котором работает сотрудник.
        """
        # Проверяем, является ли сотрудник руководителем службы
        if hasattr(self, "service_leader") and self.service_leader:
            return f"{self.service_leader.name}"

        # Проверяем, является ли сотрудник руководителем управления
        if hasattr(self, "department_leader") and self.department_leader:
            return f"{self.department_leader.name}"

        # Проверяем, является ли сотрудник руководителем отдела
        if hasattr(self, "division_leader") and self.division_leader:
            return f"{self.division_leader.name}"

        # Проверяем, к какой группе принадлежит сотрудник
        teams = self.team_members.all()
        if teams.exists():
            return f"{teams.first().name}"  # Берем первую группу из списка

        # Если сотрудник не связан ни с одним подразделением
        return "Не определено"


class Service(models.Model, EmployeeContainerMixin):
    name = models.CharField(max_length=255)
    leader = models.OneToOneField(
        Employee,
        on_delete=models.SET_NULL,
        related_name="service_leader",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Department(models.Model, EmployeeContainerMixin):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(max_length=255)
    leader = models.OneToOneField(
        Employee,
        on_delete=models.SET_NULL,
        related_name="department_leader",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} ({self.service})"


class Division(models.Model, EmployeeContainerMixin):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="divisions"
    )
    name = models.CharField(max_length=255)
    leader = models.OneToOneField(
        Employee,
        on_delete=models.SET_NULL,
        related_name="division_leader",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} ({self.department})"


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
        return f"{self.name} ({self.division})"
