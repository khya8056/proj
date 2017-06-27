from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^login$',views.LoginFormView.as_view(),name='login'),
    url(r'^logout$',views.logout,name='logout'),
    url(r'^register$',views.RegisterFormView.as_view()),
    url(r'^admin_home$',views.AdminHomeView.as_view(),name='admin_home'),
    url(r'^admin_home/create_proj$',views.CreateProjectView.as_view()),
    url(r'^student_home$',views.StudentHomeView.as_view()),
    url(r'^student_home/project$',views.ProjectView.as_view()),
    url(r'^admin_home/addproject$',views.CreateProjectView.as_view(),name='addproject'),
    url(r'^student_home/add_member$',views.AddMemberView.as_view()),
    url(r'^student_home/add_member_as_leader$',views.AddMemberAsLeaderView.as_view()),
    #url(r'^student_home/leader_add_member$',views.LeaderAddMemberView.as_view()),
    url(r'^student_home/upload_file$',views.upload_handler),
    url(r'^student_home/add_team$',views.AddTeamView.as_view()),
    url(r'^admin_home/upload_file$',views.upload_handler,name='upload_file'),
    url(r'^admin_home/download_file$',views.download_handler),
    url(r'^student_home/view_files$',views.files_view),
    url(r'^student_home/download_file$',views.download_handler),
    url(r'^student_home/send$', views.send, name='send'),
    url(r'^admin_home/send$', views.send, name='send'),
    url(r'^notification$', views.notif, name='notif'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^admin_home/deleteproject$', views.delproj.as_view(), name='delproj'),
    url(r'^student_home/del_team$',views.del_team , name="del_team"),
    url(r'^student_home/del_team_mem$', views.del_team_mem, name="del_team"),
    url(r'^changepass$', views.changepass, name='changepass'),
    url(r'^upload_pic$', views.upload_pic, name='upload_pic'),
    url(r'^user/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/home/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/home/user/password/done/'}),
    url(r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    