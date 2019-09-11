from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Pit
from .forms import FeedingForm

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
    feeding_form = FeedingForm()
    return render(request, 'pits/detail.html', 
    {'pit': pit, 'feeding_form': feeding_form}
    )

def add_feeding(request, pit_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.pit_id = pit_id
        new_feeding.save()
    return redirect('detail', pit_id=pit_id)

class PitCreate(CreateView):
    model = Pit
    fields = '__all__'

class PitUpdate(UpdateView):
    model = Pit
    fields = ['kind', 'age', 'description']

class PitDelete(DeleteView):
    model = Pit
    success_url = '/pits/'
