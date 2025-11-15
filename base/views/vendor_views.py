from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Asset, Admin, Profile, User,Vendor, Asset, AssetStatus,AssetCategory
from ..forms import VendorLoginForm,AssetForm
from django.db.models import Sum
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def vendor_login(request):
    form = VendorLoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "user with this name already exist")

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('vendor_dashboard')
            else:
                messages.error(request, "invalid email or password")
            


        except User.DoesNotExist:
            messages.error(request, "Invalid username or password")
    return render(request, 'vendor/vendor_login.html', {'form': form})


@login_required
def vendor_dashboard(request):

    vendor = request.user.vendor

    
    categories_count = (
        Asset.objects
        .select_related("category")
        .filter(vendor=vendor)
        .aggregate(total=Count("category_id"))
    )

    assets_count = Asset.objects.filter(vendor=vendor).aggregate(
        total=Count("id")
    )

    
    if request.method == "POST":
        form = AssetForm(request.POST, request.FILES)

        if form.is_valid():
            new_asset = form.save(commit=False)
            new_asset.vendor = vendor  
            new_asset.save()
            print("form submited")
            messages.success(request, "Asset added successfully.")
            return redirect("vendor_dashboard")

        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = AssetForm()
    

    
    categories = AssetCategory.objects.all()
    my_assets = Asset.objects.filter(vendor=vendor)

    context = {
        "category_total": categories_count["total"],
        "assets_total": assets_count["total"],
        "vendor": vendor,
        "form": form,
        "categories": categories,
        "my_assets": my_assets,
    }

    return render(request, "vendor/vendor_dashboard.html", context)
def vendor_logout(request):
    logout(request.user)
    return redirect('vendor_login')



        


        

