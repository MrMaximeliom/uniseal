from django.urls import path

from apps.approvals import dashboard_views as approval_views
from Util.search_form_strings import DELETE_APPROVALS_TITLE,EDIT_APPROVALS_TITLE

urlpatterns = [
    path('allApprovals', approval_views.ApprovalsListView.as_view(), name='approvalsList'),
    path('addApprovals', approval_views.ApprovalFormView.as_view(), name='addApprovals'),
    path('editApprovals', approval_views.ApprovalsListView.as_view(template_name ="approval/edit_approvals.html", active_flag="edit_approvals", title=EDIT_APPROVALS_TITLE), name='editApprovals'),
    path('editApproval/<str:slug>/', approval_views.ApprovalUpdateView.as_view(), name='editApproval'),
    path('approvalDetails/<int:pk>/', approval_views.ApprovalDetailView.as_view(), name='approvalDetails'),
    path('approvalImages/<str:slug>', approval_views.approval_images, name='approvalImages'),
    path('approvalImages/', approval_views.approval_images, name='approvalImages-dash'),
    path('deleteApprovals', approval_views.ApprovalsListView.as_view(template_name ="approvals/delete_approvals.html", active_flag="delete_approvals", title=DELETE_APPROVALS_TITLE), name='deleteApprovals'),
    path('deleteApproval/<str:slug>/', approval_views.confirm_delete, name='deleteApproval'),
]