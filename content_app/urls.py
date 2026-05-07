from django.urls import path
from . import views

urlpatterns = [
    path("", views.content_landing, name="contentLanding"),
    path("biography/", views.content_admin, name="contentAdmin"),
    path("stories/", views.stories_page, name="storiesPage"),
    path("account/settings/", views.account_settings, name="accountSettings"),
    path("content/create/", views.create_site_content, name="createSiteContent"),
    path("content/<slug:slug>/edit/", views.edit_site_content, name="editSiteContent"),
    path("content/<slug:slug>/delete/", views.delete_site_content, name="deleteSiteContent"),
    path("CRMAdmin/", views.CRMAdmin, name="CRMAdmin"),
    path("api/about/", views.about_collection_api, name="aboutCollectionApi"),
    path("api/about/<slug:slug>/", views.about_detail_api, name="aboutDetailApi"),
    path("api/stories/", views.stories_collection_api, name="storyCollectionApi"),
    path("api/stories/<slug:slug>/", views.story_detail_api, name="storyDetailApi"),
    path("api/testimonials/", views.testimonials_collection_api, name="testimonialCollectionApi"),
    path(
        "api/testimonials/<int:testimonial_id>/",
        views.testimonial_detail_api,
        name="testimonialDetailApi",
    ),
]