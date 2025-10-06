# window_measurement/urls.py
from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [

    path("", FetchCustomerFormData.as_view(), name='fetch-customer-data'),
    path("orders/", CustomerOrderView.as_view(), name='orders'),
    path('product_list/', ProductList.as_view(), name='product_list'),
    path('customer_detail/<int:customer_id>/', CustomerDetailView.as_view(), name='customer_detail'),
    # path('production_detail/<int:customer_id>/', ProductionView.as_view(), name='production_detail'),
    path("add_window_configuration/", AddWindowConfiguration.as_view(), name='add_window_configuration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),

    path('height_add/', AddWindowHeight.as_view(), name='add_window_height'),
    path('height_delete/<int:pk>/', DeleteWindowHeight.as_view(), name='delete_window_height'),

    path('width_add/', AddWindowWidth.as_view(), name='add_window_width'),
    path('width_delete/<int:pk>/', DeleteWindowWidth.as_view(), name='delete_window_width'),

    path('type_add/', AddWindowType.as_view(), name='add_window_type'),
    path('type_delete/<int:pk>/', DeleteWindowType.as_view(), name='delete_window_type'),

    path('series_add/', AddWindowSeries.as_view(), name='add_window_series'),
    path('series_delete/<int:pk>/', DeleteWindowSeries.as_view(), name='delete_window_series'),
    
    path('products_edit/<int:pk>/', EditWindowConfiguration.as_view(), name='edit_window_configuration'),
    
    path('products_delete/<int:pk>/', DeleteWindowConfiguration.as_view(), name='delete_window_configuration'),
    path('update-order-config/', UpdateOrderConfigView.as_view(), name='update_order_config'),
    path('approve_supervisor_order/', ApproveSupervisorOrderView.as_view(), name='approve_supervisor_order'),
    path('production-status-page/<int:order_id>/', ProductionStatusPage.as_view(), name='production-status-page'),
]
