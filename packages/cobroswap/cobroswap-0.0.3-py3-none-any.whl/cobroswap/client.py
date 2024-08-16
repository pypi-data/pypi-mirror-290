from cobroswap.payment_link import create_payment_link
from cobroswap.models import (
    CobrosWapJSON, ResponseCobrosWap, CobroswapCurrency,
    DEFAULT_CURRENCY, DEFAULT_CONCEPT
)


class CobrosWap:
    def __init__(self, *, company_id: str):
        self._company_id = company_id

    @property
    def company_id(self) -> str:
        return self._company_id

    def create_payment_link(
            self,
            *,
            amount: float,
            currency: CobroswapCurrency = DEFAULT_CURRENCY,
            concept: str = DEFAULT_CONCEPT
        ) -> ResponseCobrosWap | None:
        cobroswap_json = CobrosWapJSON(
            amount=amount,
            currency=currency,
            concept=concept,
            companyId=self.company_id
        )
        return create_payment_link(cobroswap_json=cobroswap_json)
