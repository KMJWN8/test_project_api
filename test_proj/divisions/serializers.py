from rest_framework import serializers

from .models import Department, Division, Employee, Service, Team


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "full_name",
            "position",
            "date_of_birth",
            "photo",
            "start_date",
            "subdivision_name",
        ]

    def get_subdivision_name(self, obj):
        """
        Получает значение свойства subdivision_name.
        """
        return obj.subdivision_name


class TeamSerializer(serializers.ModelSerializer):
    members = EmployeeSerializer(many=True)

    class Meta:
        model = Team
        fields = ["id", "name", "members"]

    def get_all_employees(self, obj):
        return EmployeeSerializer(obj.get_all_employees(), many=True).data


class DivisionSerializer(serializers.ModelSerializer):
    leader = EmployeeSerializer()
    teams = serializers.SerializerMethodField()

    class Meta:
        model = Division
        fields = ["id", "name", "leader", "teams"]

    def get_teams(self, obj):
        return TeamSerializer(obj.teams.all(), many=True).data


class DepartmentSerializer(serializers.ModelSerializer):
    leader = EmployeeSerializer()
    divisions = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id", "name", "leader", "divisions"]

    def get_divisions(self, obj):
        return DivisionSerializer(obj.divisions.all(), many=True).data


class ServiceSerializer(serializers.ModelSerializer):
    leader = EmployeeSerializer()
    departments = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ["id", "name", "leader", "departments"]

    def get_departments(self, obj):
        return DepartmentSerializer(obj.departments.all(), many=True).data
