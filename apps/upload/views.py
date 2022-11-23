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


# @login_required(login_url='/login')
# @allowed_users(allowed_roles=['compute'])
# def compute(request):
#     context = {
#         'segment': 'compute',
#     }
#     if request.method == 'POST':
#         start = datetime.now()
#         context['post'] = True
#         file_list = [os.path.join(UPLOAD_PATH, i)
#                     for i in os.listdir(UPLOAD_PATH) if i.endswith('.csv')]
#         df_list = []
#         try:
#             for file in file_list:
#                 headers = pd.read_csv(file, nrows=0).columns.tolist()
#                 req = set(headers) & set(required)
#                 df = pd.read_csv(file, usecols=req, low_memory=False)
#                 df['filename'] = [file.split('/')[-1]] * len(df)


#                 df_list.append(df)

#             frame = pd.concat(df_list, axis=0, ignore_index=True)
#             # def processing(frame):
#             frame.columns = frame.columns.str.replace(' ', '_')
#             grouped = frame.groupby(['chromosome', 'start_pos', 'end_pos',
#                                     'observed']).agg(lambda x: x.tolist())

#             grouped = grouped.astype(str).replace(
#                 "'", "", regex=True).replace("\[", "", regex=True).replace("\]", "", regex=True).replace("\,", ";", regex=True)


#             grouped['count_hom'] = grouped['zygosity'].apply(lambda x: x.count('hom'))
#             grouped['count_het'] = grouped['zygosity'].apply(lambda x: x.count('het'))

#             grouped['count_total'] = grouped['count_het'] + grouped['count_hom']
#             grouped['files_uploaded'] = [len(df_list)] * len(grouped)
#             grouped['New_allele_frequency'] = (grouped['count_het'] + 2*grouped['count_hom']) / (grouped['files_uploaded'] * 2)

#             dtypes = {
#                 'count_het': 'int16',
#                 'count_hom': 'int16',
#                 'count_total': 'int16',
#                 'files_uploaded': 'int16',
#                 'New_allele_frequency': 'float32',
#             }
#             grouped = grouped.astype(dtypes)
#             grouped = grouped.reset_index()
#             print("grouping done")
#             rows = [GeneStorage(
#                     # id=record[" "],
#                     chromosome=record["chromosome"],
#                     start_pos=record["start_pos"],
#                     end_pos=record["end_pos"],
#                     reference=record["reference"],
#                     observed=record["observed"],
#                     zygosity=record["zygosity"],
#                     refGene_function=record.get("refGene_function", None),
#                     refGene_gene=record["refGene_gene"],
#                     quality=record.get('quality', None),
#                     refGene_exonic_function=record.get(
#                         "refGene_exonic_function", None),
#                     AC=record.get("AC", None),
#                     AC_hom=record.get("AC_hom", None),
#                     aug_all=record.get("1000g2015aug_all", None),
#                     ExAC_ALL=record.get("ExAC_ALL", None),
#                     gnomAD_exome_AF=record.get("gnomAD_exome_AF", None),
#                     Kaviar_AF=record.get("Kaviar_AF", None),
#                     SIFT_pred_41a=record.get("SIFT_pred_41a", None),
#                     SIFT4G_pred_41a=record.get("SIFT4G_pred_41a", None),
#                     Polyphen2_HDIV_pred_41a=record.get(
#                         "Polyphen2_HDIV_pred_41a", None),
#                     Polyphen2_HVAR_pred_41a=record.get(
#                         "Polyphen2_HVAR_pred_41a", None),
#                     CADD_phred_41a=record.get("CADD_phred_41a", None),
#                     CLNSIG=record.get("CLNSIG", None),
#                     refGene_splice=record.get("refGene_splice_info", None),
#                     refGene_AA=record.get("refGene_AA_change", None),
#                     filename=record['filename'],
#                     count_hom=record["count_hom"],
#                     count_het=record["count_het"],
#                     count_total=record['count_total'],
#                     files_uploaded=record['files_uploaded'],
#                     New_allele_frequency=record['New_allele_frequency']
#                     ) for record in grouped.to_dict('records')]

#             GeneStorage.objects.all().delete()
#             GeneStorage.objects.bulk_create(rows)
#             context['message'] = 'All files were processed sucessfully.'
#             context['color'] = 2
#             print("COMPUTE SUCESSFUL")
#         except Exception:
#             traceback.print_exc()
#             context['message'] = 'An Error occured while processing the file, please check the logs'
#             context['color'] = 4
#         end = datetime.now()
#         print(end - start)
#         return render(request, 'home/compute.html', context)

#     else:  
#         result = GeneStorage.objects.all().values()
#         df = pd.DataFrame(result)
#         try:
#             df = df[['chromosome', 'start_pos', 'end_pos', 'observed', 'zygosity',
#                     'filename', 'count_hom', 'count_het', 'files_uploaded', 'New_allele_frequency']]

#             df = df.sample(5)
#             context['df_header'] = list(df.columns)
#             context['df'] = df.to_dict('records')
#         except Exception:
#             traceback.print_exc()
        

#         return render(request, 'home/compute.html', context)


# class UploadView(APIView):
#     serializer_class = CSVSerializer

#     def get(self, request):
#         files = serializers.serialize("json", Csv.objects.all())
#         json_object = json.loads(files)
#         files = [obj['fields']['file_name'] for obj in json_object]
#         print(json_object)
#         return Response({"Uploaded_Files": files})

#     def post(self, request):
#         serializer = CSVSerializer(data=request.data)
#         is_csv = None
#         is_excel = None
#         if serializer.is_valid():
#             file_name = self.request.FILES.get('file_name')
#             file_path = self.request.FILES.get('file_name').temporary_file_path()
#             print(file_name)
#             if (str(file_name)).endswith('.csv'):
#                 is_csv = True
#             if (str(file_name)).endswith('.xlsx') or (str(file_name)).endswith('.xls'):
#                 is_excel = True


#             df = pd.read_csv(file_path, low_memory=False) if is_csv else pd.read_excel(file_path)
#             if df.columns[0] != "chromosome":
#                 df.columns = [i for i in range(0, len(df.columns))]
#                 chrom_index = df.loc[df[0].str.contains("chromosome", case=False)].index[0]
#                 df =  df[chrom_index:]
#                 df.columns = df.loc[chrom_index]
#                 df = df.drop(chrom_index)
#                 df = df.reset_index()
#                 df = df.drop(['index'], axis=1)
            
#             try:
#                 headers = df.columns.tolist()
#                 req = set(headers) & set(required_at_upload)
#                 df1 = df.drop(df.columns.difference(req), axis=1)

#                 df1.columns = df1.columns.str.replace(' ', '_')
#                 test = df1[['chromosome', 'start_pos', 'end_pos', 'observed', 'refGene_gene', 'zygosity']]

#                 # check of the same file exists in the file system.
#                 os.makedirs(UPLOAD_PATH, exist_ok=True)
#                 file_list = [i for i in os.listdir(UPLOAD_PATH) if i.endswith('.csv') or i.endswith('.xlsx')]

#                 if str(file_name) in file_list:
#                     return Response({"Message": "File Already exists"}, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     # After sucessfully uploading
#                     # print(os.listdir(UPLOAD_PATH))
#                     serializer.save()
#                     tp = os.path.join(UPLOAD_PATH, str(file_name))
#                     df1.to_csv(tp, index=False)
#                     return Response({"Message": "Done"}, status=status.HTTP_200_OK)

#             except Exception:
#                 traceback.print_exc()
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
