from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import filters, status

from premises.models import Contention, Premise
from .serializers import (ContentionSerializer, PremisesSerializer,
                          PremiseReportSerializer)
from premises.utils import int_or_default
from premises.signals import supported_a_premise
from api.v1.users.serializers import UserProfileSerializer
from newsfeed.models import Entry


class ContentionViewset(viewsets.ModelViewSet):
    queryset = Contention.objects.filter(is_published=True)\
                                 .prefetch_related('premises',
                                                   'premises__supporters')\
                                 .select_related('user', 'premises__parent',
                                                 'premises__user')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ContentionSerializer
    paginate_by = 20
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    search_fields = ('title',)
    filter_fields = ('is_featured',)
    ordering_fields = ('date_creation',)

    @detail_route()
    def premises(self, request, pk=None):
        contention = self.get_object()
        serializer = PremisesSerializer(
            contention.premises.select_related('user').all(), many=True)
        return Response(serializer.data)

    def create_argument(self, request):
        serializer = self.serializer_class(
            data=request.data, initial={'ip': request.META['REMOTE_ADDR'],
                                        'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_owner_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg],
            'user': self.request.user
        }
        obj = get_object_or_404(Contention.objects.all(), **filter_kwargs)
        return obj

    def update_argument(self, request, pk=None):
        contention = self._get_owner_object()
        serializer = self.serializer_class(data=request.DATA,
                                           instance=contention)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_argument(self, request, pk=None):
        contention = self._get_owner_object()
        Entry.objects.delete(contention.get_newsfeed_type(), contention.id)
        contention.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route()
    def create_premise(self, request, pk=None):
        contention = self.get_object()
        serializer = PremisesSerializer(
            data=request.data, initial={'ip': request.META['REMOTE_ADDR'],
                                        'user': request.user,
                                        'argument': contention})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PremiseViewset(viewsets.ModelViewSet):
    queryset = Premise.objects.filter(is_approved=True)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PremisesSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'premise_id'

    def filter_queryset(self, queryset):
        argument_id = int_or_default(self.kwargs.get('pk'), default=0)
        return queryset.filter(argument__id=argument_id,
                               argument__is_published=True)

    @detail_route(methods=['post'])
    def report(self, request, pk=None, premise_id=None):
        premise = self.get_object()
        if premise.reports.filter(reporter=request.user).exists():
            return Response({'message': 'Onermeyi Zaten Rapor ettin.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = PremiseReportSerializer(
            data=request.data, initial={'reporter': request.user,
                                        'premise': premise,
                                        'contention': premise.argument})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_owner_object(self):
        argument_id = int_or_default(self.kwargs.get('pk'), default=0)
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg],
            'argument__id': argument_id,
            'user': self.request.user
        }
        obj = get_object_or_404(Premise.objects.all(), **filter_kwargs)
        return obj

    def update_premise(self, request, pk=None, premise_id=None):
        premise = self._get_owner_object()
        serializer = self.serializer_class(data=request.DATA,
                                           instance=premise)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_premise(self, request, pk=None, premise_id=None):
        premise = self._get_owner_object()
        premise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PremiseSupportViewset(PremiseViewset):

    @detail_route(methods=['post'])
    def support(self, request, pk=None, premise_id=None):
        premise = self.get_object()
        if premise.supporters.filter(id=request.user.id).exists():
            return Response({'message': "Onermeyi Zaten destekliyorsun"},
                            status=status.HTTP_400_BAD_REQUEST)
        premise.supporters.add(request.user)
        supported_a_premise.send(sender=self, premise=premise,
                                 user=self.request.user)
        return Response(status=status.HTTP_201_CREATED)

    @detail_route(methods=['get'])
    def supporters(self, request, pk=None, premise_id=None):
        premise = self.get_object()
        page = self.paginate_queryset(premise.supporters.all())
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)

    @detail_route(methods=['delete'])
    def unsupport(self, request, pk=None, premise_id=None):
        premise = self.get_object()
        if not premise.supporters.filter(id=request.user.id).exists():
            return Response({'message': "Once onermeyi desteklemen gerekiyor"},
                            status=status.HTTP_400_BAD_REQUEST)
        premise.supporters.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


contention_list = ContentionViewset.as_view(
    {'get': 'list', 'post': 'create_argument'}
)
contention_detail = ContentionViewset.as_view(
    {'get': 'retrieve', 'put': 'update_argument',
     'delete': 'delete_argument'}
)
premises_list = ContentionViewset.as_view(
    {'get': 'premises', 'post': 'create_premise'}
)
premise_detail = PremiseViewset.as_view(
    {'get': 'retrieve', 'put': 'update_premise',
     'delete': 'delete_premise'}
)
premise_report = PremiseViewset.as_view(
    {'post': 'report'}
)
premise_support = PremiseSupportViewset.as_view(
    {'post': 'support', 'delete': 'unsupport'}
)
premise_supporters = PremiseSupportViewset.as_view(
    {'get': 'supporters'},
    serializer_class=UserProfileSerializer
)
