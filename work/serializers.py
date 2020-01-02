from rest_framework import serializers
from work.models import (
    Company, Manager, Work, Worker, WorkPlace, WorkTime,
    NEW, APPROVED, CANCELLED, FINISHED,
)


class ManagerSerializer(serializers.ModelSerializer):
    """
    Serializer for Manager model.
    """
    name = serializers.SerializerMethodField('full_name')

    def full_name(self, man):
        return f'{man.first_name} {man.last_name}'

    class Meta:
        model = Manager
        fields = (
            'id',
            'name',
            'email',
        )


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for Company model.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name="work:comp-detail")

    managers = ManagerSerializer(read_only=True, required=False, many=True)
    works = serializers.HyperlinkedIdentityField(view_name='work:work-list')

    class Meta:
        model = Company
        fields = (
            'url',
            'name',
            'works',            
            'managers',
        )


class WorkSerializer(serializers.ModelSerializer):
    """
    Serializer for Work model.
    """
    company = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Work
        fields = (
            'id',
            'name',
            'created_date',
            'company',
        )


class WorkTimeSerializer(serializers.ModelSerializer):
    """
    Serializer for WorkTime model.
    """
    def validate_time(self, data):
        """
        Check that the start is before the end
        """
        if data['time_start'] >= data['time_end']:
            raise serializers.ValidationError('Incorrect time values')
        return data

    class Meta:
        model = WorkTime
        fields = (
            'id',
            'date',
            'time_start',
            'time_end',
        )


class WorkPlaceSerializer(serializers.ModelSerializer):
    """
    Serializer for WorkPlace model.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name="work:wp-detail")

    status = serializers.ReadOnlyField(source='get_status_display')

    def validate(self, data):
        """
        Check that the manager and the work belong to the same company.
        """
        manager = data['manager']
        work = data['work']
        if manager.company != work.company:
            raise serializers.ValidationError('Should belong to the same company')
        return data

    def to_representation(self, instance):
        wt = super().to_representation(instance)
        manager = Manager.objects.get(id=wt['manager'])
        work = Work.objects.get(id=wt['work'])
        worker = Worker.objects.get(id=wt['worker'])
        wt['manager'] = f'{manager.first_name} {manager.last_name}'
        wt['work'] = f'{work.name}'
        wt['worker'] = f'{worker.first_name} {worker.last_name}'
        return wt

    class Meta:
        model = WorkPlace
        fields = (
            'url',
            'manager',
            'work',
            'worker',
            'status',
        )


class WorkPlaceDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for WorkPlace model in detail view.
    """
    work = serializers.ReadOnlyField(source='work.name')
    status = serializers.CharField(source='get_status_display')
    worktimes = serializers.HyperlinkedIdentityField(view_name='work:wt-list')
    worker = serializers.SerializerMethodField('full_name')

    def full_name(self, wp):
        return f'{wp.worker.first_name} {wp.worker.last_name}'

    class Meta:
        model = WorkPlace
        fields = (
            'id',
            'work',
            'worker',
            'status',
            'worktimes',
        )


class WorkerSerializer(serializers.ModelSerializer):
    """
    Serializer for Worker model.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name="work:worker-detail")

    workplace = serializers.SerializerMethodField('approved_workplace')

    def approved_workplace(self, worker):
        if WorkPlace.objects.filter(worker=worker, status=APPROVED).exists():
            wp = WorkPlace.objects.get(worker=worker, status=APPROVED)
            return f'{wp.work.name}'
        return 'Not working now'

    class Meta:
        model = Worker
        fields = (
            'url',
            'first_name',
            'last_name',
            'workplace'
        )


class WorkerDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Worker model in detail view.
    """
    workplaces = WorkPlaceSerializer(read_only=True, required=False, many=True)

    class Meta:
        model = Worker
        fields = (
            'id',
            'first_name',
            'last_name',
            'workplaces',
        )
