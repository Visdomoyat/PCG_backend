from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import SiteContentViewSet
from . import views

router = DefaultRouter()
router.register("site-content", SiteContentViewSet, basename="site-content")

urlpatterns = [
    path("", views.content_landing, name="contentLanding"),
    path("biography/", views.content_admin, name="contentAdmin"),
    path("stories/create/", views.create_story, name="createStory"),
    path("stories/<slug:slug>/edit/", views.edit_story, name="editStory"),
    path("stories/<slug:slug>/delete/", views.delete_story, name="deleteStory"),
    path("stories/", views.stories_page, name="storiesPage"),
    path("gallery/create/", views.create_gallery_item, name="createGalleryItem"),
    path("gallery/<int:pk>/edit/", views.edit_gallery_item, name="editGalleryItem"),
    path("gallery/<int:pk>/delete/", views.delete_gallery_item, name="deleteGalleryItem"),
    path("gallery/", views.gallery_page, name="galleryPage"),
    path("testimonials/<int:pk>/edit/", views.edit_testimonial, name="editTestimonial"),
    path("testimonials/<int:pk>/review/", views.review_testimonial, name="reviewTestimonial"),
    path("testimonials/<int:pk>/delete/", views.delete_testimonial, name="deleteTestimonial"),
    path("testimonials/", views.testimonials_page, name="testimonialsPage"),
    path("account/settings/", views.account_settings, name="accountSettings"),
    path("content/create/", views.create_site_content, name="createSiteContent"),
    path("content/<slug:slug>/edit/", views.edit_site_content, name="editSiteContent"),
    path("content/<slug:slug>/delete/", views.delete_site_content, name="deleteSiteContent"),
    path("api/about/", views.about_collection_api, name="aboutCollectionApi"),
    path("api/about/<slug:slug>/", views.about_detail_api, name="aboutDetailApi"),
    path("api/stories/", views.stories_collection_api, name="storyCollectionApi"),
    path("api/stories/<slug:slug>/", views.story_detail_api, name="storyDetailApi"),
    path("api/gallery/", views.gallery_collection_api, name="galleryCollectionApi"),
    path("api/gallery/<int:pk>/", views.gallery_item_detail_api, name="galleryItemDetailApi"),
    path("api/testimonials/", views.testimonials_collection_api, name="testimonialCollectionApi"),
    path(
        "api/testimonials/<int:testimonial_id>/",
        views.testimonial_detail_api,
        name="testimonialDetailApi",
    ),
    path("api/v1/", include(router.urls)),
]