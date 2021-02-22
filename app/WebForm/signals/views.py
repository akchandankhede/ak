from django.shortcuts import render
from .models import Signal
from .serializers import SignalSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
from django.core.files.base import ContentFile
import json

#  Create your views here.
class SignalViewSet(viewsets.ModelViewSet):
    serializer_class = SignalSerializer
    queryset = Signal.objects.all().order_by('-created_at')
    lookup_field = 'id'

    def list(self, *args, **kwargs):
        signals = Signal.objects.all().order_by('-created_at')
        serializer = SignalSerializer(signals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def retrieve(self, request, id):
        signal = Signal.objects.get(id=id)
        serializer = SignalSerializer(signal)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        if "containerAdopt" in request.data:
            containerAdopt = request.data["containerAdopt"]
            if containerAdopt:
                fraction = request.data["fraction"] if "fraction" in request.data else ''
                containerType = request.data["containerType"] if "containerType" in request.data else ''
                request.data["text"] = request.data["text"] + ' ' + fraction + ' ' + containerType
                
        if "images" in request.data:
            #if type(request.data["images"]) == str:
                #images = json.loads(request.data["images")
            images = request.data["images"]
            print(len(images))
            endpoint = min(3, len(request.data["images"]))
            print("Endpoint : ", endpoint)

            for i in range(0, endpoint):
                image = images[i]
                format, imgstr = image.split(';base64,')
                ext = format.split('/')[-1]
                img = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                name = "file" + str(i+1)
                request.data[name] = img

        if "file" in request.data:
            file = request.data["file"]
            format, imgstr = file.split(';base64,') 
            ext = format.split('/')[-1]
            img = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            request.data["file"] = img

        serializer = SignalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        signal = serializer.save()
        # print(signal)

        data = SignalSerializer(signal).data
        return Response(data, status=status.HTTP_201_CREATED)

