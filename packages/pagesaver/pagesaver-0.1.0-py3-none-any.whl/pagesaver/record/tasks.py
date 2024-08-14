from pathlib import Path
from typing import Optional

from pagesaver.constants import SUPPORT_FORMATS
from pagesaver.enums import ExportFormat
from pagesaver.record.models import Snapshot, SnapshotResult
from pagesaver.settings import pagesaver_settings
from pagesaver.utils import export_utils, notion_utils
from pagesaver.utils.datetime_utils import get_now_str

STORAGE = pagesaver_settings.STORAGE


def export_task(snapshot_id: int, url: str, format: list[str]):
    snapshot = Snapshot.objects.get(pk=snapshot_id)

    format = None or SUPPORT_FORMATS
    base_directory = Path(STORAGE["path"]).absolute()
    directory = base_directory / str(snapshot.uuid) / get_now_str()

    path_lst, info = export_utils.export(
        url, directory, [ExportFormat(i) for i in format]
    )
    for item in path_lst:
        path = str(Path(item["path"]).relative_to(base_directory))
        SnapshotResult.objects.create(
            snapshot=snapshot, format=item["format"], path=path
        )
    snapshot.title = info.get("title", "")
    snapshot.save(update_fields=["title"])

    return path_lst, info


def notion_push_task(
    snapshot_id: int,
    url: str,
    *,
    api_token: str,
    database_id: str,
    token_v2: Optional[str] = None,
    title: str = "",
    **kwargs,
):
    snapshot = Snapshot.objects.get(pk=snapshot_id)
    path_lst = list(snapshot.results.all().values("format", "path"))

    title = title or snapshot.title

    page_id = notion_utils.create_page(
        database_id, title=title, token=api_token, link=url
    )
    if token_v2:
        base_directory = Path(STORAGE["path"]).absolute()
        path_2_dict = {p["format"]: (base_directory / p["path"]) for p in path_lst}
        if path := path_2_dict.get(ExportFormat.MHTML.value):
            notion_utils.add_mhtml_property(page_id, api_token, token_v2, path)
        if path := path_2_dict.get(ExportFormat.PDF.value):
            notion_utils.add_pdf_block(page_id, api_token, token_v2, path)

    return page_id


if __name__ == "__main__":
    import os

    from pagesaver.record.models import Snapshot

    url = "https://www.baidu.com"
    snapshot = Snapshot.objects.create(url=url)
    export_task(snapshot.id, url, ["PDF"])
    notion_push_task(
        snapshot.id,
        api_token=os.environ["NOTION_API_TOKEN"],
        database_id=os.environ["NOTION_DATABASE_ID"],
        token_v2=os.environ["NOTION_TOKEN_V2"],
        title="test",
    )
