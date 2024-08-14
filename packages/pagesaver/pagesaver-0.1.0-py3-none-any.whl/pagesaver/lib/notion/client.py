import mimetypes
import os
from pathlib import Path

from pagesaver.lib.base.client import RequestsBaseClient

API_BASE_URL = "https://api.notion.com/v1/"
UNOFFICIAL_BASE_URL = "https://www.notion.so/api/v3/"


class NotionClient(RequestsBaseClient):
    def __init__(self, token, base_url=None, **kwargs) -> None:
        super().__init__(base_url=base_url or API_BASE_URL, **kwargs)
        self.token = token or os.getenv("NOTION_API_TOKEN")

    def build_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def create_page(self, database_id, properties):
        payload = {
            "parent": {
                "database_id": database_id,
                "type": "database_id",
            },
            "properties": properties,
            "children": [],
        }
        return self.post("pages", body=payload)

    def add_block(self, page_id, children):
        payload = {
            "children": children,
        }
        return self.patch(f"blocks/{page_id}/children", body=payload)

    def update_block(self, block_id, payload):
        return self.patch(f"blocks/{block_id}", body=payload)

    def update_page_properties(self, page_id, properties):
        payload = {
            "properties": properties,
        }
        return self.patch(f"pages/{page_id}", body=payload)


class NotionUnofficialClient(RequestsBaseClient):

    def __init__(self, token_v2, space_id=None, base_url=None, **kwargs) -> None:
        super().__init__(base_url=base_url or UNOFFICIAL_BASE_URL, **kwargs)
        self.token_v2 = token_v2 or os.getenv("NOTION_TOKEN_V2")
        self.space_id = space_id or self._get_space_info().get("spaceId")

    def _get_space_info(self):
        records = self.post("loadUserContent", {})["recordMap"]
        return list(records["space_view"].values())[0]

    def build_headers(self):
        return {
            "cookie": f"token_v2={self.token_v2}",
            "Notion-Client-Version": "23.13.0.316",
            "content-type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

    def _get_upload_url(self, block_id, path: Path):
        payload = {
            "bucket": "secure",
            "name": path.name,
            "contentType": mimetypes.guess_type(path)[0] or "text/plain; charset=utf-8",
            "record": {
                "table": "block",
                "id": block_id,
                "spaceId": self.space_id,
            },
            "supportExtraHeaders": True,
            "contentLength": path.stat().st_size,
        }

        return self.post("getUploadFileUrl", body=payload)

    def upload_file(self, block_id, file_path: Path):
        data = self._get_upload_url(block_id, file_path)
        self.do_request(
            "POST",
            data["signedUploadPostUrl"],
            data=data["fields"],
            headers={header["name"]: header["value"] for header in data["postHeaders"]},
            files={"file": file_path.open("rb")},
            timeout=10,
        )
        return data["url"]


if __name__ == "__main__":
    import os
    client = NotionUnofficialClient(token_v2=os.getenv("NOTION_TOKEN_V2"))
    print(client.space_id)
