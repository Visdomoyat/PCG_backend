from django.urls import path

from . import views

urlpatterns = [
    path("CRMAdmin/", views.crm_home, name="CRMAdmin"),
    path("CRMAdmin/services/", views.services_page, name="crmServices"),
    path("CRMAdmin/services/<int:pk>/delete/", views.delete_service, name="deleteService"),
    path("CRMAdmin/leads/create/", views.create_lead, name="createLead"),
    path("CRMAdmin/leads/<int:pk>/", views.edit_lead, name="editLead"),
    path("CRMAdmin/leads/<int:pk>/delete/", views.delete_lead, name="deleteLead"),
    path(
        "CRMAdmin/leads/<int:pk>/tasks/<int:task_id>/status/",
        views.update_task_status,
        name="updateLeadTaskStatus",
    ),
    path(
        "CRMAdmin/leads/<int:pk>/tasks/<int:task_id>/delete/",
        views.delete_task,
        name="deleteLeadTask",
    ),
]
