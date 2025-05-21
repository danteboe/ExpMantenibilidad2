from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    tags_list = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Report
        fields = [
            'id', 'title', 'description', 'author', 'department',
            'category', 'priority', 'status', 'created_at', 'updated_at',
            'due_date', 'tags', 'tags_list'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        tags_list = validated_data.pop('tags_list', [])
        report = Report.objects.create(**validated_data)
        
        if tags_list:
            report.set_tags_list(tags_list)
            report.save()
        
        return report
    
    def update(self, instance, validated_data):
        tags_list = validated_data.pop('tags_list', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if tags_list is not None:
            instance.set_tags_list(tags_list)
        
        instance.save()
        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags_list'] = instance.get_tags_list()
        return data