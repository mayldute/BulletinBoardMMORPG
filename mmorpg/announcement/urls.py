from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import AnnouncementsList, AnnouncementDetail, AnnouncementCreate, AnnouncementUpdate, RespondDetail, ChangeRespondStatusView, ChangeAnnouncementStatusView


urlpatterns = [
   path('', AnnouncementsList.as_view(), name='announcements'), 
   path('<int:pk>/', AnnouncementDetail.as_view(), name='announcement_detail'),
   path('create/', AnnouncementCreate.as_view(), name='announcement_create'),
   path('<int:pk>/update/', AnnouncementUpdate.as_view(), name='announcement_update'),
   path('announcement/<int:pk>/update-status/', ChangeAnnouncementStatusView.as_view(), name='change_announcement_status'),
   path('respond/<int:pk>/', RespondDetail.as_view(), name='respond_detail'),
   path('respond/<int:pk>/update/', ChangeRespondStatusView.as_view(), name='change_respond_status'),
] 