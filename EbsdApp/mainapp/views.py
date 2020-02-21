from django.shortcuts import render
from .models import *
import pandas as pd
from .opti_code import OptiModel
import pyutilib.subprocess.GlobalData
from .forms import OptionForm

pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False

def start_page(request):
    return render(request, 'mainapp\\start_page.html')


def input_page(request):

    if request.method == 'POST':

        if 'year_file_submit' in request.POST:
            csv_file = request.FILES['t_year_file']
            data = pd.read_csv(csv_file)

            for row in data.itertuples():
                data_for_trfr = Year(year_value=int(row.i_t))
                data_for_trfr.save()
                
        elif 'option_file_submit' in request.POST:
            csv_file = request.FILES['t_option_file']
            data = pd.read_csv(csv_file)

            for row in data.itertuples():
                data_for_trfr = Option(name=str(row.i_op))
                data_for_trfr.save()

        elif 'capital_file_submit' in request.POST:
            csv_file = request.FILES['t_capital_file']
            data = pd.read_csv(csv_file)

            for row in data.itertuples():
                option = Option.objects.get(name=row.i_op)
                year = Year.objects.get(year_value=int(row.i_t))
                
                data_for_trfr = Capital(option=option, year=year, capital_value=row.p_capital)
                data_for_trfr.save()

        elif 'opex_file_submit' in request.POST:
            csv_file = request.FILES['t_opex_file']
            data = pd.read_csv(csv_file)

            for row in data.itertuples():
                option = Option.objects.get(name=row.i_op)
                year = Year.objects.get(year_value=int(row.i_t))

                data_for_trfr = Opex(option=option, year=year, opex_value=row.p_opex)
                data_for_trfr.save()

        elif 'capacity_file_submit' in request.POST:
            csv_file = request.FILES['t_capacity_file']
            data = pd.read_csv(csv_file)

            for row in data.itertuples():
                option = Option.objects.get(name=row.i_op)
                data_for_trfr = Capacity.objects.create(option=option, capacity_value=float(row.p_capacity))
                data_for_trfr.save()
        
        elif 'demand_file_submit' in request.POST:
            csv_file = request.FILES['t_demand_file']
            data = pd.read_csv(csv_file)

            for row in data.itertuples():
                year = Year.objects.get(year_value=int(row.i_t))
                data_for_trfr = Demand.objects.create(year=year, demand_value=float(row.p_demand))
                data_for_trfr.save()
            
    return render(request, 'mainapp\\input_page.html')

def run_page(request):
    result = 'no result'
    if request.method == 'POST':
        i_op = []
        for op in Option.objects.all():
            i_op.append(op.name)

        i_t = []
        for t in Year.objects.all():
            i_t.append(t.year_value)

        p_capital = {}
        p_capital.clear()
        for op in Option.objects.all():
            for t in Year.objects.all():
                p_capital[(op.name, t.year_value)] = Capital.objects.get(option=op, year=t).capital_value

        p_opcost = {}
        p_opcost.clear()
        for op in Option.objects.all():
            for t in Year.objects.all():
                p_opcost[(op.name, t.year_value)] = Opex.objects.get(option=op, year=t).opex_value

        p_capacity = {}
        p_capacity.clear()
        for op in Option.objects.all():
            p_capacity[op.name] = Capacity.objects.get(option=op).capacity_value

        p_demand = {}
        p_demand.clear()
        for t in Year.objects.all():
            # year = Year.objects.get(year_value=t.year_value)
            p_demand[t.year_value] = Demand.objects.get(year=t).demand_value
        
        run = OptiModel(i_op, i_t, p_capital, p_opcost, p_capacity, p_demand)
        run.run_model()
        result = str(run.m.obj.expr())    
        # result = str(run.m.i_t.value)

        # output results to django model
        util = run.write_results()
        for op in Option.objects.all():
            for t in Year.objects.all():
                Utilisation.objects.update_or_create(
                    option=op, 
                    year=t, 
                    util_value=util[op.name, t.year_value]
                )

    return render(request, 'mainapp\\run_page.html', {'result': result})


def output_page(request):
    form = OptionForm(request.POST)
    years = []
    values = []
    if request.method == 'POST':
        if form.is_valid():
            years = [t.year_value for t in Year.objects.all()]
            op_choice = request.POST['options']
            
            values = []
            for t in years:
                year = Year.objects.get(year_value=t)
                option = Option.objects.get(pk=op_choice)
                values.append(Utilisation.objects.get(option=option, year=year).util_value)

    return render(
        request, 
        'mainapp\\output_page.html', 
        {'form': form, 'years': years, 'values': values}
    )
