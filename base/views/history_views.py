from django.shortcuts import render, get_object_or_404
from ..models import Asset, AssetStatusHistory, AssetAssignment

def admin_view_status_history(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    history = AssetStatusHistory.objects.filter(asset=asset).order_by('-timestamp')
    assignments = AssetAssignment.objects.filter(asset=asset).order_by('-assigned_at')
    return render(request, 'admin/view_status_history.html', {
        'asset': asset,
        'history': history,
        'assignments': assignments
    })
