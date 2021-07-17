from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from app_blog import views

urlpatterns = [
                  path('registrations/', views.RegistrationsView.as_view(), name='registrations'),
                  path('login/', views.AuthenticatedView.as_view(), name='login'),
                  path('create_blog/', views.CreateBlog.as_view(), name='create_blog'),
                  path('create_blog_csv/', views.CreateBlogWithCsv.as_view(), name='create_blog_csv'),
                  path('logout/', views.Logout.as_view(), name='logout'),
                  path('blog/', views.BlogList.as_view(), name='blog'),
                  path('blog/<int:pk>', views.BlogDetail.as_view(), name='blog'),
                  path('user/<int:pk>', views.UserDetail.as_view(), name='detail_user'),
                  path('image/<int:pk>', views.ImageDetail.as_view(), name='image'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
