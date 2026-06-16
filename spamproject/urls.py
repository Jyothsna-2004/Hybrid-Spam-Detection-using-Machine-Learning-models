"""
URL configuration for spamproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from adminapp import views as admin_views
from userapp import views as user_views 

urlpatterns = [
    # User Urls
    # ---------
    path('admin/', admin.site.urls),
    path('', user_views.user_index, name = 'index'),
    path('about/', user_views.user_about, name = 'about'),
    path('blog/', user_views.user_blog, name = 'blog'),
    path('user/', user_views.user_userlogin, name ='user'),
    path('register/', user_views.user_register, name = 'register'),
    path("usadminus/", user_views.user_admin, name="admin"),
    path('dashboard/',user_views.user_dashboard, name = 'dashboard'),
    path('feedbacku/',user_views.user_feedback, name = 'feedback'),
    path('detection/',user_views.user_detection, name = 'detection'),
    path('contact/',user_views.user_contact, name = 'contact'),
    path('otp/',user_views.user_otp, name = 'otp'),
    path('userlogout/', user_views.userlogout, name = 'userlogout'),
    path('myprofile/',user_views.user_myprofile, name = 'myprofile'),
    path('result/',user_views.user_result, name = 'result'),

    # Admin Urls
    # ----------
    path('admin_dashboard',admin_views.admin_dashboard,name='admin_dashboard'),
    path('adminpendingusers',admin_views.adminpendingusers, name="adminpendingusers"),
    path('adminallusers',admin_views.adminallusers,name='adminallusers'),
    path('uploaddataset',admin_views.uploaddataset,name='uploaddataset'),
    path('viewdataset',admin_views.viewdataset,name='viewdataset'),
    path('xgboost',admin_views.xgboost,name='xgboost'),
    path('adaboost',admin_views.adaboost,name='adaboost'),
    path('knn',admin_views.knn,name='knn'),
    path('logistic',admin_views.logistic,name='logistic'),
    path('decision',admin_views.decision,name='decision'),
    path('gradient',admin_views.gradient,name='gradient'),
    path('randomforest',admin_views.randomforest,name='randomforest'),   
    path('admin_graph',admin_views.admin_graph,name='admin_graph'),
    path("admin-change-status/<int:id>",admin_views.Change_Status,name="change_status"),
    path('user_feedbacks',admin_views.user_feedbacks,name='user_feedbacks'),
    path('user_sentiment',admin_views.user_sentiment,name='user_sentiment'),
    path('user_graph',admin_views.user_graph,name='user_graph'),
    path('delete-dataset/<int:id>', admin_views.delete_dataset, name = 'delete_dataset'),
    path('GRADIENT_btn', admin_views.gradient_btn, name='gradient_btn'),

    path('adminlogout',admin_views.adminlogout, name='adminlogout'),
    path('accept-user/<int:id>', admin_views.accept_user, name = 'accept_user'),
    path('reject-user/<int:id>', admin_views.reject_user, name = 'reject'),
    path('delete-user/<int:id>', admin_views.delete_user, name = 'delete_user'),
    path('admin_dataset_btn',admin_views.admin_dataset_btn,name='admin_dataset_btn'),
    path('adminlogout',admin_views.adminlogout, name='adminlogout'),
    path('view_view/', admin_views.view_view, name='view_view'),
    path('XGBOOST_btn', admin_views.XGBOOST_btn, name='XGBOOST_btn'),
    path('ADABoost_btn', admin_views.ADABoost_btn, name='ADABoost_btn'),
    path('KNN_btn', admin_views.KNN_btn, name='KNN_btn'),
    path('SVM_btn', admin_views.SVM_btn, name='SVM_btn'),
    path('Decisiontree_btn', admin_views.Decisiontree_btn, name='Decisiontree_btn'),
    path('logistic_btn', admin_views.logistic_btn, name='logistic_btn'),
    path('randomforest_btn', admin_views.randomforest_btn, name='randomforest_btn'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
