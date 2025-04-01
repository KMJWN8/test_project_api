from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
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
            "team"
        ]
        
    def get_team_name(self, obj):
        return obj.team



class TeamSerializer(WritableNestedModelSerializer):
    members = EmployeeSerializer(many=True)
    
    class Meta:
        model = Team
        fields = ["id", "name", "members"]

    def get_all_employees(self, obj):
        return EmployeeSerializer(obj.get_all_employees(), many=True).data


class DivisionSerializer(WritableNestedModelSerializer):
    teams = serializers.SerializerMethodField()

    class Meta:
        model = Division
        fields = ["id", "name", "teams"]

    def get_teams(self, obj):
        return TeamSerializer(obj.teams.all(), many=True).data


class DepartmentSerializer(WritableNestedModelSerializer):
    divisions = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id", "name", "divisions"]

    def get_divisions(self, obj):
        return DivisionSerializer(obj.divisions.all(), many=True).data


class ServiceSerializer(WritableNestedModelSerializer):
    departments = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ["id", "name", "departments"]

    def get_departments(self, obj):
        return DepartmentSerializer(obj.departments.all(), many=True).data
