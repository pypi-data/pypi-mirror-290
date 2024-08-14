__all__ = [
    'pull_model_data', 'digest_model',
    'pull_model', 'push_model',
    'SyncViewSet',
]

import requests
from urllib.parse import urljoin

from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


def pull_model_data(api_url, auth=None, id=None, **params):
    is_list = id is None
    if is_list:
        url = api_url  # Restful List
    else:
        url = urljoin(api_url, f'{id}/')  # Restful Detail
    r = requests.get(url, params=params, auth=auth)
    r.raise_for_status()
    data = r.json()
    if is_list and isinstance(data, dict):
        # paginated result
        if 'results' in data:  # DRF style
            return data['results']
        elif 'data' in data:  # other style
            return data['data']
        else:  # by guess
            for value in data.values():
                if isinstance(value, list):
                    return value
        return []
    else:
        return data


def digest_model(model_class, serializer_class, data, id_field='id'):
    if isinstance(data, list):
        instances = []
        for item in data:
            try:
                instance = digest_model(model_class, serializer_class, data=item, id_field=id_field)
                instances.append(instance)
            except Exception as e:
                print(e)
        return instances

    try:
        instance = model_class.objects.get(id=data[id_field])
        serializer = serializer_class(instance, data=data)
        action = 'Updating'
    except model_class.DoesNotExist:
        serializer = serializer_class(data=data)
        action = 'Syncing'

    print(f"{action} {model_class.__name__} {data[id_field]} {getattr(data, 'name', '')}")

    if serializer.is_valid(raise_exception=True):
        return serializer.save()


def pull_model(model_class, serializer_class, api_url, auth=None, id=None, data=None, id_field='id', **params):
    if not data:
        data = pull_model_data(api_url, auth=auth, id=id, **params)

    return digest_model(model_class, serializer_class, data=data, id_field=id_field)


def push_model(instance, serializer_class, api_url, auth=None):
    data = serializer_class(instance).data
    id = instance.pk
    url = urljoin(api_url, f'{id}/')  # Restful Detail
    r = requests.put(url, json=data, auth=auth)
    r.raise_for_status()
    return r.json()


class SyncViewSet(ModelViewSet):
    def update(self, request, *args, **kwargs):
        """Auto treat create / update, and partial is prefered"""

        partial = kwargs.pop('partial', True)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Http404:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
