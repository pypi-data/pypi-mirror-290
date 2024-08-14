# https://developers.notion.com/reference/page-property-values#type-objects

from pydantic import BaseModel


class Property(BaseModel):
    id: str = ""
    type: str

    def get_objects(self):
        return self.__dict__.get(self.type, None)

    def to_dict(self, include_meta=False, include_type=True):
        data = {str(self.type): self.get_objects()}
        if include_meta:
            data.update({"id": self.id, "type": self.type})
        if include_type:
            data.update({"type": self.type})
        return data


class ChildrenMixin:
    children: list

    def get_objects(self):
        return [child.to_dict(include_type=True) for child in self.children]


class Text(Property):
    type: str = "text"
    content: str

    def get_objects(self):
        return {"content": self.content}


class Title(ChildrenMixin, Property):
    type: str = "title"
    children: list[Text]


class Url(Property):
    type: str = "url"
    url: str


class File(Property):
    type: str = "external"
    name: str
    url: str

    def get_objects(self):
        return {
            "name": self.name,
            "type": self.type,
            self.type: {"url": self.url},
        }

    def to_dict(self, include_meta=False, include_type=False):
        return super().to_dict(include_meta, include_type).get(self.type)


class NotionHostedFile(File):
    type: str = "file"


class Files(ChildrenMixin, Property):
    type: str = "files"
    children: list[File]


if __name__ == "__main__":
    print(Url(url="https://www.notion.so").to_dict())
    print(Text(content="hello").to_dict())
    print(Title(children=[Text(content="hello")]).to_dict())
    print(Files(children=[File(name="hello", url="https://www.notion.so")]).to_dict())
    print(
        Files(
            children=[NotionHostedFile(name="hello", url="https://www.notion.so")]
        ).to_dict()
    )
