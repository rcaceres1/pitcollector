from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


import boto3
import uuid 

from .models import Pit, Toy, Photo
from .forms import FeedingForm

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'rc-cat-collector'

# Create your views here.

class PitCreate(LoginRequiredMixin, CreateView):
    model = Pit
    fields = ['name', 'kind', 'age', 'description']
    
    def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)

class PitUpdate(LoginRequiredMixin, UpdateView):
    model = Pit
    fields = ['kind', 'age', 'description']

class PitDelete(LoginRequiredMixin, DeleteView):
    model = Pit
    success_url = '/pits/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def pits_index(request):
    pits = Pit.objects.filter(user=request.user)
    return render(request, 'pits/index.html', { 'pits': pits })

@login_required
def pits_detail(request, pit_id):
    pit = Pit.objects.get(id=pit_id)
    toys_pit_doesnt_have = Toy.objects.exclude(id__in = pit.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'pits/detail.html', {
        'pit': pit, 'feeding_form': feeding_form, 
        'toys': toys_pit_doesnt_have
    })

@login_required
def add_feeding(request, pit_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.pit_id = pit_id
        new_feeding.save()
    return redirect('detail', pit_id=pit_id)

@login_required
def assoc_toy(request, pit_id, toy_id):
  Pit.objects.get(id=pit_id).toys.add(toy_id)
  return redirect('detail', pit_id=pit_id)

@login_required
def unassoc_toy(request, pit_id, toy_id):
  Pit.objects.get(id=pit_id).toys.remove(toy_id)
  return redirect('detail', pit_id=pit_id)

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)