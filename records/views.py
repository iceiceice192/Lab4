
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .forms import RecordForm
from .models import Record
from .utils import save_to_json, save_to_xml
from django.db.models import Q

def add_record(request):
    msg=None
    if request.method=='POST':
        f=RecordForm(request.POST)
        if f.is_valid():
            storage=f.cleaned_data.pop('storage')
            data=f.cleaned_data
            if storage=='db':
                if Record.objects.filter(name=data['name'],email=data['email']).exists():
                    msg='Дубликат'
                else:
                    Record.objects.create(**data); msg='Сохранено в БД'
            elif storage=='json':
                save_to_json(data); msg='Сохранено в JSON'
            else:
                save_to_xml(data); msg='Сохранено в XML'
    else:
        f=RecordForm()
    return render(request,'add.html',{'form':f,'msg':msg})

def list_records(request):
    return render(request,'list.html',{'records':Record.objects.all()})

def ajax_search(request):
    q=request.GET.get('q','')
    return JsonResponse(list(Record.objects.filter(
        Q(name__icontains=q)|Q(email__icontains=q)|Q(description__icontains=q)
    ).values()),safe=False)

def edit_record(request,pk):
    r=get_object_or_404(Record,pk=pk)
    f=RecordForm(request.POST or None,instance=r)
    if f.is_valid():
        f.save(); return redirect('/list/')
    return render(request,'edit.html',{'form':f})

def delete_record(request,pk):
    get_object_or_404(Record,pk=pk).delete()
    return redirect('/list/')
