from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GeneStorage
import pandas as pd
from django.http import HttpResponse
from apps.utils import allowed_users
# Create your views here.


@login_required(login_url='accounts/login_user')
@allowed_users(allowed_roles=['compute', 'search'])
def search_gene(request):
    context = {
        'segment': 'search',
        'types': ['Chromosome', 'Gene'],
    }
    if request.method == 'POST':
        try:
            search = request.POST.get("search")
            select_type = request.POST.get("type")
            start = request.POST.get('start', default=None)
            end = request.POST.get('end', default=None)
            export = request.POST.get('export')
            columns_required = request.POST.getlist('columns')
            context['sel_type'] = select_type
            context['search'] = search
            context['columns_req'] = columns_required
            context['start'] = start
            context['end'] = end

            if select_type == 'Gene':
                if (search.startswith('"') and search.endswith('"')):
                    search = search.replace('"', '')
                    result = GeneStorage.objects.filter(refGene_gene__icontains=search).values()
                else:
                    result = GeneStorage.objects.filter(refGene_gene__icontains=search).values()
            else:
                result = GeneStorage.objects.filter(chromosome=search, start_pos=start, end_pos=end).values()

            df = pd.DataFrame(list(result))
            df = df.rename({'aug_all': '1000genome'}, axis=1)

            df.dropna(how='all', axis=1, inplace=True)
            context['df_header_all'] = list(df.columns)
            if columns_required != []:
                df.drop(df.columns.difference(columns_required), axis=1, inplace=True)
            else:
                df.drop(df.columns.difference(['chromosome', 'start_pos', 'end_pos', 'observed', 'refGene gene',
                        'zygosity', 'filename', 'count_hom', 'count_het', 'count_total', 'New_allele_frequency']), axis=1, inplace=True)
                
            context['df'] = df.to_dict('records')
            context['df_header'] = list(df.columns)

            if export:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename=exported.csv'
                export = pd.DataFrame(list(result))
                export = export.rename({'aug_all': '1000genome'}, axis=1)
                export.dropna(how='all', axis=1, inplace=True)
                export.to_csv(path_or_buf=response)
                return response

            return render(request, 'home/search.html', context)
        except Exception as e:
            print('[ERROR]:', e)
            context['sel_type'] = 'Chromosome'
            return render(request, 'home/search.html', context)
    else:
        context['sel_type'] = 'Chromosome'
        return render(request, 'home/search.html', context)

