from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def form_handler(request: HttpRequest) -> HttpResponse:
    context = {}
    max_file_size = 4000
    if request.method == 'POST' and request.FILES.get('myfile'):
        if (request.FILES.get('myfile').size > 0) and (request.FILES.get('myfile').size <= max_file_size):
            file = request.FILES['myfile']

            fs = FileSystemStorage()
            fs.save(file.name, file)

            context = {'message': 'Файл успешно отправлен'}

        else:
            context = {'message': f'Файл не отправлен, размер файла более {max_file_size}'}

    return render(request=request, template_name='requestdataapp/form-list.html', context=context)


def raise_error_frequent_call(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request=request, template_name='requestdataapp/error-frequent-call.html', context=context)