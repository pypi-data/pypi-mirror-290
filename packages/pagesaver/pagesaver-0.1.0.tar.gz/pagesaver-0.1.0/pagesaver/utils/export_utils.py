from pathlib import Path
from typing import TypeVar

from playwright.sync_api import Page, sync_playwright

from pagesaver.enums import ExportFormat


def _export_pdf(page: Page, path: Path) -> str:
    pdf_path = path.with_suffix(".pdf").as_posix()
    page.emulate_media(media="screen")
    page.pdf(path=pdf_path)
    return pdf_path


def _export_mhtml(page: Page, path: Path) -> str:
    mhtml_path = path.with_suffix(".mhtml")
    client = page.context.new_cdp_session(page)
    data = client.send("Page.captureSnapshot", {"format": "mhtml"})
    mhtml_path.write_bytes(data["data"].encode("utf-8"))
    return mhtml_path.as_posix()


T = TypeVar("T", bound=ExportFormat)


def export(
    url: str,
    path: Path,
    formats: list[T],
    headless: bool = True,
    proxy: str | None = None,
    **browser_decls,
):
    """
    Args:
        url (str): The url you want to export
        path (Path): The directory of the exported file
        formats (List[T]): The format you want to export
        headless (bool, optional): Whether to use headless mode. Defaults to True.
        browser_decls (Dict, optional): The browser declaration. Defaults to {}.
    Return:
        (list[dict[str]], dict[str]): The path list and the page information
    """
    if proxy:
        browser_decls["proxy"] = {"server": proxy}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)

        context = browser.new_context(**browser_decls)
        page = context.new_page()
        page.goto(url)

        page.wait_for_load_state("networkidle")
        info = {
            "title": page.title(),
        }
        # Wait img
        locators = page.locator("img").all()
        for locator in locators:
            locator.evaluate("node => node.scrollIntoView()")
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_load_state("networkidle")

        # Back to top
        page.evaluate("() => window.scrollTo(0, 0)")

        path_lst = list()
        # pdf
        if ExportFormat.PDF in formats:
            path_lst.append(
                {
                    "format": ExportFormat.PDF.value,
                    "path": _export_pdf(page, path),
                }
            )

        # mhtml
        if ExportFormat.MHTML in formats:
            path_lst.append(
                {
                    "format": ExportFormat.MHTML.value,
                    "path": _export_mhtml(page, path),
                }
            )

        browser.close()
        return (path_lst, info)


if __name__ == "__main__":
    export(
        "https://www.baidu.com",
        Path("").absolute() / "test",
        [ExportFormat.PDF],
    )
