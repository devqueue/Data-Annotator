from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.settings import UPLOAD_PATH
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from .Serializers import CSVSerializer
from .forms import CsvModelForm
from .models import Csv
from apps.utils import required, required_at_upload, allowed_users
from apps.search.models import Sentance_for_tagging, Sentance_for_classification
import pandas as pd
from datetime import datetime
import traceback
import os
import json
# Create your views here.


@login_required(login_url='/login')
@allowed_users(allowed_roles=['compute'])
def upload_file(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    is_csv = False
    is_excel = False
    context = {
        'segment': 'upload',
        'form': form
    }
    if form.is_valid():
        context['post'] = True
        file_name = form.cleaned_data.get('file_name')
        file_path = form.cleaned_data.get('file_name').temporary_file_path()

        if (str(file_name)).endswith('.csv'):
            is_csv = True
        if (str(file_name)).endswith('.xlsx') or (str(file_name)).endswith('.xls'):
            is_excel = True

        df1 = pd.read_csv(file_path, low_memory=False) if is_csv else pd.read_excel(file_path)
        print(df1)
        try:
            df1 = df1[['id', 'sentence']].to_dict('records')

            sentance_instances = [Sentance_for_classification(
                    id=record['id'],
                    sentance=record['sentence']
                ) for record in df1]

            sentance_instances2 = [Sentance_for_tagging(
                    id=record['id'],
                    sentance=record['sentence']
                ) for record in df1]

            try:
                Sentance_for_classification.objects.bulk_create(sentance_instances)
                Sentance_for_tagging.objects.bulk_create(sentance_instances2)
            
            except Exception:
                Sentance_for_classification.objects.bulk_update(
                    sentance_instances,
                    fields=['id', 'sentence']
                )

                Sentance_for_tagging.objects.bulk_update(
                    sentance_instances,
                    fields=['id', 'sentence']
                )
                traceback.print_exc()

            # After sucessfully uploading
            context['message'] = 'File was uploaded sucessfully.'
            context['color'] = 2
            form.cleaned_data['activated'] = True
            form.save()

        except Exception:
            traceback.print_exc()
            context['message'] = 'An Error occured while uploading the file, please make sure the file format is correct and it contains all required columns.'
            context['color'] = 4

    return render(request, 'home/upload.html', context)

