from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.admin.views.pages.create import CreateView
from wagtail.admin.views.pages.edit import EditView
from wagtail.admin.ui.components import MediaContainer
from wagtail.admin.ui.side_panels import PreviewSidePanel
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views


class CustomPreviewSidePanel(PreviewSidePanel):
    class SidePanelToggle(PreviewSidePanel.SidePanelToggle):
        icon_name = "desktop"

    template_name = "custom-preview.html"


class CustomCreateView(CreateView):
    def get_side_panels(self):
        # Replace any PreviewSidePanel in parent method with CustomPreviewSidePanel
        media_container = MediaContainer()
        for side_panel in super().get_side_panels():
            if isinstance(side_panel, PreviewSidePanel):
                side_panel = CustomPreviewSidePanel(
                    self.page, self.request, preview_url=self.get_preview_url()
                )

            media_container.append(side_panel)

        return media_container


class CustomEditView(EditView):
    def get_side_panels(self):
        # Replace any PreviewSidePanel in parent method with CustomPreviewSidePanel
        media_container = MediaContainer()
        for side_panel in super().get_side_panels():
            if isinstance(side_panel, PreviewSidePanel):
                side_panel = CustomPreviewSidePanel(
                    self.page, self.request, preview_url=self.get_preview_url()
                )

            media_container.append(side_panel)

        return media_container


urlpatterns = [
    # Override create view in order to apply custom view
    path(
        "admin/pages/add/<slug:content_type_app_name>/<slug:content_type_model_name>/<int:parent_page_id>/",
        CustomCreateView.as_view(),
        name="add",
    ),
    # Override edit view in order to apply custom view
    path("admin/pages/<int:page_id>/edit/", CustomEditView.as_view(), name="edit"),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
