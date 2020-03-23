from django.shortcuts import render
from .forms import *
from django.contrib import messages
from trains.models import Train

def get_graph():
    qs = Train.objects.values('from_city')
    from_city_set = set(i['from_city'] for i in qs)
    graph = {}
    for city in from_city_set:
        trains = Train.objects.values('to_city')
        tmp = set(i['to_city'] for i in trains)
        graph[city] = tmp
    return  graph


def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex]- set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))

def home(request):
    form = RouteForm()
    return render(request,'routes/home.html', {'form':form})

def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            #assert False
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities_form = data['across_cities']
            traveling_time = data['travel_time']
            graph = get_graph()
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
            if len(all_ways) == 0:
                messages.error(request, 'Маршрута удовлетворяющим условиям не существует')
                return render(request, 'routes/home.html', {'form': form})
            if across_cities_form:
                across_cities = [city.id for city in across_cities_form]
                right_ways = []
                for way in all_ways:
                    if all(point in way for point in across_cities):
                        right_ways.append(way)
                    if not right_ways:
                        messages.error(request, 'Маршрут через эти города невозможен')
                        return render(request, 'routes/home.html', {'form': form})
            else:
                right_ways = all_ways
            trains = []
            for route in trains:
                tmp = {}
                tmp['trains'] = []
                total_time = 0
                for index in range(len(route)-1):
                    qs = Train.objects.filter(from_city = route[index], to_city = route[index + 1])
                    qs = qs.oreder_by('travel_time').first()
                    total_time += qs.travel_time
                tmp['total_time'] = total_time
                if total_time <= traveling_time:
                    trains.append(tmp)
            if not trains:
                messages.error(request, 'Время в пути больше заданного')
                return render(request, 'routes/home.html', {'form': form})
            context = {}
            form = RouteForm()
            context['form'] = form
            context['ways'] = trains
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form':form})
    else:
        messages.error(request, 'Создайте маршрут')
        form = RouteForm()
        return render(request, 'routes/home.html',{'form':form})

