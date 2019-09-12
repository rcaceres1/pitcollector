from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

import boto3
import uuid 

from .models import Pit, Toy, Photo
from .forms import FeedingForm

S3_BASE_URL = 'https://apigateway.us-east-2.amazonaws.com/'
BUCKET = 'rc-cat-collector'

# Create your views here.

class PitCreate(CreateView):
    model = Pit
    fields = ['name', 'kind', 'age', 'description']

class PitUpdate(UpdateView):
    model = Pit
    fields = ['kind', 'age', 'description']

class PitDelete(DeleteView):
    model = Pit
    success_url = '/pits/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def pits_index(request):
    pits = Pit.objects.all()
    return render(request, 'pits/index.html', { 'pits': pits })

def pits_detail(request, pit_id):
    pit = Pit.objects.get(id=pit_id)
    toys_pit_doesnt_have = Toy.objects.exclude(id__in = pit.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'pits/detail.html', {
        'pit': pit, 'feeding_form': feeding_form, 
        'toys': toys_pit_doesnt_have
    })

def add_feeding(request, pit_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.pit_id = pit_id
        new_feeding.save()
    return redirect('detail', pit_id=pit_id)

def assoc_toy(request, pit_id, toy_id):
  Pit.objects.get(id=pit_id).toys.add(toy_id)
  return redirect('detail', pit_id=pit_id)

def unassoc_toy(request, pit_id, toy_id):
  Pit.objects.get(id=pit_id).toys.remove(toy_id)
  return redirect('detail', pit_id=pit_id)

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

def add_photo(request, pit_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, pit_id=pit_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
    return redirect('detail', pit_id=pit_id)