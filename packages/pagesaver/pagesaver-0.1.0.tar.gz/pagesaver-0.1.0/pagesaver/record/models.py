from functools import cached_property

from django.db import models

from pagesaver.enums import ExportFormat
from pagesaver.lib.base.models import BaseModelWithUUID


class Snapshot(BaseModelWithUUID):
    url = models.URLField(db_index=True)
    title = models.CharField(max_length=512, default="", blank=True, db_index=True)

    @cached_property
    def size(self):
        pass

    class Meta:
        verbose_name = "快照"
        verbose_name_plural = verbose_name
        db_table = "snapshot"

    def __str__(self):
        return self.title

    def __repr___(self):
        return "<Snapshot: {}|{}>".format(self.title, self.uuid)


class SnapshotResult(BaseModelWithUUID):
    FORMAT_CHOICES = (
        (ExportFormat.PDF.value, "PDF"),
        (ExportFormat.MHTML.value, "MHTML文件"),
    )
    snapshot = models.ForeignKey(
        Snapshot, on_delete=models.CASCADE, related_name="results"
    )
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    path = models.FileField()

    class Meta:
        unique_together = ("snapshot", "format")
        verbose_name = "快照结果"
        verbose_name_plural = verbose_name
        db_table = "snapshot_result"

    def __str__(self):
        return str(self.path)

    def __repr___(self):
        return "<SnapshotResult: {} |{}>".format(self.snapshot.title, self.uuid)
