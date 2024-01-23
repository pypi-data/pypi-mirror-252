import abc
from typing import Type, List, Optional
from pydantic import BaseModel, Field

from pymultirole_plugins.v1 import ABCSingleton
from pymultirole_plugins.v1.schema import Document


class TaggerParameters(BaseModel):
    outputFields: Optional[str] = Field(None, description="Output fields. None means all")


class TaggerBase(metaclass=ABCSingleton):
    """Base class for example plugin used in the tutorial."""

    def __init__(self):
        pass

    @abc.abstractmethod
    def tag(
        self, documents: List[Document], options: TaggerParameters
    ) -> List[Document]:
        """Tag the input documents and return the modified documents.

        :param document: An tagged document.
        :param options: options of the parser.
        :returns: Document.
        """

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return TaggerParameters
