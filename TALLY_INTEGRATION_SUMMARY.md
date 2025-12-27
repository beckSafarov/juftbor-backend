# Tally Integration - Quick Reference

## Files Created

1. **`app/tally_field_mapping.py`** - Complete mapping configuration
   - Maps Tally question keys to database field names
   - Maps all option IDs to database enum values
   - Handles all field types: gender, marital status, locations, languages, etc.

2. **`app/tally_converter.py`** - Conversion utility
   - `TallyConverter` class: Transforms Tally JSON to User format
   - `convert_tally_to_user()` function: Convenience function for quick conversion
   - Handles all field types including MATRIX questions for habits

3. **`POST /webhook/tally`** endpoint in `main.py`
   - Receives Tally webhook POST requests
   - Validates event type is `FORM_RESPONSE`
   - Converts data using `convert_tally_to_user()`
   - Creates user in database
   - Returns success/error response

4. **`test_tally_conversion.py`** - Test script
   - Tests conversion with `sample_tally_response.json`
   - Validates output against UserCreate schema
   - Run with: `python test_tally_conversion.py`

5. **`TALLY_MAPPING_GUIDE.md`** - Documentation
   - Complete field mapping reference
   - Usage examples
   - Testing instructions

## Quick Usage

### Set up Tally webhook:
```
URL: https://your-domain.com/webhook/tally
Method: POST
```

### Manual conversion:
```python
from app.tally_converter import convert_tally_to_user
from app.schemas import UserCreate

user_data = convert_tally_to_user(tally_response_json)
user = UserCreate(**user_data)
```

### Test the conversion:
```bash
python test_tally_conversion.py
```

## Example Flow

1. User submits Tally form
2. Tally webhook sends JSON to `/webhook/tally`
3. Endpoint converts: `convert_tally_to_user(tally_json)`
4. Validates: `UserCreate(**user_data)`
5. Saves to database: `User(**user_data)`
6. Returns: `{"success": true, "user_id": 123}`

## Key Mappings

- **Gender**: `6403d166...` → `M`, `47126feb...` → `F`
- **Marital Status**: IDs → `S`, `D`, `W`, `M`
- **Degree**: IDs → `0-3`
- **Religious Level**: IDs → `0-3`
- **Habits (Matrix)**: Row+Column IDs → `drinks`, `smokes` (`n`/`s`/`y`)
- **Languages**: Multiple IDs → Array of language names
- **Locations**: IDs → Location names (14 regions)

See `TALLY_MAPPING_GUIDE.md` for complete mapping details.
