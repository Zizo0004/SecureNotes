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
import logging
logger = logging.getLogger(__name__)

f = Fernet(CRYPTO_KEY)



def encryption(text):
    encrypted_message = f.encrypt(text.encode())
    return encrypted_message

def decryption(encrypted_text):
    x = encrypted_text.encode()
    message = x.replace(b"b'", b"").replace(b"'", b"")
    return f.decrypt(message).decode()



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
    if request.method == "POST":
        title = request.POST.get('title')
        text = request.POST.get('text')
        user = request.user
        print(text)
        encrypted_text = encryption(text)
        print(encrypted_text)
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
        user_notes = []
        for note in notes:
            try:
                decrypted_text = decryption(note.text)
                user_note = {
                    "model": "notes.notes",
                    "pk": note.pk,
                    "fields": {
                        "text": decrypted_text,
                        "title": note.title,
                        "date_created": note.date_created,
                        "user": note.user.id  # Use note.user.id to avoid serializing the entire user object
                    }
                }
                print(user_note)
                user_notes.append(user_note)
            except Exception as e:
                logger.error(f"Error decrypting note ID {note.pk}: {e}")
                return JsonResponse({'message': f"Error decrypting note ID {note.pk}"}, status=500)

        return JsonResponse({'message': "Notes successfully listed", 'notes': user_notes}, status=200)

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
  if request.method == 'POST':
    note_id = request.POST.get('note_id')
    print(request.POST)
    try:
      note = Notes.objects.get(id=note_id)
      note.delete()
      return JsonResponse({'success': True})
    except Notes.DoesNotExist:
      return JsonResponse({'success': False, 'error': 'Note not found'})
  else:
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


"""@login_required    
def displayNotes(request):
    if request.method == "GET":
        user = request.user
        notes = Notes.objects.filter(user=user)
        user_notes = []
        #serialized_notes = serializers.serialize('json', notes)
        #print(serialized_notes)
        for note in notes:
            user = {"model": "notes.notes", "pk":note.pk,"fields":{
                "text":decryption(note.text.encode(),CRYPTO_KEY),"title":note.title,"date_created":note.date_created,"user":note.user
            }}
            user_notes.append(user)
            print(user_notes)
        return JsonResponse({'message': "Notes successfully listed", 'notes': user_notes}, status=200)

    else:
        return JsonResponse({'message': "Invalid request method"}, status=400)"""

"""
@login_required    
def displayNotes(request):
    if request.method == "GET":
        print(f"Decryption Key: {key}")
        user = request.user
        notes = Notes.objects.filter(user=user)
        user_notes = []

        for note in notes:
            try:
                # Debugging: log the encrypted text and the key
                logger.debug(f"Encrypted text (bytes): {note.text.encode()}")
                logger.debug(f"CRYPTO_KEY: {key}")

                decrypted_text = decryption(note.text.encode(), key)
                logger.debug(f"Decrypted text: {decrypted_text}")

                user_note = {
                    "model": "notes.notes",
                    "pk": note.pk,
                    "fields": {
                        "text": decrypted_text,
                        "title": note.title,
                        "date_created": note.date_created,
                        "user": note.user.id  # Use note.user.id to avoid serializing the entire user object
                    }
                }
                user_notes.append(user_note)
            except Exception as e:
                logger.error(f"Error decrypting note ID {note.pk}: {e}")
                return JsonResponse({'message': f"Error decrypting note ID {note.pk}"}, status=500)

        return JsonResponse({'message': "Notes successfully listed", 'notes': user_notes}, status=200)

    else:
        return JsonResponse({'message': "Invalid request method"}, status=400)
"""