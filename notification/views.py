import json
from django.shortcuts import render
from account.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def notification(request):
    if request.method != "POST":
        return JsonResponse({'message':'only posts'}, status=405)

    data = json.loads(request.body)
    title = data.get("title") 
    summary = data.get("description") 

    if not title  or summary:
        return JsonResponse({'message':'title and summary is required'}, status=400)
    users = User.objects.filter(is_subscribed=True)
    user_email=[]
    for user in users:
        user_email.append(user.email)
        
    email= EmailMessage(subject=title, body=summary, from_email=settings.EMAIL_HOST_USER, to=user_email)
    email.send()
    return JsonResponse({'message':'notification sent'}, status=200)
    

@csrf_exempt
def subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email =data.get("email")
        if not email:
            return JsonResponse({'message':'email is required'}, status=400,)
        user = User.objects.filter(email=email)

        if not user:
            return JsonResponse({'message':'no user found'}, status=400)
        user = User.objects.get(email=email)
        if user.is_subscribed:
            return JsonResponse({'message':'user is already subscribed'}, status=400)
        
        user.is_subscribed=True
        user.save()
        return JsonResponse({'message':'user subscribed'}, status=200)
    users = User.objects.filter(is_subscribed=True)

    subscribers = {
        idx+1:user.email for idx, user in enumerate(users)
    }
    return JsonResponse(json.dumps(subscribers) ,safe=False)

@csrf_exempt
def unsubscription(request):
    if request.method != "POST":
        return JsonResponse({'message':'only posts'}, status=405)

    # email =request.POST.get("email")
    data = json.loads(request.body)
    email =data.get("email")
    if not email:
        return JsonResponse({'message':'email is required'}, status=400)
    user = User.objects.filter(email=email)
    if not user:
        return JsonResponse({'message':'no user found'}, status=400)
    user = User.objects.get(email=email)
    if  not user.is_subscribed:
        return JsonResponse({'message':'user is  not subscribed'}, status=400)
        
    user.is_subscribed=False
    user.save()
    return JsonResponse({'message':'user unsubscribed'}, status=200)