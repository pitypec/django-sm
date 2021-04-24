from django.conf import settings
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer, TweetActionSerializer,TweetCreateSerializer


ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.
def home_view(request):
    context = {}
    return render(request, 'sm/index.html', context, status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"Message": "You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"Message": "Tweet removed"}, status=200)

@api_view(['GET'])
def tweet_list_view(request):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def tweet_action_view(request, *args, **kwargs):
    """
     id is required
     Action options are: like, unlike, retweet
    """
    print(request.POST, request.data)
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id = tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
           obj.likes.add(request.user)
           serializer = TweetSerializer(obj)
           return Response(serializer.data, status=200)
        elif action == "unlike":
          obj.likes.remove(request.user)
          serializer = TweetSerializer(obj)
          return Response(serializer.data, status=200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(user=request.user, parent=obj, content= content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({'message': "Likes"}, status=200)

def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)

        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, allowed_hosts=ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    context = {
        "form": form
    }
    return render(request, "sm/components/form.html", context)

def tweet_list_view_pure_django(request):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    consume by javascript or swift
    """
    data = {
       "id": tweet_id,
    }
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
      data['message'] = 'not found'

    return JsonResponse(data)