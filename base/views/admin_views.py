from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Asset, Admin, Profile, User,Vendor
from ..forms import AdminSignupForm, AdminLoginForm, VendorSignupForm, VendorForm
from django.db.models import Sum
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.db.models import Count
from ..models import Vendor, Asset, AssetStatus


# Admin signup
def admin_signup(request):
    form = AdminSignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']
        department = form.cleaned_data['department']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create(username = username, password=make_password(password), email=email)
            profile = Profile.objects.create(user=user, user_type=Profile.UserTypeEnums.ADMIN.value, email=email)
            admin = Admin(
               department=department,
               last_login=timezone.now(),
               profile=profile
            )
            admin.save()
            messages.success(request, "Admin account created successfully")
            return redirect('admin_login')
    return render(request, 'admin/admin_signup.html', {'form': form})

# Admin login
def admin_login(request):
    form = AdminLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid username or password")
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password)")
    return render(request, 'admin/admin_login.html', {'form': form})

# Admin logout
def admin_logout(request):
    logout(request)  
    return redirect('admin_login')

# Admin dashboard
def admin_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "Admin login required")
        return redirect('admin_login')


    total_vendors = Vendor.objects.count()
    total_assets = Asset.objects.count()
    status_counts = {
        'inventory': Asset.objects.filter(current_status=AssetStatus.INVENTORY).count(),
        'assigned': Asset.objects.filter(current_status=AssetStatus.ASSIGNED).count(),
        'repair': Asset.objects.filter(current_status=AssetStatus.REPAIR).count(),
        'retired': Asset.objects.filter(current_status=AssetStatus.RETIRED).count(),
    }

    latest_assets = Asset.objects.select_related('vendor', 'category').order_by('-created_at')[:6]

    return render(request, 'admin/admin_dashboard.html', {
        'total_vendors': total_vendors,
        'total_assets': total_assets,
        'status_counts': status_counts,
        'latest_assets': latest_assets
    })


#Manage vendors
def admin_manage_vendors(request):
    vendors = Vendor.objects.order_by('-user__date_joined')
    form = VendorForm()
    return render(request, 'admin/manage_vendors.html', {'vendors': vendors, 'form': form})

# Add vendor
def admin_add_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, "Passwords do not match")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")

            else:
                user = User.objects.create(username = username, password=make_password(password), email=email)
                profile = Profile.objects.create(user=user, user_type=Profile.UserTypeEnums.ADMIN.value, email=email)
                vendor=Vendor.objects.create(user=user)
             
    return redirect('admin_manage_vendors')




def admin_delete_vendor(request, id):
    vendor = get_object_or_404(Vendor, id=id)
    vendor.delete()
    messages.success(request, "Vendor deleted successfully")
    return redirect("admin_manage_vendors")

# View vendor assets
def view_vendor_assets(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor_assets_qs = Asset.objects.filter(vendor=vendor).select_related('category')
    
    # create list of tuples (asset, category_name)
    vendor_assets = [(asset, asset.category.name if asset.category else 'Uncategorized') 
                     for asset in vendor_assets_qs]
    
    total_quantity = vendor_assets_qs.aggregate(Sum('quantity'))['quantity__sum'] or 0

    return render(request, 'admin/vendor_assets.html', {
        'vendor': vendor,
        'vendor_assets': vendor_assets,
        'total_quantity': total_quantity
    })


