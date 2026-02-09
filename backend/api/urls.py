from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomAuthToken, FileUploadView, HistoryView, ExportPDFView, 
    ExportExcelView, DeleteDatasetView, SignupView, UserProfileView, 
    AnalysisView, LogoutView, ChangePasswordView, CompareDatasetView,
    CustomTokenObtainPairView
)

urlpatterns = [
    # Auth endpoints
    path('signup/', SignupView.as_view(), name='api_signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='api_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    
    # User endpoints
    path('profile/', UserProfileView.as_view(), name='api_profile'),
    path('profile/password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Data endpoints
    path('upload/', FileUploadView.as_view(), name='api_upload'),
    path('analysis/<int:file_id>/', AnalysisView.as_view(), name='api_analysis'),
    path('history/', HistoryView.as_view(), name='api_history'),
    path('compare/', CompareDatasetView.as_view(), name='api_compare'),
    
    # Export endpoints
    path('export/pdf/<int:file_id>/', ExportPDFView.as_view(), name='api_export_pdf'),
    path('export/excel/<int:file_id>/', ExportExcelView.as_view(), name='api_export_excel'),
    
    # Delete endpoint
    path('delete/<int:file_id>/', DeleteDatasetView.as_view(), name='api_delete'),
]