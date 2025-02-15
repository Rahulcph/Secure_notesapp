from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Homepage
def home(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user)
    else:
        notes = []
    return render(request, 'vault/home.html', {'notes': notes})

# Add a note
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')
    else:
        form = NoteForm()
    return render(request, 'vault/add_note.html', {'form': form})

# Encrypt a note
def encrypt_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = iv + encryptor.update(note.plaintext.encode()) + encryptor.finalize()
    note.ciphertext = ciphertext.hex()
    note.plaintext = None
    note.save()
    return redirect('home')

# Decrypt a note
def decrypt_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    key = os.urandom(32)  # Replace with actual key management logic
    iv = bytes.fromhex(note.ciphertext[:32])
    ciphertext = bytes.fromhex(note.ciphertext[32:])
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    note.plaintext = (decryptor.update(ciphertext) + decryptor.finalize()).decode()
    note.save()
    return redirect('home')
