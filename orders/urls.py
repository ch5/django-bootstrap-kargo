from django.conf.urls import url
from orders import views as order_views

urlpatterns = [
    url(r'^$', order_views.index, name="index"),
    url(r'^management/$', order_views.management, name="management"),

    url(r'^create_order/$', order_views.create_order, name="create_order"),
    url(r'^edit_order/(?P<uuid>[0-9a-z-]+)/$', order_views.edit_order, name="edit_order"),
    url(r'^delete_order/(?P<uuid>[0-9a-z-]+)/$', order_views.delete_order, name="delete_order"),
]

#########################################################
#              My Taks URL                              #
#########################################################
from orders import views
urlpatterns += [
    url(r'^customers/$', views.vehicle_list, name='vehicle_list'),
    url(r'customers/create/$', views.vehicle_create, name='vehicle_create'),
    url(r'customers/edit/(?P<number>[a-zA-Z0-9]+)/$', views.vehicle_edit, name='vehicle_edit'),
    url(r'customers/delete/(?P<number>[a-zA-Z0-9]+)/$', views.vehicle_delete, name='vehicle_delete'),
]
