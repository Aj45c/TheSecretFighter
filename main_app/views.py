from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Game,Photo

import boto3
import uuid

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'secretfighter-buck'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def game_index(request):
    games = Game.objects.all()
    return render(request, 'games/index.html', { 'games': games })

@login_required
def game_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'games/detail.html', {'game':game})

@login_required
def add_photo(request, game_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, game_id=game_id)
      photo.save()
    except Exception as error:
      print("Error uploading photo: ", error)
      return redirect('detail', game_id=game_id)
  return redirect('detail', game_id=game_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid - Please Try Again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html' , context)

#===========================================================================
class GamesCreate(LoginRequiredMixin,CreateView):
    model = Game
    fields = ['name', 'release', 'publisher', 'num_of_chars', 'crit_rating','description']
    success_url = '/fighters/'
    def form_valid(self, form):
          form.instance.user = self.request.user
          return super().form_valid(form)

class GamesUpdate(LoginRequiredMixin,UpdateView):
    model = Game
    fields = ['description']

class GamesDelete(LoginRequiredMixin,DeleteView):
    model = Game
    success_url = '/fighters/'
