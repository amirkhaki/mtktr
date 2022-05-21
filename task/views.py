from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404, redirect 
from django.http import Http404
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.cache import cache
import json
import requests
import os
import datetime
from .serializers import (
        TelegramAccountSerializer, TelegramTaskSerializer,
        DiscordAccountSerializer, DiscordTaskSerializer)
from .models import TelegramAccount, TelegramTask, DiscordAccount, DiscordTask
from . import permissions

class DiscordTaskViewSet(mixins.RetrieveModelMixin,
        GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DiscordTaskSerializer

    def get_queryset(self):
        queryset = DiscordTask.objects.exclude(count=0)
        return queryset

    @action(methods=['get'], detail=False,
            url_path='list/(?P<acid>[0-9]+)')
    def tlist(self, request, acid=None, *arg, **kwarg):
        """
        show tasks not performed by acid
        """
        dcaccount = get_object_or_404(DiscordAccount, pk=acid, owner=request.user)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.exclude(performers__in=[dcaccount])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serilizer = self.get_serialzer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def _add_to_guild(self, access_token, guild_id, user_id):
        url = f'{settings.DC_API_BASE_URL}/guilds/{guild_id}/members/{user_id}'
        data = {
                'access_token': access_token 
                }
        headers = {
                'Authorization': f'Bot {settings.DC_BOT_TOKEN}',
                'Content-Type': 'application/json'
                }
        response = requests.put(url=url, headers=headers, json=data)
        response.raise_for_status()
        return


    @action(methods=['post'], detail=True,
            url_path='perform/(?P<acid>[0-9]+)')
    def perform_task(self, request, pk=None, acid=None):
        dcaccount = get_object_or_404(DiscordAccount, pk=acid, owner=request.user)
        task = self.get_object()
        if task.performers.filter(pk=dcaccount.pk).exists():
            raise Http404("You performed this before")
        if dcaccount.is_expired():
            dcaccount.refresh()
        try:
            self._add_to_guild(dcaccount.access_token, task.guild_id, dcaccount.did)
        except Exception as e:
            return Response({'success': False})
        return Response({'success': True})


class DiscordAccountViewSet(mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    permission_classes = [permissions.IsAdminOrOwner]
    serializer_class = DiscordAccountSerializer
    queryset = DiscordAccount.objects.all()

    @action(methods=['get'], detail=False)
    def add(self, request):
        state = get_random_string(21)
        request.session['state'] = state
        url = settings.DC_AUTHORIZATION_BASE_URL+'?'+f'response_type=code&client_id={settings.DC_OAUTH2_CLIENT_ID}&scope=identify+guilds.join&state={state}&redirect_uri={settings.DC_OAUTH2_REDIRECT_URI}&prompt=consent'
        return redirect(url)

    def _exchange_code(self, code):
        data = {
                'client_id': settings.DC_OAUTH2_CLIENT_ID,
                'client_secret': settings.DC_OAUTH2_CLIENT_SECRET,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': settings.DC_OAUTH2_REDIRECT_URI
                }
        headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
                }
        r = requests.post(settings.DC_TOKEN_URL, data=data, headers=headers)
        r.raise_for_status()
        return r.json()

    def _get_user(self, access_token):
        url = f'{settings.DC_API_BASE_URL}/users/@me'
        headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
                }
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()


    @action(methods=['get'], detail=False)
    def callback(self, request):
        code = request.GET.get('code', None)
        state = request.GET.get('state', None)
        print(code, "  ", state, " ", request.session.get('state', None))
        if not code:
            raise Http404('no code')
        if not state:
            raise Http404('no state')
        if state != request.session.get('state'):
            raise Http404('state and session state are not same')
        token = self._exchange_code(code)
        exp_date = datetime.datetime.now() + datetime.timedelta(seconds=token['expires_in']-4)
        user = self._get_user(token['access_token'])
        if DiscordAccount.objects.filter(did=user['id']).exists():
            return redirect(settings.DC_REDIRECT_TO)
        dc = DiscordAccount()
        dc.owner = request.user
        dc.access_token = token['access_token']
        dc.refresh_token = token['refresh_token']
        dc.expire_date = exp_date
        dc.did = user['id']
        dc.username = user['username']+'#'+user['discriminator']
        dc.save()
        return redirect(settings.DC_REDIRECT_TO)




class TelegramAccountViewSet(mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    queryset = TelegramAccount.objects.all()
    serializer_class = TelegramAccountSerializer
    permission_classes = [permissions.IsAdminOrOwner]

    @action(methods=['post'], detail=True, permission_classes=[AllowAny],
            url_path='verify/(?P<token>[0-9a-zA-Z]+)')
    def verify(self, request, pk=None, token=None):
        #TODO limit this endpoint to pymtktr
        body = json.loads(request.body)
        acc = get_object_or_404(self.get_queryset(), pk=pk,
                token=token, username=body['username'], verified=False)
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
            url_path='list/(?P<acid>[0-9]+)')
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


    @action(methods=['get'], detail=False, url_path='invite')
    def get_invite_code(self, request, pk=None):
        t = self.get_object()
        if t.task_type is 'channel':
            return Response({'error':'yoy can not invite to channel'})
        return Response({'code': f'{request.user.pk}'})

    @action(methods=['post'], detail=False, url_path='invite')
    def set_invite_code(self, request):
        req = json.loads(request.body)
        t = get_object_or_404(TelegramTask, chat_id=req['chat_id'])
        if t.count == 0:
            raise Http404()
        u = get_object_or_404(get_user_model(), pk=req['code'])
        t.count -= 1
        u.credit += t.cpp
        t.save()
        u.save()
        return Response({'done': True})
        
        









