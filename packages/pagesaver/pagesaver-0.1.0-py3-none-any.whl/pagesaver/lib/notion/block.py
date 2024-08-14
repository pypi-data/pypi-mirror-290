from pydantic import BaseModel


class Block(BaseModel):
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


class PDFBlock(Block):
    type: str = "pdf"
    url: str
    external: bool = True

    def get_objects(self):
        pdf_type = "external" if self.external else "file"
        return {
            "type": pdf_type,
            pdf_type: {"url": self.url},
        }


if __name__ == "__main__":
    print(PDFBlock(url="https://www.notion.so/placeholder.pdf").to_dict())
