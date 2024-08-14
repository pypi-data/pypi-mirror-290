from django.contrib import admin

from .models import Snapshot, SnapshotResult


class SnapshotAdmin(admin.ModelAdmin):
    list_display = ("uuid", "title", "url", "size", "created")
    fields = ("uuid", "title", "url")
    readonly_fields = ("uuid",)
    list_filter = ("created",)


class SnapshotResultAdmin(admin.ModelAdmin):
    list_display = ("uuid", "snapshot", "format", "path", "created")
    readonly_fields = ("uuid", "snapshot", "format", "created")
    fields = ("uuid", "created", "snapshot", "format", "path")
    list_filter = ("format", "snapshot", "created")


admin.site.register(Snapshot, SnapshotAdmin)
admin.site.register(SnapshotResult, SnapshotResultAdmin)
