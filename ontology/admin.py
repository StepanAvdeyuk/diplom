from django import forms
from django.contrib import admin
from .models import FileUpload
from .utils import DataImporter, OntologyManager, process_file
from django.core.exceptions import ValidationError

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file', 'description', 'tag_type']

@admin.action(description='Загрузить вариации тегов')
def upload_tag_variations(modeladmin, request, queryset):
    for file_upload in queryset:
        if file_upload.tag_type in ['vacancy', 'skill']:
            importer = DataImporter(file_upload.file.path, file_upload.tag_type)
            importer.read_variations()
            file_upload.delete()
        else:
            modeladmin.message_user(request, "Только типы 'vacancy' и 'skill' поддерживаются для этого действия.")


@admin.action(description='Загрузить онтологию')
def upload_ontology(modeladmin, request, queryset):
    for file_upload in queryset:
        if file_upload.tag_type == 'ontology':
            OntologyManager._instance = None  # сбросить текущий экземпляр
            OntologyManager._instance = OntologyManager()
            file_upload.delete()
        else:
            modeladmin.message_user(request, "Только тип 'ontology' поддерживается для этого действия.")

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('file', 'tag_type', 'uploaded_at')

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
            # Process the file based on the type
            process_file(obj)
        except ValidationError as e:
            self.message_user(request, e.message, level='error')

admin.site.register(FileUpload, FileUploadAdmin)