from rest_framework import generics
from django.utils import translation
from .models import Course
from .serializers import CourseSerializer


def activate_request_language(request):
    # Priority: ?lang= -> Accept-Language -> default (ru)
    lang_param = request.query_params.get('lang') if hasattr(request, 'query_params') else request.GET.get('lang')
    if lang_param:
        translation.activate(lang_param)
        request.LANGUAGE_CODE = lang_param
        return
    # Fallback to header
    header = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if header:
        # simple parse of first language
        preferred = header.split(',')[0].split(';')[0].strip()
        if preferred:
            translation.activate(preferred)
            request.LANGUAGE_CODE = preferred
            return
    translation.activate('ru')
    request.LANGUAGE_CODE = 'ru'


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        activate_request_language(request)
        return super().get(request, *args, **kwargs)


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        activate_request_language(request)
        return super().get(request, *args, **kwargs)
from django.shortcuts import render

# Create your views here.
