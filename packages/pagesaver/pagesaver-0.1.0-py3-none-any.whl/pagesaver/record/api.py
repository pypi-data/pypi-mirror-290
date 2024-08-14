from typing import Optional

from ninja import Field, Query, Router, Schema

from pagesaver.enums import ExportFormat
from pagesaver.record.models import Snapshot
from pagesaver.record.runner import BackgroundThreadRunner
from pagesaver.record.tasks import export_task, notion_push_task

router = Router()


class RecordFilters(Schema):
    format: list[ExportFormat] = Field(
        default=list(ExportFormat.__members__.values()),
    )


class NotionFilters(RecordFilters):
    api_token: str
    database_id: str
    token_v2: Optional[str] = None
    title: Optional[str] = ""


@router.get("/notion/{path:url}")
def notion_record(request, url: str, filters: Query[NotionFilters]):
    snapshot = Snapshot.objects.create(url=url)

    runner = BackgroundThreadRunner()
    runner.add_task(export_task, snapshot.pk, url, format=filters.format)
    runner.add_task(
        notion_push_task, snapshot.pk, url, **filters.model_dump(mode="json")
    )
    runner.start()
    return {
        "url": url,
        "uuid": snapshot.uuid,
        "params": filters.model_dump(mode="json"),
    }


@router.get("/{path:url}")
def record(request, url: str, filters: Query[RecordFilters]):
    snapshot = Snapshot.objects.create(url=url)
    runner = BackgroundThreadRunner()
    runner.add_task(export_task, snapshot.pk, url, **filters.model_dump(mode="json"))
    runner.start()
    return {
        "url": url,
        "uuid": snapshot.uuid,
        "params": filters.model_dump(mode="json"),
    }
