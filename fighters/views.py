from fighters.models import Weightclass
from fighters.models import Fighter
from fighters.serializers import WeightclassSerializer
from fighters.serializers import FighterSerializer
from fighters.serializers import UserSerializer
from fighters.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle
from django.contrib.auth.models import User
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'

class WeightclassList(generics.ListCreateAPIView):
    queryset = Weightclass.objects.all()
    serializer_class = WeightclassSerializer
    name = 'weightclass-list'
    throttle_scope = 'weightclasses'
    throttle_classes = (ScopedRateThrottle,)
    filter_fields = ('name',)
    search_fields = ('name',)
    ordering_fields = ('name',)

class WeightclassDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Weightclass.objects.all()
    serializer_class = WeightclassSerializer
    name = 'weightclass-detail'
    throttle_scope = 'weightclasses'
    throttle_classes = (ScopedRateThrottle,)

class FighterList(generics.ListCreateAPIView):
    queryset = Fighter.objects.all()
    serializer_class = FighterSerializer
    name = 'fighter-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    filter_fields = (
        'name',
        'birthplace',
        'age',
        'height',
        'weight',
        'reach',
        'wins',
        'losses',
        'draws',
        'weightclass'
    )
    search_fields = ('^name',)
    ordering_fields = (
        'name',
        'weightclass',
        )
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FighterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fighter.objects.all()
    serializer_class = FighterSerializer
    name = 'fighter-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'weightclasses': reverse(WeightclassList.name, request=request),
            'fighters': reverse(FighterList.name, request=request),
            'users': reverse(UserList.name, request=request)
        })
