from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.kontaktart import Kontaktart

if TYPE_CHECKING:
    from ..bo.vertrag import Vertrag
    from .adresse import Adresse


class VertragskontoCBA(BaseModel):
    """
    Models a CBA (child billing account) which directly relates to a single contract. It contains information about
    locks and billing dates. But in the first place, CBAs will be grouped together by the address in their contracts.
    For each group of CBAs with a common address there will be created an MBA (master billing
    account) to support that the invoices for the CBAs can be bundled into a single invoice for the MBA.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    ouid: int = Field(..., title="Ouid")
    vertrags_adresse: "Adresse" = Field(..., alias="vertragsAdresse")
    vertragskontonummer: str = Field(..., title="Vertragskontonummer")
    rechnungsstellung: Kontaktart
    vertrag: "Vertrag"
    erstellungsdatum: datetime = Field(..., title="Erstellungsdatum")
    enddatum: Optional[datetime] = Field(default=None, title="Enddatum")
    rechnungsdatum_start: datetime = Field(..., alias="rechnungsdatumStart", title="Rechnungsdatumstart")
    rechnungsdatum_naechstes: datetime = Field(..., alias="rechnungsdatumNaechstes", title="Rechnungsdatumnaechstes")
