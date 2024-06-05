from django.shortcuts import render
from cryptography.fernet import Fernet
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Notes
from django.http import JsonResponse
from SecureNotes.settings import CRYPTO_KEY
from django.core import serializers





def encryption(text,key):
    encryption_key = Fernet(key)
    encrypted_message = encryption_key.encrypt(text.encode())
    return encrypted_message
    from django.core import serializers


def decryption(text,key):
    decryption_key = Fernet(key)
    decrypted_message = decryption_key.decrypt(text).decode()
    return decrypted_message

def signup(request):

    if request.method == "POST": # user sending data to backend
        print("POST")
        form = UserCreationForm(request.POST) # dict data being send and 
        if form.is_valid():
            print("is valid!!!")
            form.save()
            return redirect('login') # valid then go to login
        else:
            print("is not valid")
    else:
        form = UserCreationForm()
    return render(request,'notes/signup.html',{'form':form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = LoginForm()
    return render(request, 'notes/login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'notes/home.html')

from django.http import JsonResponse

@login_required
def createNotes(request):
    print("WORKS")
    if request.method == "POST":
        title = request.POST.get('title')
        text = request.POST.get('text')
        user = request.user
        encrypted_text = encryption(text, CRYPTO_KEY)
        notes = Notes.objects.create(title=title, text=encrypted_text, user=user)
        notes.save()
        return JsonResponse({'message': "Note created successfully"})
    else:
        return JsonResponse({'message': "Invalid request method"}, status=400)

@login_required    
def displayNotes(request):
    if request.method == "GET":
        user = request.user
        notes = Notes.objects.filter(user=user)
        serialized_notes = serializers.serialize('json', notes)
        return JsonResponse({'message': "Notes successfully listed", 'notes': serialized_notes}, status=200)

    else:
        return JsonResponse({'message': "Invalid request method"}, status=400)


@login_required    
def updateNotes(request):
    noteID = request.GET.get('note_id')
    note = Notes.objects.get(pk=noteID)
    note_data = {
      'pk': note.pk,
      'fields': {
          'title': note.title,
          'text': note.text,
          'date_created': note.date_created.isoformat(),
          'user': note.user.id
      }
    }
    return JsonResponse({'note':note_data})

def changeNotes(request):
  if request.method == 'POST':
      note_id = request.POST.get('note_id')
      title = request.POST.get('title')
      text = request.POST.get('text')

      note = Notes.objects.get(pk=note_id)
      note.title = title
      note.text = text
      note.save()

      return JsonResponse({'success': True})
  else:
      return JsonResponse({'success': False, 'error': 'Invalid request method'}) 

def deleteNotes(request):
  print("deletion working")
  if request.method == 'POST':
    note_id = request.POST.get('note_id')
    try:
      note = Notes.objects.get(id=note_id)
      note.delete()
      return JsonResponse({'success': True})
    except Notes.DoesNotExist:
      return JsonResponse({'success': False, 'error': 'Note not found'})
  else:
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


