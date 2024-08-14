from pathlib import Path

from pagesaver.lib.notion import block, property
from pagesaver.lib.notion.client import NotionClient, NotionUnofficialClient
from pagesaver.settings import pagesaver_settings

TITLE_KEY = pagesaver_settings.TITLE_PROPERTY
LINK_KEY = pagesaver_settings.LINK_PROPERTY
MHTML_KEY = pagesaver_settings.MHTML_PROPERTY


def create_page(database_id: str, token: str, title: str, link: str) -> str:
    client = NotionClient(token=token)
    properties = {
        TITLE_KEY: property.Title(children=[property.Text(content=title)]).to_dict(),
        LINK_KEY: property.Url(url=link).to_dict(),
    }

    return client.create_page(database_id, properties)["id"]


def upload_file(token_v2: str, block_id: str, file_path: Path):
    unofficial_client = NotionUnofficialClient(token_v2=token_v2)
    return unofficial_client.upload_file(block_id, file_path)


def add_mhtml_property(page_id: str, token: str, token_v2: str, file_path: Path):
    url = upload_file(token_v2, page_id, file_path)
    client = NotionClient(token=token)
    client.update_page_properties(
        page_id,
        {
            MHTML_KEY: property.Files(
                children=[property.NotionHostedFile(name=file_path.name, url=url)]
            ).to_dict(),
        },
    )


def add_pdf_block(page_id: str, token: str, token_v2: str, file_path: Path):
    client = NotionClient(token=token)
    block_id = client.add_block(
        page_id, [block.PDFBlock(url="https://www.notion.so/placeholder.pdf").to_dict()]
    )["results"][0]["id"]

    url = upload_file(token_v2, block_id, file_path)

    payload = block.PDFBlock(url=url).to_dict()
    del payload["pdf"]["type"]
    client.update_block(block_id, payload)
    return block_id


if __name__ == "__main__":
    import os

    database_id = os.getenv("NOTION_DATABASE_ID")
    token = os.getenv("NOTION_API_TOKEN")
    token_v2 = os.getenv("NOTION_TOKEN_V2")
    page_id = create_page(
        database_id, title="test", token=token, link="https://www.notion.so"
    )

    add_mhtml_property(page_id, token, token_v2, Path("exported.mhtml"))
    add_pdf_block(page_id, token, token_v2, Path("exported.pdf"))
