# window_measurement/urls.py
from django.urls import path
from .views import *

app_name = 'windows'

urlpatterns = [
    path("window-series/", WindowSeriesAPIView.as_view()),
    path("window-types/", WindowTypesAPIView.as_view()),
    path("window-height/", WindowHeightAPIView.as_view()),
    path("window-width/", WindowWidthAPIView.as_view()),
    path("window-details/", WindowDetailsAPIView.as_view()),
    path("customer-details/", CustomerFormData.as_view()),
    path('puffing-options/', PuffingPriceOptionAPIView.as_view(), name='puffing-options'),
    path('surface-treatments/', SurfaceTreatmentAPIView.as_view(), name='surface-treatments'),
    path('wood-lamination-types/', WoodLaminationTypeAPIView.as_view(), name='wood-lamination-types'),
    path('powder-coating-types/', PowderCoatingTypeAPIView.as_view(), name='powder-coating-types'),
    path('powder-coating-colors/', PowderCoatingColorAPIView.as_view(), name='powder-coating-colors'),
    path('fitting-price-options/', FittingPriceOptionAPIView.as_view(), name='fitting-price-options'),


]
