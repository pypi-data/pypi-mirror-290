from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field

CobroswapCurrency = Literal["UYU"]
DEFAULT_CURRENCY = "UYU"
DEFAULT_CONCEPT = "Membresia 3 meses"                   # FIXME: Hardcodeado.


class CobrosWapJSON(BaseModel):
    amount: float
    currency: CobroswapCurrency = DEFAULT_CURRENCY      # FIXME: Que monedas acepta?
    concept: str = Field(DEFAULT_CONCEPT)
    companyId: str

class PaymentLink(BaseModel):
    id: str
    expires_at: datetime
    qr_code: str
    url: str

class ResponseCobrosWap(BaseModel):
    message: str
    paymentLink: PaymentLink
