from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Classification, NER, Sentance_for_classification, Sentance_for_tagging
import pandas as pd
from django.http import HttpResponse
from apps.utils import allowed_users
from .forms import CHOICES
import datetime

# Create your views here.


@login_required(login_url='accounts/login_user')
@allowed_users(allowed_roles=['compute', 'search'])
def classification_view(request):
    context = {
        'segment': 'classification'
    }

    form = CHOICES(request.POST)
    context['form'] = form

    if request.method == 'POST':
        if form.is_valid():
            id = request.POST.get("sentanceid")
            sentance = request.POST.get("sentance")
            selected = form.cleaned_data.get("NUMS")

        try:
            username = request.user.username
            Classification_item = Classification(id=id, sentance=sentance, label=selected)
            Classification_item.save()
            sentance_item = Sentance_for_classification.objects.get(pk=id)
            sentance_item.classified_by = username
            sentance_item.save()

            return redirect("/")
        except Exception as e:
            print('[ERROR]:', e)
            return redirect("/")
    else:
        result = Sentance_for_classification.objects.filter(classified_by='')
        if result:
            context['sentance'] = result[0].sentance
            context['id'] = result[0].id
        return render(request, 'home/search.html', context)


@login_required(login_url='accounts/login_user')
@allowed_users(allowed_roles=['compute', 'search'])
def ner(request):
    context = {
        'segment': 'ner'
    }

    username = request.user.username

    if request.method == 'POST':
        
        id = request.POST.get("sentanceid")
        sentance = request.POST.get("sentance")
        words = sentance.split()
        list_of_tags = [request.POST.get(word) for word in words]


        try:
            for word, tag in zip(words, list_of_tags):
                tagging_item = NER(sentance=id, word=word, tag=f'{tag}, ')
                tagging_item.save()
            sentance_item = Sentance_for_tagging.objects.get(pk=id)
            sentance_item.tagged_by += f'{username}, '
            sentance_item.save()

            return redirect("/ner")
        except Exception as e:
            print('[ERROR]:', e)
            return redirect("/ner")
    else:
        result = Sentance_for_tagging.objects.all()
        result2 = NER.objects.all()
        print(result2)
        print(result)
        result = result.exclude(tagged_by__contains=f'{username}')

        if result:
            context['sentance'] = result[0].sentance
            context['id'] = result[0].id
            words = context['sentance'].split()
            context['words'] = words
        return render(request, 'home/ner.html', context)


@login_required(login_url='login/')
@allowed_users(allowed_roles=['compute', 'search'])
def export(request):
    context = {
        'segment': 'export',
    }
    if request.method == 'POST':
        table = request.POST.get('table')
        export = request.POST.get('export') 
        context['table'] = table
            
        if table == 'NER':
            df = pd.DataFrame(list(NER.objects.all().values()))
            df = df.tail(50)
            context['df_header'] = list(df.columns)
            context['df'] = df.to_dict('records')
        elif table == 'Classification':
            df = pd.DataFrame(list(Classification.objects.all().values()))
            df = df.tail(50)
            context['df_header'] = list(df.columns)
            context['df'] = df.to_dict('records')
        else:
            context['notselected'] = True
            return render(request, 'home/export.html', context)
        
        if df.empty:
            context['empty'] = True
            return render(request, 'home/export.html', context)

        if export:
            timestamp = datetime.datetime.now()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={table}-{timestamp}.csv'
            print("[INFO]: Table FOUND")
            df.to_csv(path_or_buf=response, index=False)
            return response

    return render(request, 'home/export.html', context)
