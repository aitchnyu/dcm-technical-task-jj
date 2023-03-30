from django.urls import path

from .views import TestFileUploadAPIView, TestRunRequestAPIView, TestRunRequestItemAPIView, AssetsAPIView

urlpatterns = [
    path('assets', AssetsAPIView.as_view(), name='assets'),
    path('test-file', TestFileUploadAPIView.as_view(), name='test_file'),
    path('test-run', TestRunRequestAPIView.as_view(), name='test_run_req'),
    path('test-run/<pk>', TestRunRequestItemAPIView.as_view(), name='test_run_req_item'),
]
