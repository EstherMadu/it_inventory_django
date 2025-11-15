from django.urls import path
from base.views.admin_views import (admin_signup,admin_login,admin_dashboard, admin_manage_vendors, admin_delete_vendor,
admin_add_vendor, view_vendor_assets, admin_logout)
from base.views.asset_views import admin_manage_assets, admin_add_asset, admin_change_asset_status, admin_delete_asset
from base.views.assignment_views import admin_view_assignments, admin_assign_asset
from base.views.history_views import admin_view_status_history
from base.views.vendor_views import vendor_dashboard,vendor_login,vendor_logout 
from base.views.base_views  import home




urlpatterns = [
    path("", home, name="home"),
    path('admin/signup/',admin_signup, name= "admin_signup"),
    path('admin/login', admin_login, name="admin_login"),
    path('admin/dasboard', admin_dashboard, name="admin_dashboard"),
    path('admin/manage/vendors', admin_manage_vendors, name="admin_manage_vendors" ),
    path('admin/manage/asset', admin_manage_assets, name="admin_manage_assets" ),
    path('admin/add/asset', admin_add_asset, name="admin_add_asset" ),
    path('admin/view/assignment', admin_view_assignments, name="admin_view_assignments" ),
    path('admin/add/vendors', admin_add_vendor, name="admin_add_vendor" ),
    path('admin/delete/vendor/<str:id>', admin_delete_vendor, name="admin_delete_vendor"),
    path('admin/vendor/asset/<str:vendor_id>', view_vendor_assets, name="view_vendor_assets"),
    path('admin/change/status/<str:asset_id>', admin_change_asset_status, name="admin_change_asset_status"),
    path('admin/assign/asset/<str:asset_id>', admin_assign_asset, name="admin_assign_asset"),
    path('admin/delete/asset/<str:asset_id>', admin_delete_asset, name="admin_delete_asset"),
    path('admin/status/<str:asset_id>', admin_view_status_history, name="admin_view_status_history"),
    path('admin/view/assignment/<str:asset_id>', admin_view_assignments, name="admin_view_assignments"),
    path('admin/logout', admin_logout, name="admin_logout"),
    path("vendor/login", vendor_login, name="vendor_login"),
    path("vendor/dashboard", vendor_dashboard, name="vendor_dashboard"),
    path("vendor/logout", vendor_logout, name="vendor_logout"),
    path("admin/history/<str:asset_id>", admin_view_status_history, name="admin_view_status_history"),


    
    
  
]