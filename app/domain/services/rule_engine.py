from typing import Dict, Any, List
import re
from app.infrastructure.database.models.rules import ExtractionRule, BusinessDictionary, FieldAlias
from app.infrastructure.database.models.document import DocumentSchema

class RuleEngineService:
    """Engine to apply deterministic regex and dictionary rules before sending data to AI."""
    
    async def apply_regex_rules(self, text: str, rules: List[ExtractionRule]) -> Dict[str, Any]:
        extracted = {}
        for rule in rules:
            if rule.rule_type == "regex":
                match = re.search(rule.pattern, text, re.IGNORECASE)
                if match:
                    extracted[rule.target_field] = match.group(1) if match.groups() else match.group(0)
        return extracted
        
    async def match_aliases(self, extracted_keys: List[str], aliases: List[FieldAlias]) -> Dict[str, str]:
        """Maps discovered aliases in text back to their standardized target fields."""
        mapped = {}
        for alias_doc in aliases:
            for alias in alias_doc.aliases:
                for key in extracted_keys:
                    if alias.lower() in key.lower():
                        mapped[key] = alias_doc.target_field
        return mapped
