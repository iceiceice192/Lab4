from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import RecordForm
from .models import Record
from .utils import save_to_json, save_to_xml
from django.db.models import Q
import json
import os
import xml.etree.ElementTree as ET
from django.conf import settings # Для правильных путей к файлам

def add_record(request):
    msg = None
    # Создаем форму. Если POST - с данными, если нет - пустую.
    f = RecordForm(request.POST or None)
    
    if request.method == 'POST':
        # Сначала получаем выбор хранилища
        storage = request.POST.get('storage')
        
        # ЛОГИКА ДЛЯ БАЗЫ ДАННЫХ
        if storage == 'db':
            if f.is_valid():
                # save() сам создаст запись в БД
                f.save()
                msg = 'Успешно сохранено в Базу Данных'
                f = RecordForm() # Очищаем форму после успеха
            else:
                msg = 'Ошибка! Возможно, такая запись уже есть в БД.'

        # ЛОГИКА ДЛЯ ФАЙЛОВ (JSON / XML)
        else:
            # Для файлов берем данные напрямую, игнорируя проверку уникальности БД
            name = request.POST.get('name')
            email = request.POST.get('email')
            desc = request.POST.get('description')
            
            # Проверяем, что поля не пустые
            if name and email and desc:
                data = {'name': name, 'email': email, 'description': desc}
                
                # Используем абсолютный путь, чтобы файлы точно нашлись
                base_path = settings.BASE_DIR 
                
                if storage == 'json':
                    save_to_json(data, os.path.join(base_path, 'data.json'))
                    msg = 'Успешно сохранено в JSON'
                elif storage == 'xml':
                    save_to_xml(data, os.path.join(base_path, 'data.xml'))
                    msg = 'Успешно сохранено в XML'
                
                f = RecordForm() # Очищаем форму
            else:
                msg = 'Пожалуйста, заполните все поля'

    return render(request, 'add.html', {'form': f, 'msg': msg})

def list_records(request):
    # Получаем источник из ссылки ?source=json, по умолчанию db
    source = request.GET.get('source', 'db')
    records = []
    base_path = settings.BASE_DIR

    if source == 'db':
        records = Record.objects.all()
    
    elif source == 'json':
        path = os.path.join(base_path, 'data.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                records = json.load(f)
    
    elif source == 'xml':
        path = os.path.join(base_path, 'data.xml')
        if os.path.exists(path):
            tree = ET.parse(path)
            root = tree.getroot()
            for elem in root:
                rec = {child.tag: child.text for child in elem}
                records.append(rec)

    return render(request, 'list.html', {'records': records, 'source': source})

def ajax_search(request):
    q = request.GET.get('q', '')
    
    # Если запрос пустой - возвращаем ВСЕ записи
    if not q:
        results = list(Record.objects.all().values())
    else:
        # Иначе фильтруем
        results = list(Record.objects.filter(
            Q(name__icontains=q) | 
            Q(email__icontains=q) | 
            Q(description__icontains=q)
        ).values())
    
    return JsonResponse(results, safe=False)

def edit_record(request, pk):
    r = get_object_or_404(Record, pk=pk)
    f = RecordForm(request.POST or None, instance=r)
    if f.is_valid():
        f.save()
        return redirect('/list/')
    return render(request, 'edit.html', {'form': f})

def delete_record(request, pk):
    get_object_or_404(Record, pk=pk).delete()
    return redirect('/list/')