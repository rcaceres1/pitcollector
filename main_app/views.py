from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Pit

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def pits_index(request):
    pits = Pit.objects.all()
    return render(request, 'pits/index.html', { 'pits': pits })

def pits_detail(request, pit_id):
    pit = Pit.objects.get(id=pit_id)
    return render(request, 'pits/detail.html', {'pit': pit})

class PitCreate(CreateView):
    model = Pit
    fields = '__all__'
    success_url = '/pits/'

class PitUpdate(UpdateView):
    model = Pit
    fields = ['kind', 'age', 'description']

class PitDelete(DeleteView):
    model = Pit
    success_url = '/pits/'
