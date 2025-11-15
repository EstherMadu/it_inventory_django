from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Asset, AssetCategory, AssetStatus, AssetStatusHistory
from ..forms import AssetForm

# Manage assets
def admin_manage_assets(request):
    assets = Asset.objects.select_related('vendor', 'category').all()
    category_filter = request.GET.get('category')
    vendor_filter = request.GET.get('vendor')
    status_filter = request.GET.get('status')
    statuses = ["INVENTORY", "ASSIGNED", "REPAIR", "RETIRED"]

    if category_filter:
        assets = assets.filter(category_id=category_filter)
    if vendor_filter:
        assets = assets.filter(vendor_id=vendor_filter)
    if status_filter:
        assets = assets.filter(current_status=status_filter)

    form = AssetForm()
    categories = AssetCategory.objects.all()
    vendors = Asset.objects.all()

    return render(request, 'admin/manage_assets.html', {
        'assets': assets,
        'categories': categories,
        'vendors': vendors,
        'form': form,
        'statuses':statuses,
    })

# Add asset
def admin_add_asset(request):
    if request.method == "POST":
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.save()
            messages.success(request, "Asset added successfully")
        else:
            messages.error(request, "Please fix the errors on the form.")
    return redirect('admin_manage_assets')

# Delete asset
def admin_delete_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if asset.picture:
        asset.picture.delete()
    asset.delete()
    messages.success(request, "Asset deleted successfully")
    return redirect('admin_manage_assets')

#Change asset status
def admin_change_asset_status(request, asset_id):
    if request.method == "POST":
        asset = get_object_or_404(Asset, id=asset_id)
        new_status = request.POST.get('status')
        note = request.POST.get('note', '')
        changed_by = request.user
        # if new_status in AssetStatus.values:
        asset.current_status = new_status
        asset.save()
        AssetStatusHistory.objects.create(
            asset=asset,
            status=new_status,
            changed_by=changed_by,
            note=note
        )
        messages.success(request, "Status updated successfully")
    return redirect("admin_manage_assets")


# from django.http import JsonResponse

# def admin_change_asset_status(request, asset_id):
#     if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         asset = get_object_or_404(Asset, id=asset_id)
#         new_status = request.POST.get('status')
#         note = request.POST.get('note', '')
#         changed_by = request.user

#         asset.current_status = new_status
#         asset.save()

#         AssetStatusHistory.objects.create(
#             asset=asset,
#             status=new_status,
#             changed_by=changed_by,
#             note=note
#         )

#         # Return updated counts
#         status_counts = {
#             'inventory': Asset.objects.filter(current_status=AssetStatus.INVENTORY).count(),
#             'assigned': Asset.objects.filter(current_status=AssetStatus.ASSIGNED).count(),
#             'repair': Asset.objects.filter(current_status=AssetStatus.REPAIR).count(),
#             'retired': Asset.objects.filter(current_status=AssetStatus.RETIRED).count(),
#         }

#         return JsonResponse({
#             'success': True,
#             'status_counts': status_counts,
#             'asset_id': asset.id,
#             'new_status': asset.current_status.value
#         })

