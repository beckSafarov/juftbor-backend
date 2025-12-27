# Tally to Database Field Mapping

This document explains how Tally form responses are mapped to database fields.

## Overview

The Tally webhook integration consists of three main components:

1. **`tally_field_mapping.py`**: Configuration file containing all mappings between Tally option IDs and database values
2. **`tally_converter.py`**: Conversion logic that transforms Tally JSON to UserCreate schema format
3. **`POST /webhook/tally`**: Webhook endpoint in main.py that receives Tally submissions and creates users

## Field Mappings

### Direct Text Fields

| Tally Question | Tally Key | Database Field | Type |
|---|---|---|---|
| Telefon raqamingiz | `question_R0MOYK` | `reg_phone` | String |
| Ism va Familyangiz | `question_oyeJdb` | `full_name` | String |
| Tug'ilgan sanangiz | `question_Oz4RYa` | `birthdate` | Date |
| Bo'yingiz (sm) | `question_jy6KWQ` | `height` | Integer |
| Vazningiz (kg) | `question_2ea2ve` | `weight` | Integer |
| O'zingiz haqingizda | `question_xpMGyd` | `biography` | Text |
| Nechta Farzandingiz | `question_P61oY1` | `number_of_children` | Integer |
| Ish joyingiz | `question_QDeGYY` | `occupation` (detail) | String |
| Nomzodlar bog'lanishi uchun raqam | `question_MbN0Yl` | `contact_phone` | String |
| Telegram akkaunt | `question_J6pyDr` | `telegram_username` | String |
| Bog'lanmoqchi bo'lganlar uchun xabar | `question_g0dBZP` | `contact_comment` | Text |

### Enum/Choice Fields (with Option ID Mapping)

#### Gender (`question_Gz9MDe` → `gender`)
| Tally Option | Option ID | DB Value |
|---|---|---|
| Erkak | `6403d166-35b0-405d-b17c-c173e104339e` | `M` |
| Ayol | `47126feb-b81a-44e6-8a1b-14be45ed4154` | `F` |

#### Marital Status (`question_V0QrYj` → `marital_status`)
| Tally Option | Option ID | DB Value |
|---|---|---|
| Hech qachon oila qurmagan | `93f3ce52-782b-4c04-abc7-dc9c183fbb56` | `S` (Single) |
| Ajrashgan | `03132d75-201a-4c2d-b9b8-9803f24d375d` | `D` (Divorced) |
| Beva | `07240243-109c-4225-85fe-de8903e242f6` | `W` (Widowed) |
| Boshqa | `c34b1bcc-00e2-48a3-b74b-fcb457222daa` | `M` (Married) |

#### Education Degree (`question_ZNExYV` → `degree`)
| Tally Option | Option ID | DB Value |
|---|---|---|
| Litsey/Kollej/Maktab | `c5c9d3ff-2d54-4f52-8426-25cc7bb440c3` | `0` |
| Bakalavr | `16588022-d4fa-4b98-b7bb-555934be90d2` | `1` |
| Magistratura | `58a056b9-1017-40b9-a73d-91c7236b6f1d` | `2` |
| Phd | `14f0dc5d-290b-4b81-b26e-d997fee27b1b` | `3` |

#### Religious Level (`question_9W9evE` → `religious_level`)
| Tally Option | Option ID | DB Value |
|---|---|---|
| Dindor emasman | `44c79fb3-df10-494a-b5b4-5da1017daf0c` | `0` |
| Farz amallarni qisman bajaraman | `4adb2ffb-e5a6-4e88-8c25-d2f5339c3ff8` | `1` |
| Farz amallarni to'liq bajaraman | `85d3e858-42e9-470f-9a98-6b42a067a163` | `2` |
| Farz va qo'shimcha amallar | `93f348ad-459e-4997-863c-91fa6f48d0a9` | `3` |

#### Contact Person (`question_Lb78Yy` → `contact_person`)
| Tally Option | Option ID | DB Value |
|---|---|---|
| O'zim | `1dabb031-466e-4661-815c-37cf91cce53c` | `s` (self) |
| Otam | `fcda8d7e-4d31-4661-9cc2-2100f67c301b` | `d` (dad) |
| Onam | `5a137ecc-af53-4130-aee6-58808d417677` | `m` (mom) |
| Akam | `c9575973-6957-4da8-9ae1-7f69d5fdd032` | `b` (brother) |
| Other (custom text) | `3320c5a4-cb04-4324-9743-8ce79c8d5d5b` | `o` (other) |

### Multi-Select Fields

#### Languages (`question_48JZvr` → `languages`)
Maps multiple language option IDs to an array of language names.

| Tally Option | Option ID | DB Value |
|---|---|---|
| O'zbek | `4de1597d-2762-4223-aec2-3d479e2e7edf` | `"O'zbek"` |
| Tojik | `31c47367-7702-4545-99ee-98a7911713bf` | `"Tojik"` |
| Rus | `5b523bee-80d0-4be8-89ae-913c9586275f` | `"Rus"` |
| Ingliz | `e1c454d4-5cc2-45d9-b638-32b48fd41462` | `"Ingliz"` |
| Qozoq | `53dd750f-fd8b-4ebc-b98b-0da1313e9810` | `"Qozoq"` |
| Turk | `5e9fa463-7170-432f-bfc3-2982704989a6` | `"Turk"` |
| Arab | `217788f7-9ff1-4e41-a708-f01a1a59b13b` | `"Arab"` |

### Location Fields

Both `native_town` (`question_EXdpDl`) and `hometown` (`question_r6aXLo`) use the same location mapping:

| Location | Sample Option IDs | DB Value |
|---|---|---|
| Toshkent shahar | `7d2a04b8...`, `fb0d9e6a...`, etc. | `"Toshkent shahar"` |
| Toshkent viloyati | `0a3ddcfd...`, `6df76ed1...`, etc. | `"Toshkent viloyati"` |
| Buxoro viloyati | `46c222b1...`, `96a2a4fa...`, etc. | `"Buxoro viloyati"` |
| ... (all 14 regions) | ... | ... |

### Matrix Fields (Habits)

The habits question (`question_e6Qb2x`) is a MATRIX type with rows (questions) and columns (answers).

**Rows (Questions):**
- `290c55eb-8213-4454-a1d0-d31a23a47eb4` → `drinks` (Ichasizmi?)
- `6a79c94a-815e-4041-bc56-db1ebe56146f` → `smokes` (Chekasizmi?)

**Columns (Answers):**
- `0ff1179c-1a7a-415f-ad63-cf296da44507` → `n` (Yo'q)
- `2eb5838f-160a-4eea-8c4e-99d6f04ead12` → `s` (Ba'zida)
- `96ba35a5-a648-4d87-9ede-27c08369b5c0` → `y` (Ha)

The converter extracts both `drinks` and `smokes` values from this single matrix question.

### Lookup Fields

#### Field of Study (`question_N6lzY0` → `field_of_study`)
Maps option IDs to field names like "Informatsion Texnologiyalar", "Transport va Logistika", etc.

#### Occupation (`question_qdDyWO` → `occupation`)
Maps option IDs to occupation names like "Dasturchi", "Logistikachi", "Menejer", etc.

## Usage

### 1. Configure Tally Webhook

In your Tally form settings, set the webhook URL to:
```
https://your-domain.com/webhook/tally
```

### 2. Automatic User Creation

When a user submits the Tally form:
1. Tally sends a POST request to `/webhook/tally`
2. The endpoint receives the JSON payload
3. `convert_tally_to_user()` transforms the data
4. UserCreate schema validates the data
5. A new User is created in the database

### 3. Manual Conversion (for testing)

```python
from app.tally_converter import convert_tally_to_user
from app.schemas import UserCreate
import json

# Load Tally response
with open("sample_tally_response.json") as f:
    tally_data = json.load(f)

# Convert to User format
user_data = convert_tally_to_user(tally_data)

# Validate and create
user = UserCreate(**user_data)
```

## Testing

Run the test script to validate the conversion:

```bash
python test_tally_conversion.py
```

## Notes

1. **Multiple Option IDs for Same Value**: Some locations and occupations have multiple option IDs (for different dropdown instances in the form) that map to the same database value.

2. **Occupation Handling**: The converter merges the occupation dropdown with the text field "Ish joyingiz" for more detailed occupation information.

3. **Contact Person "Other"**: When users select "Other" and provide custom text, the converter attempts to match patterns (like "onam", "otam") to the appropriate enum value.

4. **Default Values**: The converter sets `is_active = "a"` (active) by default for new users.

5. **Validation**: All converted data passes through the UserCreate Pydantic schema for validation before database insertion.

## Error Handling

The webhook endpoint handles:
- Invalid event types (must be `FORM_RESPONSE`)
- Duplicate phone numbers
- Duplicate Telegram IDs
- Schema validation errors
- Database errors

All errors return appropriate HTTP status codes and messages.
