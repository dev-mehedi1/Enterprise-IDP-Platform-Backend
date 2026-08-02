from beanie import Document
from pydantic import Field
from typing import List
from datetime import datetime, timezone

class FieldAlias(Document):
    target_field: str = Field(indexed=True) # e.g. "purchaseOrderNumber"
    aliases: List[str] # e.g. ["PO Number", "PO No", "Order Number"]
    
    class Settings:
        name = "field_aliases"

class ExtractionRule(Document):
    target_field: str = Field(indexed=True)
    rule_type: str # "regex", "dictionary", "business"
    pattern: str
    priority: int = 1
    
    class Settings:
        name = "extraction_rules"

class BusinessDictionary(Document):
    name: str = Field(unique=True) # e.g. "CurrencyCodes"
    values: List[str] # ["USD", "EUR", "GBP"]
    
    class Settings:
        name = "business_dictionaries"
