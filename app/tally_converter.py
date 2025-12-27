"""
Tally to User Converter
Transforms Tally webhook responses into UserCreate schema format.
"""
from typing import Dict, Any, Optional, List
from datetime import date
from app.tally_field_mapping import (
    FIELD_MAPPING,
    GENDER_MAPPING,
    MARITAL_STATUS_MAPPING,
    LOCATION_MAPPING,
    LANGUAGE_MAPPING,
    DEGREE_MAPPING,
    FIELD_OF_STUDY_MAPPING,
    OCCUPATION_MAPPING,
    RELIGIOUS_LEVEL_MAPPING,
    HABITS_COLUMN_MAPPING,
    HABITS_ROW_MAPPING,
    CONTACT_PERSON_MAPPING,
    CONTACT_PERSON_TEXT_PATTERNS,
)


class TallyConverter:
    """Converts Tally form responses to User model format"""
    
    def __init__(self, tally_response: Dict[str, Any]):
        """
        Initialize converter with Tally webhook response.
        
        Args:
            tally_response: Full Tally webhook JSON response
        """
        self.tally_response = tally_response
        self.fields = {field["key"]: field for field in tally_response.get("data", {}).get("fields", [])}
        self.user_data = {}
    
    def convert(self) -> Dict[str, Any]:
        """
        Convert Tally response to UserCreate-compatible dict.
        
        Returns:
            Dictionary matching UserCreate schema
        """
        # Process all fields
        for tally_key, db_field in FIELD_MAPPING.items():
            if tally_key not in self.fields:
                continue
            
            field = self.fields[tally_key]
            value = field.get("value")
            
            if value is None:
                continue
            
            # Route to appropriate handler based on field type and name
            if db_field == "gender":
                self._convert_gender(value)
            elif db_field == "marital_status":
                self._convert_marital_status(value)
            elif db_field in ["native_town", "hometown"]:
                self._convert_location(db_field, value)
            elif db_field == "languages":
                self._convert_languages(value)
            elif db_field == "degree":
                self._convert_degree(value)
            elif db_field == "field_of_study":
                self._convert_field_of_study(value)
            elif db_field in ["occupation", "occupation_detail"]:
                self._convert_occupation(value, tally_key)
            elif db_field == "religious_level":
                self._convert_religious_level(value)
            elif db_field == "habits":
                self._convert_habits(value)
            elif db_field == "habits_preferences":
                self._convert_habits(value)
            elif db_field == "contact_person":
                self._convert_contact_person(value, field)
            elif db_field in ["birthdate"]:
                self._convert_date(db_field, value)
            elif db_field in ["height", "weight", "number_of_children"]:
                self._convert_integer(db_field, value)
            else:
                # Direct mapping for simple fields
                self.user_data[db_field] = value
        
        # Set default is_active status
        self.user_data["is_active"] = "a"
        
        return self.user_data
    
    def _convert_gender(self, value: List[str]):
        """Convert gender option ID to enum value"""
        if value and len(value) > 0:
            gender_id = value[0]
            self.user_data["gender"] = GENDER_MAPPING.get(gender_id, "M")
    
    def _convert_marital_status(self, value: List[str]):
        """Convert marital status option ID to enum value"""
        if value and len(value) > 0:
            status_id = value[0]
            self.user_data["marital_status"] = MARITAL_STATUS_MAPPING.get(status_id)
    
    def _convert_location(self, field_name: str, value: List[str]):
        """Convert location option ID to location name"""
        if value and len(value) > 0:
            location_id = value[0]
            self.user_data[field_name] = LOCATION_MAPPING.get(location_id, "Unknown")
    
    def _convert_languages(self, value: List[str]):
        """Convert language option IDs to language names"""
        if value and len(value) > 0:
            languages = [LANGUAGE_MAPPING.get(lang_id, "Unknown") for lang_id in value]
            self.user_data["languages"] = languages
    
    def _convert_degree(self, value: List[str]):
        """Convert degree option ID to integer (0-3)"""
        if value and len(value) > 0:
            degree_id = value[0]
            self.user_data["degree"] = DEGREE_MAPPING.get(degree_id, 0)
    
    def _convert_field_of_study(self, value: List[str]):
        """Convert field of study option ID to field name"""
        if value and len(value) > 0:
            field_id = value[0]
            self.user_data["field_of_study"] = FIELD_OF_STUDY_MAPPING.get(field_id, "Other")
    
    def _convert_occupation(self, value: Any, tally_key: str):
        """Convert occupation - merge occupation and occupation_detail"""
        if tally_key == "question_qdDyWO":
            # Main occupation dropdown
            if value and len(value) > 0:
                occupation_id = value[0]
                occupation = OCCUPATION_MAPPING.get(occupation_id, "Unknown")
                
                # If it's "Boshqa", will be overridden by occupation_detail
                if occupation != "Boshqa":
                    self.user_data["occupation"] = occupation
        elif tally_key == "question_QDeGYY":
            # Occupation detail text field (Ish joyingiz)
            if value:
                # If occupation is already set to "Boshqa", replace it
                if self.user_data.get("occupation") == "Boshqa" or "occupation" not in self.user_data:
                    self.user_data["occupation"] = value
                else:
                    # Append as additional detail
                    self.user_data["occupation"] = f"{self.user_data['occupation']} - {value}"
    
    def _convert_religious_level(self, value: List[str]):
        """Convert religious level option ID to integer (0-3)"""
        if value and len(value) > 0:
            level_id = value[0]
            self.user_data["religious_level"] = RELIGIOUS_LEVEL_MAPPING.get(level_id, 0)
    
    def _convert_habits(self, value: Dict[str, List[str]]):
        """
        Convert MATRIX question for habits (drinks/smokes).
        
        Args:
            value: Dict with row IDs as keys and list of column IDs as values
        """
        if not isinstance(value, dict):
            return
        
        for row_id, column_ids in value.items():
            field_name = HABITS_ROW_MAPPING.get(row_id)
            if field_name and column_ids and len(column_ids) > 0:
                column_id = column_ids[0]
                habit_value = HABITS_COLUMN_MAPPING.get(column_id, "n")
                self.user_data[field_name] = habit_value
    
    def _convert_contact_person(self, value: Any, field: Dict[str, Any]):
        """
        Convert contact person option.
        Handles both predefined options (mapped to short codes: s, d, m, b)
        and "other" text inputs (either pattern-matched or custom text).
        """
        if not value:
            return
        
        # Value can be a list of option IDs or strings
        if isinstance(value, list) and len(value) > 0:
            contact_value = value[0]
            
            # Check if it's a string value
            if isinstance(contact_value, str):
                # First check if it's a known option ID
                if contact_value in CONTACT_PERSON_MAPPING:
                    self.user_data["contact_person"] = CONTACT_PERSON_MAPPING[contact_value]
                    return
                
                # Not a known ID, so it's custom text from "other" option
                # Try to match patterns first
                text_lower = contact_value.lower().strip()
                for pattern, short_code in CONTACT_PERSON_TEXT_PATTERNS.items():
                    if pattern in text_lower:
                        self.user_data["contact_person"] = short_code
                        return
                
                # No pattern matched, use the custom text as-is
                self.user_data["contact_person"] = contact_value
                return
        
        # Check if there's an "other" option with custom text in the field options
        options = field.get("options", [])
        for option in options:
            if option.get("isOtherOption") and isinstance(value, list):
                for val in value:
                    if isinstance(val, str):
                        # Try to map the custom text to known patterns
                        text_lower = val.lower().strip()
                        for pattern, short_code in CONTACT_PERSON_TEXT_PATTERNS.items():
                            if pattern in text_lower:
                                self.user_data["contact_person"] = short_code
                                return
                        
                        # No pattern matched, use custom text as-is
                        self.user_data["contact_person"] = val
                        return
    
    def _convert_date(self, field_name: str, value: str):
        """Convert date string to date object"""
        try:
            # Tally sends dates in ISO format: YYYY-MM-DD
            self.user_data[field_name] = value
        except (ValueError, AttributeError):
            pass
    
    def _convert_integer(self, field_name: str, value: Any):
        """Convert value to integer"""
        try:
            self.user_data[field_name] = int(value)
        except (ValueError, TypeError):
            pass
    
    def get_user_create_dict(self) -> Dict[str, Any]:
        """
        Get the converted data as a dict ready for UserCreate validation.
        Alias for convert() for clearer intent.
        """
        return self.convert()


def convert_tally_to_user(tally_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to convert Tally response to User data.
    
    Args:
        tally_response: Full Tally webhook JSON response
    
    Returns:
        Dictionary matching UserCreate schema
    
    Example:
        >>> tally_data = {...}  # Tally webhook response
        >>> user_data = convert_tally_to_user(tally_data)
        >>> user = UserCreate(**user_data)
    """
    converter = TallyConverter(tally_response)
    return converter.get_user_create_dict()
