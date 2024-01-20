import requests
from typing import Dict
from datetime import datetime

from .config import (
    PRIVATBANK_CURRENCIES_CASHE_RATE_URI,
    PRIVATBANK_CURRENCIES_NON_CASHE_RATE_URI,
    PRIVATBANK_BALANCE_URI,
    PRIVATBANK_BALANCE_URI_BODY,
    PRIVATBANK_STATEMENT_URI,
    PRIVATBANK_STATEMENT_URI_BODY,
    PRIVATBANK_PAYMENT_URI,
    DOCUMENT_NUMBER,
    DOCUMENT_TYPE,
    PAYMENT_CCY,
    PAYMENT_DESTINATION,
    PAYMENT_NAMING,
    RECIPIENT_IFI,
    RECIPIENT_IFI_TEXT,
    RECIPIENT_NCEO,
)


class BasePrivatManager:
    def __init__(self, token=None, iban=None):
        self._token = token
        self._iban = iban

    _privat_balance_uri_body = PRIVATBANK_BALANCE_URI_BODY
    _privat_statement_uri_body = PRIVATBANK_STATEMENT_URI_BODY

    _privat_currencies_cashe_rate_uri = PRIVATBANK_CURRENCIES_CASHE_RATE_URI
    _privat_currencies_non_cashe_rate_uri = PRIVATBANK_CURRENCIES_NON_CASHE_RATE_URI
    _privat_balance_uri = PRIVATBANK_BALANCE_URI
    _privat_statement_uri = PRIVATBANK_STATEMENT_URI
    _privat_payment_uri = PRIVATBANK_PAYMENT_URI

    _document_number = DOCUMENT_NUMBER
    _document_type = DOCUMENT_TYPE
    _payment_ccy = PAYMENT_CCY
    _payment_destination = PAYMENT_DESTINATION
    _payment_naming = PAYMENT_NAMING
    _recipient_ify = RECIPIENT_IFI
    _recipient_ify_text = RECIPIENT_IFI_TEXT
    _recipient_nceo = RECIPIENT_NCEO

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, new_token: str):
        self._token = new_token

    @property
    def iban(self) -> str:
        return self._iban

    @iban.setter
    def iban(self, new_iban: str):
        self._iban = new_iban

    @property
    def privat_currencies_cashe_rate_uri(self) -> str:
        return self._privat_currencies_cashe_rate_uri

    @privat_currencies_cashe_rate_uri.setter
    def privat_currencies_cashe_rate_uri(self, new_uri: str):
        self._privat_currencies_cashe_rate_uri = new_uri

    @property
    def privat_currencies_non_cashe_rate_uri(self) -> str:
        return self._privat_currencies_non_cashe_rate_uri

    @privat_currencies_non_cashe_rate_uri.setter
    def privat_currencies_non_cashe_rate_uri(self, new_uri: str):
        self._privat_currencies_non_cashe_rate_uri = new_uri

    @property
    def privat_balance_uri(self) -> str:
        return self._privat_balance_uri

    @privat_balance_uri.setter
    def privat_balance_uri(self, new_uri: str):
        self._privat_balance_uri = new_uri

    @property
    def privat_statement_uri(self) -> str:
        return self._privat_statement_uri

    @privat_statement_uri.setter
    def privat_statement_uri(self, new_uri: str):
        self._privat_statement_uri = new_uri

    @property
    def privat_payment_uri(self) -> str:
        return self._privat_payment_uri

    @privat_payment_uri.setter
    def privat_payment_uri(self, new_uri: str):
        self._privat_payment_uri = new_uri

    @property
    def privat_balance_uri_body(self) -> str:
        return self._privat_balance_uri_body

    @privat_balance_uri_body.setter
    def privat_balance_uri_body(self, new_uri_body: str):
        self._privat_balance_uri_body = new_uri_body

    @property
    def privat_statement_uri_body(self) -> str:
        return self._privat_statement_uri_body

    @privat_statement_uri_body.setter
    def privat_statement_uri_body(self, new_uri_body: str):
        self._privat_statement_uri_body = new_uri_body

    @property
    def document_number(self) -> str:
        return self._document_number

    @document_number.setter
    def document_number(self, new_document_number: str):
        self._document_number = new_document_number

    @property
    def document_type(self) -> str:
        return self._document_type

    @document_type.setter
    def document_type(self, new_document_type: str):
        self._document_type = new_document_type

    @property
    def payment_ccy(self) -> str:
        return self._payment_ccy

    @payment_ccy.setter
    def payment_ccy(self, new_payment_ccy: str):
        self._payment_ccy = new_payment_ccy

    @property
    def payment_destination(self) -> str:
        return self._payment_destination

    @payment_destination.setter
    def payment_destination(self, new_payment_destination: str):
        self._payment_destination = new_payment_destination

    @property
    def payment_naming(self) -> str:
        return self._payment_naming

    @payment_naming.setter
    def payment_naming(self, new_payment_naming: str):
        self._payment_naming = new_payment_naming

    @property
    def recipient_ify(self) -> str:
        return self._recipient_ify

    @recipient_ify.setter
    def recipient_ify(self, new_recipient_ify: str):
        self._recipient_ify = new_recipient_ify

    @property
    def recipient_ify_text(self) -> str:
        return self._recipient_ify_text

    @recipient_ify_text.setter
    def recipient_ify_text(self, new_recipient_ify_text: str):
        self._recipient_ify_text = new_recipient_ify_text

    @property
    def recipient_nceo(self) -> str:
        return self._recipient_nceo

    @recipient_nceo.setter
    def recipient_nceo(self, new_recipient_nceo: str):
        self._recipient_nceo = new_recipient_nceo

    @classmethod
    def session(cls) -> requests.sessions.Session:
        return requests.Session()

    @staticmethod
    def date(period: int) -> Dict:
        _day = 86400  # 1 day (UNIX)
        try:
            time_delta = int(datetime.now().timestamp()) - (period * _day)
            dt_object = datetime.fromtimestamp(time_delta)
            year = dt_object.strftime("%Y")
            month = dt_object.strftime("%m")
            day = dt_object.strftime("%d")
            date = f"{day}-{str(month)}-{year}"
            payload = {"date": date}
            return payload
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception

    def payment_body(self, recipient: str, amount: float, iban: str) -> Dict:
        try:
            payment_body = {
                "document_number": self.document_number,
                "recipient_card": recipient,
                "recipient_nceo": self.recipient_nceo,
                "payment_naming": self.payment_naming,
                "payment_amount": amount,
                "recipient_ifi": self.recipient_ify,
                "recipient_ifi_text": self.recipient_ify_text,
                "payment_destination": self.payment_destination,
                "payer_account": iban,
                "payment_ccy": self.payment_ccy,
                "document_type": self.document_type,
            }
            return payment_body
        except Exception as exc:
            exception = {"detail": str(exc)}
            return exception
