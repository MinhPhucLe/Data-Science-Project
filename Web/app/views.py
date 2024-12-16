from django.shortcuts import render
from django.http import JsonResponse
from .forms import LaptopPredictionForm
from .services import predict_laptop_price
from xgboost import XGBRegressor

def predict_price(request):
    if request.method == 'POST':
        form = LaptopPredictionForm(request.POST)
        if form.is_valid():
            predicted_price = predict_laptop_price(form.cleaned_data)
            return JsonResponse({'predicted_price': predicted_price})
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def home(request):
    form = LaptopPredictionForm(request.POST or None)

    return render(request, 'home.html', {
        'form': form,
    })
