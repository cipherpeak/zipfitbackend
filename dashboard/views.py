from django.shortcuts import render,get_object_or_404,redirect,reverse
from windows.models import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .models import ProductionApproval

# Create your views here.
class LoginView(View):
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:fetch-customer-data')
        return render(request, 'login.html')
        
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard:fetch-customer-data'))  
        return render(request, 'login.html', {'error': 'Invalid credentials'})

class FetchCustomerFormData(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('dashboard:login')
        
        enquiries = CustomerEnquiry.objects.all().order_by('-created_at')
        return render(request, 'dashboard.html', {'enquiries': enquiries})
    

from django.db.models import Count
from collections import defaultdict

class CustomerOrderView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('dashboard:login')
        
        # Group enquiries by customer_email
        enquiries = CustomerEnquiry.objects.all().order_by('-created_at')
        
        # Create a dictionary to group orders by customer
        customer_orders = defaultdict(list)
        for enquiry in enquiries:
            customer_orders[enquiry.customer_email].append(enquiry)
        
        # Get the most recent order for each customer and add order count
        grouped_orders = []
        for email, orders in customer_orders.items():
            most_recent_order = max(orders, key=lambda x: x.created_at)
            most_recent_order.order_count = len(orders)
            grouped_orders.append(most_recent_order)
        
        return render(request, 'orders.html', {'enquiries': grouped_orders})
    
from django.core import serializers
from django.utils.html import mark_safe
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')    
class CustomerDetailView(View):
    def get(self, request, customer_id):
        if not request.user.is_authenticated:
            return redirect('dashboard:login')
        
        customer = get_object_or_404(CustomerEnquiry, id=customer_id)
        customer_orders = CustomerEnquiry.objects.filter(
            customer_email=customer.customer_email,
            customer_phone=customer.customer_phone
        ).order_by('-created_at')
        is_approved_for_production = any(order.status == 'approved' for order in customer_orders)
        is_in_production = any(order.status == 'in_production' for order in customer_orders)
        orders_data = []
        for order in customer_orders:
            order_data = {
                'id': order.id,
                'customer_name': order.customer_name,
                'customer_email': order.customer_email,
                'customer_phone': order.customer_phone,
                'customer_address': order.customer_address,
                'approximate_amount': order.approximate_amount,
                'notes': order.notes,
                'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                
                # Window configuration data
                'window_type': order.window_model.window_type.name if order.window_model and order.window_model.window_type else None,
                'window_series': order.window_model.window_series.name if order.window_model and order.window_model.window_series else None,
                'dimensions': f"{order.window_model.width.name} x {order.window_model.height.name}" if order.window_model and order.window_model.width and order.window_model.height else None,
                'window_image': order.window_model.image.url if order.window_model and order.window_model.image else None,
                
                # Surface treatment data
                'surface_treatment': order.surface_treatment.name if order.surface_treatment else None,
                'wood_lamination_types': [wood.name for wood in order.wood_lamination_types.all()] if order.wood_lamination_types.exists() else [],
                
                # Powder coating data
                'powder_coating_type': order.powder_coating_type.name if order.powder_coating_type else None,
                'powder_coating_color': order.powder_coating_color.name if order.powder_coating_color else None,
                
                # Additional features
                'mosquito_net_needed': order.mosquito_net_needed,
                'has_mosquito_net': order.has_mosquito_net.name if order.has_mosquito_net else None,
                'fitting_price': order.fitting_price.price if order.fitting_price else None,
                'puffing_price': order.puffing_price.price if order.puffing_price else None,
                
                # Add the IDs for the related fields
                'finish_id': order.finish.id if order.finish else None,
                'infill_id': order.infill.id if order.infill else None,
                'hardware_id': order.hardware.id if order.hardware else None,
                'lock_id': order.lock.id if order.lock else None,
                'other_id': order.other.id if order.other else None,
                
                # Items list
                'items': [{
                    "sl_no": idx + 1,
                    "width": order.window_model.width.name if order.window_model and order.window_model.width else None,
                    "height": order.window_model.height.name if order.window_model and order.window_model.height else None,
                    "area": None,  # You'll need to calculate this
                    "item": order.window_model.window_type.name if order.window_model and order.window_model.window_type else None,
                    "profile": order.window_model.window_series.name if order.window_model and order.window_model.window_series else None,
                    "finish": order.finish.text if order.finish else None,
                    "infill": order.infill.text if order.infill else None,
                    "hardware": order.hardware.text if order.hardware else None,
                    "lock": order.lock.text if order.lock else None,
                    "other": order.other.text if order.other else order.notes,
                    "amount": order.approximate_amount
                } for idx in range(1)]  
            }
            orders_data.append(order_data)
        
        context = {
            'customer': customer,  
            'customer_orders': customer_orders,     
            'orders_json': mark_safe(json.dumps(orders_data)),
            'finish_options': Finish.objects.all(),
            'infill_options': Infill.objects.all(),
            'hardware_options': Hardware.objects.all(),
            'lock_options': Lock.objects.all(),
            'other_options': Other.objects.all(),
            'is_approved_for_production': is_approved_for_production,
            'is_in_production': is_in_production,
            'window_types': WindowType.objects.all(),
            'window_series': WindowSeries.objects.all(),
            'window_configurations': WindowConfiguration.objects.all(),
            
        }
        return render(request, 'customer.html', context)
    


@method_decorator(csrf_exempt, name='dispatch')
class UpdateOrderConfigView(View):
    def post(self, request, customer_id=None):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Authentication required'})
        
        try:
            # Get the order ID from the request
            order_id = request.POST.get('order_id')
            if not order_id:
                return JsonResponse({'success': False, 'message': 'Order ID is required'})
            
            # Get the order instance
            order = CustomerEnquiry.objects.get(id=order_id)
            
            # Update the order with the new data
            finish_id = request.POST.get('finish')
            infill_id = request.POST.get('infill')
            hardware_id = request.POST.get('hardware')
            lock_id = request.POST.get('lock')
            other_id = request.POST.get('other')
            
            # Update or clear fields
            if finish_id:
                order.finish = Finish.objects.get(id=finish_id)
            else:
                order.finish = None
                
            if infill_id:
                order.infill = Infill.objects.get(id=infill_id)
            else:
                order.infill = None
                
            if hardware_id:
                order.hardware = Hardware.objects.get(id=hardware_id)
            else:
                order.hardware = None
                
            if lock_id:
                order.lock = Lock.objects.get(id=lock_id)
            else:
                order.lock = None
                
            if other_id:
                order.other = Other.objects.get(id=other_id)
            else:
                order.other = None
            
            order.save()
            
            return JsonResponse({'success': True, 'message': 'Configuration updated successfully'})
            
        except CustomerEnquiry.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        

@method_decorator(csrf_exempt, name='dispatch')
class ApproveSupervisorOrderView(View):
    def post(self, request):
        try:
            data = request.POST
            customer_id = data.get('customer_id')
            print(customer_id,"this is coustomer id")
            
            if not customer_id:
                return JsonResponse({
                    'success': False, 
                    'message': 'Customer ID is required'
                })
            
            
            # Get all orders for this customer
            orders = CustomerEnquiry.objects.filter(id=customer_id)
            print(orders,"this is orders")
            # Process each order
            for order in orders:
                order_id = str(order.id)
                
                # Get the actual width and height values
                actual_width = data.get(f'actual_width_{order_id}')
                actual_height = data.get(f'actual_height_{order_id}')
                
                # Check if approval checkbox is checked
                is_approved = data.get('supervisor_approval') == 'on'
                
                # Create or update ProductionApproval
                approval, created = ProductionApproval.objects.get_or_create(
                    customer_enquiry=order,
                    defaults={
                        'actual_width': actual_width,
                        'actual_height': actual_height,
                        'is_approved': is_approved
                    }
                )
                
                if not created:
                    approval.actual_width = actual_width
                    approval.actual_height = actual_height
                    approval.is_approved = is_approved
                    approval.save()
                
                # Update the order status if approved
                if is_approved:
                    order.status = 'approved'
                    order.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'Order approved successfully!'
            })
            
        except CustomerEnquiry.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Customer enquiry not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error: {str(e)}'
            })

        
class ProductionStatusPage(View):
    def get(self, request, order_id): 
        if not request.user.is_authenticated:
            return redirect('dashboard:login')
        
        # Get the specific order
        order = get_object_or_404(CustomerEnquiry, id=order_id)
        
        # Get all orders for this customer (based on email and phone)
        customer_orders = CustomerEnquiry.objects.filter(
            customer_email=order.customer_email,
            customer_phone=order.customer_phone
        ).order_by('-created_at')

        context = {
            'order': order,  # The specific order
            'customer_orders': customer_orders,  # All orders for this customer
        }
        return render(request, 'production.html', context)

class AddWindowConfiguration(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('dashboard:login')
        
        context = {
            'window_widths': WindowWidth.objects.all(),
            'window_heights': WindowHeight.objects.all(),
            'window_types': WindowType.objects.all(),
            'window_series': WindowSeries.objects.all(),
        }
        return render(request, 'add_measurment.html', context)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('dashboard:login')
        
        try:
            width_id = request.POST.get('width')
            height_id = request.POST.get('height')
            window_type_id = request.POST.get('window_type')
            window_series_id = request.POST.get('window_series')
            rate_per_Sq_Feet = request.POST.get('rate_per_Sq_Feet')
            gst_amount = request.POST.get('gst_amount')
            total_amount = request.POST.get('total_amount')
            notes = request.POST.get('notes')
            image = request.FILES.get('image')

            if not all([width_id, height_id, window_type_id, window_series_id, rate_per_Sq_Feet, gst_amount]):
                messages.error(request, "Please fill all required fields")
                return redirect('dashboard:add_window_configuration')

            existing_config = WindowConfiguration.objects.filter(
                width_id=width_id,
                height_id=height_id,
                window_type_id=window_type_id,
                window_series_id=window_series_id
            ).first()

            if existing_config:
                messages.warning(request, 
                    f"This window configuration already exists (ID: {existing_config.id}). "
                    f"Please edit the existing configuration instead of creating a duplicate."
                )
                return redirect('dashboard:add_window_configuration')

            window_config = WindowConfiguration(
                width_id=width_id,
                height_id=height_id,
                window_type_id=window_type_id,
                window_series_id=window_series_id,
                rate_per_Sq_Feet=rate_per_Sq_Feet,
                gst_amount=gst_amount,
                total_amount=total_amount if total_amount else None,
                notes=notes,
            )

            if image:
                window_config.image = image

            window_config.save()

            messages.success(request, "Window configuration added successfully!")
            return render(request, 'success_message.html', {
                'message': 'Window Configuration Saved Successfully',
                'config_id': window_config.id,
                'window_type': window_config.window_type.name
            })

        except Exception as e:
            messages.error(request, f"Error saving window configuration: {str(e)}")
            return redirect('dashboard:add_window_configuration')
        



        
class LogoutView(View):
    def get(self,request):
        logout(request)  
        return render(request,'login.html')   

class ProductList(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('dashboard:login')
        
        search_query = request.GET.get('search', '')
        
        products = WindowConfiguration.objects.all().order_by('-created_at')
        
        if search_query:
            products = products.filter(
                Q(window_series__name__icontains=search_query) |
                Q(window_series__code__icontains=search_query)
            )
        
        context = {
            'products': products,
            'window_widths': WindowWidth.objects.all(),
            'window_heights': WindowHeight.objects.all(),
            'window_types': WindowType.objects.all(),
            'window_series': WindowSeries.objects.all(),
            'search_query': search_query,
        }
        return render(request, 'products.html', context)

class AddWindowHeight(View):
    
    def post(self, request):
        name = request.POST.get('height')
        description = request.POST.get('description')
        
        try:
            WindowHeight.objects.create(name=name, description=description)
            messages.success(request, 'Height added successfully!')
            return redirect('dashboard:add_window_configuration')
        except Exception as e:
            messages.error(request, f'Error adding height: {str(e)}')
            return redirect('dashboard:add_window_configuration')

class DeleteWindowHeight(View):
    def post(self, request, pk):
        height = get_object_or_404(WindowHeight, pk=pk)
        try:
            height.delete()
            messages.success(request, 'Height deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting height: {str(e)}')
        return redirect('dashboard:add_window_configuration')
    


class AddWindowWidth(View):

    def post(self, request):
        name = request.POST.get('width')
        description = request.POST.get('description')
        
        try:
            WindowWidth.objects.create(name=name, description=description)
            messages.success(request, 'Width added successfully!')
            return redirect('dashboard:add_window_configuration')
        except Exception as e:
            messages.error(request, f'Error adding width: {str(e)}')
            return redirect('dashboard:add_window_configuration')


class DeleteWindowWidth(View):
    def post(self, request, pk):
        width = get_object_or_404(WindowWidth, pk=pk)
        try:
            width.delete()
            messages.success(request, 'Width deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting width: {str(e)}')
        return redirect('dashboard:add_window_configuration')    




class AddWindowType(View):
    
    def post(self, request):
        name = request.POST.get('name')
        code = request.POST.get('code')
        icon = request.POST.get('icon')
        description = request.POST.get('description')
        
        try:
            WindowType.objects.create(
                name=name,
                code=code,
                icon=icon,
                description=description
            )
            messages.success(request, 'Window type added successfully!')
            return redirect('dashboard:add_window_configuration')
        except Exception as e:
            messages.error(request, f'Error adding window type: {str(e)}')
            return redirect('dashboard:add_window_configuration')


class DeleteWindowType(View):
    def post(self, request, pk):
        window_type = get_object_or_404(WindowType, pk=pk)
        try:
            window_type.delete()
            messages.success(request, 'Window type deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting window type: {str(e)}')
        return redirect('dashboard:add_window_configuration')





class AddWindowSeries(View):
    def post(self, request):
        name = request.POST.get('name')
        code = request.POST.get('code')
        price_per_sqft = request.POST.get('price_per_sqft')
        description = request.POST.get('description')
        
        try:
            WindowSeries.objects.create(
                name=name,
                code=code,
                price_per_sqft=price_per_sqft,
                description=description
            )
            messages.success(request, 'Window series added successfully!')
            return redirect('dashboard:add_window_configuration')
        except Exception as e:
            messages.error(request, f'Error adding window series: {str(e)}')
            return redirect('dashboard:add_window_configuration')


class DeleteWindowSeries(View):
    def post(self, request, pk):
        series = get_object_or_404(WindowSeries, pk=pk)
        try:
            series.delete()
            messages.success(request, 'Window series deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting window series: {str(e)}')
        return redirect('dashboard:add_window_configuration')
    

class EditWindowConfiguration(View):

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('dashboard:login')
        
        product = get_object_or_404(WindowConfiguration, pk=pk)
        try:
            product.width_id = request.POST.get('width')
            product.height_id = request.POST.get('height')
            product.window_type_id = request.POST.get('window_type')
            product.window_series_id = request.POST.get('window_series')
            product.rate_per_Sq_Feet = request.POST.get('rate_per_Sq_Feet')
            product.gst_amount = request.POST.get('gst_amount')
            product.total_amount = request.POST.get('total_amount')
            product.notes = request.POST.get('notes')
            
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            
            product.save()
            messages.success(request, "Window configuration updated successfully!")
            return redirect('dashboard:product_list')
            
        except Exception as e:
            messages.error(request, f"Error updating window configuration: {str(e)}")
            return redirect('dashboard:product_list', pk=pk)    
        
class DeleteWindowConfiguration(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('dashboard:login')
        
        product = get_object_or_404(WindowConfiguration, pk=pk)
        try:
            product.delete()
            messages.success(request, "Window configuration deleted successfully!")
        except Exception as e:
            messages.error(request, f"Error deleting window configuration: {str(e)}")
        
        return redirect('dashboard:product_list')        
    


    



