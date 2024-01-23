from typing import Type, List

import pytest
from pydantic import BaseModel, Field

from pymultirole_plugins.v1.schema import Document, Token
from pymultirole_plugins.v1.tagger import TaggerBase, TaggerParameters


def test_tagger():
    with pytest.raises(TypeError) as err:
        parser = TaggerBase()
        assert parser is None
    assert (
        "Can't instantiate abstract class TaggerBase with abstract methods tag"
        in str(err.value)
    )


def test_default_options():
    options = TaggerParameters()
    assert options is not None


class DummyParameters(TaggerParameters):
    foo: str = Field("foo", description="Foo")
    bar: float = Field(0.123456789, description="Bar")


class DummyTagger(TaggerBase):
    """Dummy tagger."""

    def tag(
        self, documents: List[Document], parameters: TaggerParameters
    ) -> List[Document]:
        parameters: DummyParameters = parameters
        for document in documents:
            document.tokens = []
            for i, c in enumerate(document.text):
                document.tokens.append(Token(start=i, end=i + 1, text=c, lemma=c.lower()))
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DummyParameters


def test_dummy():
    tagger = DummyTagger()
    options = DummyParameters()
    docs: List[Document] = tagger.tag(
        [Document(text="This is a test document", metadata=options.dict())], options
    )
    assert len(docs[0].tokens) == len(docs[0].text)


def test_singleton():
    tagger1 = DummyTagger()
    tagger2 = DummyTagger()
    assert id(tagger2) == id(tagger1)
