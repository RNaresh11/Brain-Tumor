from django.shortcuts import render,HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from tensorflow.keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from django.contrib.auth.decorators import login_required
import numpy as np
from django.conf import settings

# Create your views here.
def base(request):
    return render(request,"app/home.html")

# @login_required
def home(request):
    return render(request,"app/home1.html")

@login_required
def details(request):
    return render(request,"app/details.html")


model = load_model('models/model.h5')
model_path = os.path.join(settings.BASE_DIR, 'models', 'model.h5')
model = load_model(model_path)
class_labels = ['pituitary', 'glioma', 'notumor', 'meningioma']


def predict_tumor(image_path):
    IMAGE_SIZE = 128
    img = load_img(image_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence_score = np.max(predictions)

    if class_labels[predicted_class_index] == 'notumor':
        return "No Tumor", confidence_score
    else:
        return f"Tumor: {class_labels[predicted_class_index]}", confidence_score

@login_required
def detect(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        result, confidence = predict_tumor(file_path)

        return render(request, 'app/result.html', {
            'result': result,
            'confidence': f"{confidence * 100:.2f}",
            'file_path': fs.url(filename)
        })

    return render(request, 'app/result.html')






from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to dashboard or homepage
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')