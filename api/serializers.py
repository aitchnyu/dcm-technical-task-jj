import os
from django.conf import settings
from rest_framework import serializers

from api.models import TestRunRequest, TestFilePath, TestEnvironment


class TestRunRequestSerializer(serializers.ModelSerializer):
    env_name = serializers.ReadOnlyField(source='env.name')

    class Meta:
        model = TestRunRequest
        fields = (
            'id',
            'requested_by',
            'env',
            'path',
            'status',
            'created_at',
            'env_name'
        )
        read_only_fields = (
            'id',
            'created_at',
            'status',
            'logs',
            'env_name'
        )


class TestRunRequestItemSerializer(serializers.ModelSerializer):
    env_name = serializers.ReadOnlyField(source='env.name')

    class Meta:
        model = TestRunRequest
        fields = (
            'id',
            'requested_by',
            'env',
            'path',
            'status',
            'created_at',
            'env_name',
            'logs'
        )


class TestFilePathSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestFilePath
        fields = ('id', 'path')


class TestFilePathCreateSerializer(serializers.Serializer):
    upload_dir = serializers.CharField(max_length=1024, write_only=True)
    test_file = serializers.FileField(write_only=True)

    @staticmethod
    def write_test_file(dir_name, file_name, file_contents):
        os.makedirs(dir_name, exist_ok=True)
        with open(file_name  , 'wb+') as f:
            f.write(file_contents)
    
    def validate_test_file(self, value):
        if not value.name.endswith('.py'):
            raise serializers.ValidationError('File extension is not .py')
        if not value.content_type.endswith("text/x-python"):
            raise serializers.ValidationError('File content-type is not text/x-python')
        return value

    def create(self, validated_data):
        file_upload = validated_data['test_file']
        dirname = os.path.join(settings.BASE_DIR, 'user_tests', validated_data['upload_dir'])
        filename =  os.path.join(dirname, file_upload.name)
        relative_filename = os.path.relpath(filename, settings.BASE_DIR)
        self.write_test_file(dirname, filename, validated_data['test_file'].read())
        
        maybe_test_file_path = TestFilePath.objects.filter(path=relative_filename).first()
        if maybe_test_file_path:
            return maybe_test_file_path
        else:
            return TestFilePath.objects.create(path=relative_filename)


class TestEnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestEnvironment
        fields = ('id', 'name')
