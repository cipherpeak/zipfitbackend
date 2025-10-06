from rest_framework import serializers
from .models import *




class PuffingPriceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuffingPriceOption
        fields = '__all__'

class SurfaceTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurfaceTreatment
        fields = '__all__'

class WoodLaminationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WoodLaminationType
        fields = '__all__'

class PowderCoatingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowderCoatingType
        fields = '__all__'

class PowderCoatingColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowderCoatingColor
        fields = '__all__'



class FittingPriceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FittingPriceOption
        fields = '__all__'


class WindowSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowSeries
        fields = ['name']


class WindowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowType
        fields = ['name', 'icon']


class WindowHeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowHeight
        fields = ['name']



class WindowWidthSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowWidth
        fields = ['name']


class WindowConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowConfiguration
        fields = ['id', 'image', 'rate_per_Sq_Feet', 'gst_amount', 'total_amount', 'notes']

class CustomerEnquirySerializer(serializers.ModelSerializer):
    window_model = WindowConfigurationSerializer()
    surface_treatment = SurfaceTreatmentSerializer()
    wood_lamination_types = WoodLaminationTypeSerializer(many=True)
    powder_coating_type = PowderCoatingTypeSerializer()
    powder_coating_color = PowderCoatingColorSerializer()
    has_mosquito_net = WindowWidthSerializer()
    fitting_price = FittingPriceOptionSerializer()
    puffing_price = PuffingPriceOptionSerializer()

    class Meta:
        model = CustomerEnquiry
        fields = [
            'id',
            'customer_name',
            'customer_email',
            'customer_phone',
            'customer_address',
            'window_model',
            'surface_treatment',
            'wood_lamination_types',
            'powder_coating_type',
            'powder_coating_color',
            'mosquito_net_needed',
            'has_mosquito_net',
            'fitting_price',
            'puffing_price',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']      
        
