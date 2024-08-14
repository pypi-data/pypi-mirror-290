# PageSaver 
[![Python version](https://img.shields.io/pypi/pyversions/pagesaver.svg?logo=python)](https://pypi.python.org/pypi/pagesaver)
[![PyPI package](https://img.shields.io/pypi/v/pagesaver.svg)](https://pypi.python.org/pypi/pagesaver)
[![PyPI download](https://img.shields.io/pypi/dm/pagesaver.svg)](https://pypi.python.org/pypi/pagesaver)
[![GitHub](https://img.shields.io/github/license/ZhaoQi99/pagesaver)](https://github.com/ZhaoQi99/pagesaver/blob/main/LICENSE)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/ZhaoQi99/pagesaver)

Archive your web page.

## Requirements
* Python >= 3.8

## Install
<details open>
<summary><img height="15" src="https://www.python.org/favicon.ico"></img> pip</summary>

```shell
pip install pagesaver
✨🍰✨
```
Or you can use `pip install git+https://github.com/ZhaoQi99/PageSaver.git
` install latest version.
</details>

<details>
<summary><img height="15" src="https://cdn.simpleicons.org/docker/338FED?viewbox=auto" /> docker</summary>

```shell
docker run -d --name pagesaver -p 8001:8001 zhaoqi99/pagesaver
```

</details>

## Quick Start
### HTTP API
1. Init PageSaver: `pagesaver init`
2. Start HTTP Server: `pagesaver server`
    > `nohup pagesaver server >> server.log 2>&1 &`
3. Examples:
```shell
~$ curl http://127.0.0.1:8001/api/record/https://www.baidu.com/?format=MHTML&format=PDF -H 'Authorization: <API_TOKEN>'
~$ curl http://127.0.0.1:8001/api/record/notion/https://www.baidu.com/?format=MHTML&format=PDF&api_token=api_token&database_id=1&token_v2=token_v2&title=test -H 'Authorization: <API_TOKEN>'
```

### CLI 
```shell
pagesaver export https://www.baidu.com -o . -f MHTML,PDF
```

## HTTP Usage
### Authorization
Using the Authorization header, format is: `Authorization: <API_TOKEN>`

### Record API
* GET `api/record/{url}?format=MHTML&format=PDF`
#### Query Params

| Parameter | Type   | Required | Description                                           |
| --------- | ------ | -------- | ----------------------------------------------------- |
| format    | string | No       | Storage format, can be MHTML or PDF, defaults to all. |

### Notion Push API
* GET `api/record/notion/{url}?format=MHTML&format=PDF&api_token=<NOTION_API_TOKEN>&database_id=<NOTION_DATABASE_ID>&token_v2=<NOTION_TOKEN_V2>&title=test`
* [Notion API Token](https://www.notion.so/profile/integrations)
* Notion Token V2: F12 -> Application -> Cookies -> token_v2
* Database ID: https://www.notion.so/{USERNAME}/{DATABASE_ID}
* Connection with: Notion ->Top right corner -> More -> Connections -> Connect to -> Your Integration

### Automations
<a href="https://www.icloud.com/shortcuts/2917f0c4c8a94654978d6b70cb5d84c0">
  <img src="https://help.apple.com/assets/645D5D228BE0233D28263F4B/645D5D258BE0233D28263F5A/zh_CN/d230a25cb974f8908871af04caad89a1.png" height="50" alt="IOS Shortcut" />
</a>


#### Query Params

| Parameter    | Type   | Required | Description                                                                                    |
| ------------ | ------ | -------- | ---------------------------------------------------------------------------------------------- |
| format       | string | No       | Storage format, can be MHTML or PDF, defaults to all.                                          |
| api_token*   | string | Yes      | Notion API Token                                                                               |
| database_id* | string | Yes      | Notion Database ID                                                                             |
| title        | string | No       | Title stored in Notion.                                                                        |
| token_v2     | string | No       | Obtained from Browser->Cookies->token_v2.To store files in Notion, this parameter is required. |

## CLI Usage
### Export
```shell
~$ pagesaver export -h
Usage: pagesaver export [OPTIONS] URL

  Export page to the output file

Options:
  -f, --format [MHTML,PDF]  Format which you want to export  [required]
  -o, --output DIRECTORY    Output directory of the file  [required]
  -n, --name TEXT           Name of the exported file  [default: exported]
  -h, --help                Show this message and exit.
```
### Server
```shell
~$ pagesaver init
~$ pagesaver server -h
Usage: pagesaver server [OPTIONS]

  Run PageSaver HTTP server

Options:
  -h, --help       Show this message and exit.
  -b, --bind TEXT  The TCP host/address to bind to.  [default: 0.0.0.0:8001]
```

## Configuration
PageSaver will read the configuration from `config.py` automatically.

### STORAGE
* type: storage type. Currently supported values are "local".
* path: path of storage.This is only used when type is set to "local".

### SERVER_BIND
The TCP host/address to bind to.

Default: `0.0.0.0:8001`

### TITLE_PROPERTY
The property name in Notion to use for the title of a page.

Default: `title`

### LINK_PROPERTY
The property name in Notion to use for the link of a page.

Default: `link`

### MHTML_PROPERTY
The property name in Notion to use for the MHTML file of a page.

Default: `mhtml`

## License
[GNU General Public License v3.0](https://github.com/ZhaoQi99/PageSaver/blob/main/LICENSE)

## Author
* Qi Zhao([zhaoqi99@outlook.com](mailto:zhaoqi99@outlook.com))
