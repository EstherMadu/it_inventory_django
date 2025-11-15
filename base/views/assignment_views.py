from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from ..models import Asset, AssetAssignment, AssetStatus, AssetStatusHistory
from ..forms import AssignmentForm

# View all assignments
def admin_view_assignments(request):
    assignments = AssetAssignment.objects.select_related('asset').order_by('-assigned_at')
    form = AssignmentForm()
    return render(request, 'admin/view_assignments.html', {'assignments': assignments, 'form': form})

def admin_assign_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            
            assigned_to = form.cleaned_data['assigned_to']
            assigned_by = form.cleaned_data.get('assigned_by', '')
            note = form.cleaned_data.get('note', '')

            
            assignment, created = AssetAssignment.objects.get_or_create(asset=asset)
            assignment.assigned_to = assigned_to
            assignment.assigned_by = assigned_by
            assignment.note = note
            assignment.save()

            
            asset.current_holder = assignment.assigned_to
            asset.current_status = AssetStatus.ASSIGNED
            asset.save()

            
            AssetStatusHistory.objects.create(
                asset=asset,
                status=AssetStatus.ASSIGNED,
                changed_by=request.user,
                note=f"Assigned to {assignment.assigned_to}"
            )

            messages.success(request, f"Asset '{asset.name}' assigned to {assignment.assigned_to}")
            return redirect('admin_view_assignments')
        else:
            messages.error(request, "Please provide assignee name")
    else:
        form = AssignmentForm()  

    return render(request, 'admin/assign_asset.html', {"asset": asset, "form": form})

    