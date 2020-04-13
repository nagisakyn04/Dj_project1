from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView ,UpdateView ,DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import City
from django.contrib import messages
from .forms import CityForm
from django.core.paginator import Paginator
def home(request):
    #if request.method == 'POST':
     #   form = CityForm(request.POST or None)
    #    if form.is_valid():
     #       print(form.cleaned_data)
   # form= CityForm()
    cities=City.objects.all()
    paginator = Paginator(cities, 10)
    page = request.GET.get('page')
    cities=paginator.get_page(page)
    return render(request, 'cities/home.html',{'objects_list' : cities,})

class CityDetailView(DetailView):
    queryset = City.objects.all()
    context_object_name = 'object'
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin,LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = City
    form_class = CityForm
    template_name ='cities/create.html'
    success_url = reverse_lazy('city:home')
    success_message ='Город успешно создан!'

class CityUpdateView(SuccessMessageMixin,LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = City
    form_class = CityForm
    template_name ='cities/update.html'
    success_url = reverse_lazy('city:home')
    success_message = 'Город успешно отредактирован !'

class CityDeleteView(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = City
    #template_name ='cities/delete.html'
    success_url = reverse_lazy('city:home')

    def get(self, request , *args , **kwargs):
        messages.success(request, 'Город успешно удален!')
        return self.post(request, *args , **kwargs)