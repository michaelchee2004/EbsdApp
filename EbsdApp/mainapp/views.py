from django.shortcuts import render
from .models import *
import pandas as pd
from .opti_code import OptiModel
import pyutilib.subprocess.GlobalData

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
        
    #     i_t = []
        # for t in Year.objects.all():
        #     print(type(t.year_value))

        p_capital = {}
        p_capital.clear()
        for op in Option.objects.all():
            for t in Year.objects.all():
                option = Option.objects.get(name=op.name)
                year = Year.objects.get(year_value=t.year_value)
                p_capital[(option.name, year.year_value)] = Capital.objects.get(option=option, year=year).capital_value

        # p_capital = {
        #     ('op1', 2020): 100,
        #     ('op2', 2020): 200,
        #     ('op3', 2020): 300
        # }

        p_opcost = {}
        p_opcost.clear()
        for op in Option.objects.all():
            for t in Year.objects.all():
                option = Option.objects.get(name=op.name)
                year = Year.objects.get(year_value=t.year_value)
                p_opcost[(option.name, year.year_value)] = Opex.objects.get(option=option, year=year).opex_value

        # p_opcost = {
        #     ('op1', 2020): 50,
        #     ('op2', 2020): 20,
        #     ('op3', 2020): 10
        # }

        p_capacity = {}
        p_capacity.clear()
        for op in Option.objects.all():
            option = Option.objects.get(name=op.name)
            p_capacity[option.name] = Capacity.objects.get(option=option).capacity_value

        # p_capacity = {
        #     'op1': 80,
        #     'op2': 70,
        #     'op3': 40
        # }

        p_demand = {}
        p_demand.clear()
        for t in Year.objects.all():
            year = Year.objects.get(year_value=t.year_value)
            p_demand[year.year_value] = Demand.objects.get(year=year).demand_value

        # p_demand = {
        #     2020: 170
        # }
        
        run_instance = OptiModel(i_op, i_t, p_capital, p_opcost, p_capacity, p_demand)
        run_instance.run_model()
        result = str(run_instance.m.obj.value())

    # myyear = Year.objects.get(year_value=2020).id
    # myoption = Option.objects.get(name='op01').id
    # p_capital = {}
    # for op in Option.objects:
    #     for t in Year.objects:
    #         option_id = op.id
    #         year_id = t.id
    #         p_capital[(op, t)] = Capital.objects.get(
    #             option=option_id, year=year_id)

    # result = p_capital
    

    return render(request, 'mainapp\\run_page.html', {'result': result})
