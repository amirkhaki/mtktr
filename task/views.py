from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings
from django.core.cache import cache
import json
import requests
from .serializers import TelegramAccountSerializer, TelegramTaskSerializer
from .models import TelegramAccount, TelegramTask
from . import permissions

class TelegramAccountViewSet(mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    queryset = TelegramAccount.objects.all()
    serializer_class = TelegramAccountSerializer
    permission_classes = [permissions.IsAdminOrOwner]

    @action(methods=['post'], detail=True,
            url_path='verify/(?P<token>[0-9a-zA-Z]+)')
    def verify(self, request, pk=None, token=None):
        #TODO limit this endpoint to pymtktr
        acc = get_object_or_404(self.get_queryset(), pk=pk,
                token=token, verified=False)
        body = json.loads(request.body)
        acc.tid = body['tid']
        acc.verified = True
        acc.save()
        return Response({'verified':True})

class TelegramTaskViewSet(mixins.RetrieveModelMixin,
        GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TelegramTaskSerializer

    def get_queryset(self):
        queryset = TelegramTask.objects.exclude(count=0)
        return queryset

    @action(methods=['get'], detail=False,
            url_path='(?P<acid>[0-9]+)')
    def tlist(self, request, acid=None, *arg, **kwarg):
        """
        show tasks not performed by acid
        """
        tgaccount = get_object_or_404(TelegramAccount, pk=acid, owner=request.user)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.exclude(performers__in=[tgaccount])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serilizer = self.get_serialzer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True,
            url_path='start/(?P<acid>[0-9]+)')
    def start_task(self, request, pk=None, acid=None):
        tgaccount = get_object_or_404(TelegramAccount, pk=acid, owner=request.user)
        task = self.get_object()
        if task.performers.filter(pk=tgaccount.pk).exists():
            raise Http404("You performed this before")
        key = str(tgaccount.pk)+'+'+str(task.pk)
        sentinel = object()
        if cache.get(key, sentinel) is not sentinel:
            cache.set(key, None, settings.WAIT_DURATION)
        # check if account doesn't exist in channel
        # if exists, add to performers and return error
        if task.task_type == 'channel':
            endpoint = 'ischannelmember'
        else:
            endpoint = 'isgroupmember'
        url = f'{settings.TG_URL}/{endpoint}?u={tgaccount.tid}&ch={task.chat_id}'
        resp = requests.post(url).json()
        if resp['ismember']:
            task.performers.add(tgaccount)
            return Response({'success':False, 'error':'joined before'})
        exp_time = cache._expire_info.get(cache.make_key(key))
        return Response({'success':True, 'ends':exp_time})


    @action(methods=['post'], detail=True,
            url_path='perform/(?P<acid>[0-9]+)')
    def perform_task(self, request, pk=None, acid=None):
        tgaccount = get_object_or_404(TelegramAccount, pk=acid, owner=request.user)
        task = self.get_object()
        if task.performers.filter(pk=tgaccount.pk).exists():
            raise Http404("You performed this before")
        key = str(tgaccount.pk)+'+'+str(task.pk)
        sentinel = object()
        if cache.get(key, sentinel) is sentinel:
            raise Http404("first start the task")
        if task.task_type == 'channel':
            endpoint = 'ischannelmember'
        else:
            endpoint = 'isgroupmember'
        url = f'{settings.TG_URL}/{endpoint}?u={tgaccount.tid}&ch={task.chat_id}'
        resp = requests.post(url).json()
        if not resp['ismember']:
            return Response({'success':False, 'error': 'user has not joined'})
        task.performers.add(tgaccount)
        tgaccount.owner.credit += task.cpp
        tgaccount.owner.save()
        return Response({'success': True})










