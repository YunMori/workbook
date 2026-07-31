from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "SSAFY 문제집 관리"
admin.site.site_title = "SSAFY 문제집 관리"
admin.site.index_title = "문제 관리"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("exams.urls")),
]
