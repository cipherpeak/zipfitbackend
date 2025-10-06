
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status


class WindowSeriesAPIView(APIView):
    def get(self, request):
        series = WindowSeries.objects.all()
        serializer = WindowSeriesSerializer(series, many=True)
        return Response(serializer.data)


class WindowTypesAPIView(APIView):
    def get(self, request):
        types = WindowType.objects.all()
        serializer = WindowTypeSerializer(types, many=True)
        return Response(serializer.data)


class WindowHeightAPIView(APIView):
    def get(self, request):
        types = WindowHeight.objects.all()
        serializer = WindowHeightSerializer(types, many=True)
        return Response(serializer.data)
    


class WindowWidthAPIView(APIView):
    def get(self, request):
        types = WindowWidth.objects.all()
        serializer = WindowWidthSerializer(types, many=True)
        return Response(serializer.data)
    

class WindowDetailsAPIView(APIView):
    def post(self, request):
        width = request.data.get('width')
        series = request.data.get('series')
        height = request.data.get('height')
        window_type = request.data.get('windowType')  
        
        if not all([width, series, height, window_type]):
            return Response(
                {'error': 'Missing required fields (width, series, height, windowType)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            width_obj = WindowWidth.objects.get(name=int(width))
            height_obj = WindowHeight.objects.get(name=int(height))
            window_type_obj = WindowType.objects.get(name=window_type)
            window_series_obj = WindowSeries.objects.get(name=series)
            
            config = WindowConfiguration.objects.filter(
                width=width_obj,
                height=height_obj,
                window_type=window_type_obj,
                window_series=window_series_obj
            ).first()
            
            if config:
                serializer = WindowConfigurationSerializer(config)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'No matching window configuration found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except WindowWidth.DoesNotExist:
            return Response(
                {'error': f'Invalid width: {width}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except WindowHeight.DoesNotExist:
            return Response(
                {'error': f'Invalid height: {height}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except WindowType.DoesNotExist:
            return Response(
                {'error': f'Invalid window type: {window_type}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except WindowSeries.DoesNotExist:
            return Response(
                {'error': f'Invalid series: {series}'},
                status=status.HTTP_400_BAD_REQUEST
            )
            

class CustomerFormData(APIView):
    def post(self, request):
        try:
            customer_data = request.data
            required_fields = ['name', 'email', 'phone', 'address', 'window_config_id', 'window_config','approximate_amount']
            for field in required_fields:
                if field not in customer_data:
                    return Response(
                        {'error': f'Missing required field: {field}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            try:
                window_config = WindowConfiguration.objects.get(id=customer_data['window_config_id'])
            except WindowConfiguration.DoesNotExist:
                return Response(
                    {'error': 'Invalid window configuration ID'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            window_config_data = customer_data['window_config']

            
            surface_treatment = SurfaceTreatment.objects.filter(name=window_config_data.get('surfaceTreatment')).first()

            powder_coating_type = PowderCoatingType.objects.filter(name=window_config_data.get('powderCoatingType')).first()
            
            powder_coating_color = PowderCoatingColor.objects.filter(name=window_config_data.get('powderCoatingColor')).first()
            
            mosquito_net_width = WindowWidth.objects.filter(name=window_config_data.get('mosquitoNetWidth')).first() if window_config_data.get('mosquitoNet') else None
            
            fitting_price = FittingPriceOption.objects.filter(price=window_config_data.get('fittingPrice')).first()
            
            puffing_price = PuffingPriceOption.objects.filter(price=window_config_data.get('puffingPrice')).first()
            
            enquiry = CustomerEnquiry.objects.create(
                customer_name=customer_data['name'],
                customer_email=customer_data['email'],
                customer_phone=customer_data['phone'],
                approximate_amount=customer_data['approximate_amount'],
                customer_address=customer_data['address'],
                window_model=window_config,
                surface_treatment=surface_treatment,
                powder_coating_type=powder_coating_type,
                powder_coating_color=powder_coating_color,
                mosquito_net_needed=window_config_data.get('mosquitoNet', False),
                has_mosquito_net=mosquito_net_width,
                fitting_price=fitting_price,
                puffing_price=puffing_price,
            )

            
            wood_lamination_types = window_config_data.get('woodLaminationType', [])
            for lamination_type in wood_lamination_types:
                lamination_obj = WoodLaminationType.objects.filter(name=lamination_type).first()
                if lamination_obj:
                    enquiry.wood_lamination_types.add(lamination_obj)
            
            serializer = CustomerEnquirySerializer(enquiry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PuffingPriceOptionAPIView(APIView):
    def get(self, request):
        options = PuffingPriceOption.objects.all()
        serializer = PuffingPriceOptionSerializer(options, many=True)
        return Response(serializer.data)

class SurfaceTreatmentAPIView(APIView):
    def get(self, request):
        treatments = SurfaceTreatment.objects.all()
        serializer = SurfaceTreatmentSerializer(treatments, many=True)
        return Response(serializer.data)

class WoodLaminationTypeAPIView(APIView):
    def get(self, request):
        lamination_types = WoodLaminationType.objects.all()
        serializer = WoodLaminationTypeSerializer(lamination_types, many=True)
        return Response(serializer.data)

class PowderCoatingTypeAPIView(APIView):
    def get(self, request):
        coating_types = PowderCoatingType.objects.all()
        serializer = PowderCoatingTypeSerializer(coating_types, many=True)
        return Response(serializer.data)

class PowderCoatingColorAPIView(APIView):
    def get(self, request):
        colors = PowderCoatingColor.objects.all()
        serializer = PowderCoatingColorSerializer(colors, many=True)
        return Response(serializer.data)


class FittingPriceOptionAPIView(APIView):
    def get(self, request):
        options = FittingPriceOption.objects.all()
        serializer = FittingPriceOptionSerializer(options, many=True)
        return Response(serializer.data)
