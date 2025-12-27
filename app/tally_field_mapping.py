"""
Mapping configuration for Tally form responses to database fields.
This module contains all the mappings needed to transform Tally webhook data
into the format expected by the User model.
"""

# Map Tally question keys to database field names
FIELD_MAPPING = {
    "question_R0MOYK": "reg_phone",           # Telefon raqamingiz
    "question_oyeJdb": "full_name",           # Ism va Familyangiz
    "question_Gz9MDe": "gender",              # Jinsingiz
    "question_Oz4RYa": "birthdate",           # Tug'ilgan sanangiz
    "question_V0QrYj": "marital_status",      # Turmushdagi holatingiz
    "question_P61oY1": "number_of_children",  # Nechta Farzandingiz bor?
    "question_EXdpDl": "native_town",         # Tug'ilgan shahringiz/viloyatingiz
    "question_r6aXLo": "hometown",            # Hozirgi yashash manzilingiz
    "question_48JZvr": "languages",           # Qaysi tillarni bilasiz
    "question_jy6KWQ": "height",              # Bo'yingiz (sm)
    "question_2ea2ve": "weight",              # Vazningiz (kg)
    "question_xpMGyd": "biography",           # O'zingiz haqingizda gapirib bering
    "question_Oz4R9p": "photo_upload",        # Rasm yuklang (not in User model directly)
    "question_ZNExYV": "degree",              # Ma'lumotingiz
    "question_N6lzY0": "field_of_study",      # O'qishdagi yo'nalishingiz
    "question_qdDyWO": "occupation",          # Hozirgi kasbingiz
    "question_QDeGYY": "occupation_detail",   # Ish joyingiz (merged with occupation)
    "question_9W9evE": "religious_level",     # E'tiqod darajangizni belgilang
    "question_e6Qb2x": "habits",              # Zararli odatlar (MATRIX: drinks & smokes)
    "question_K65XDg": "habits_preferences",  # Zararli odatlar preferences (MATRIX: drinks_preference & smokes_preference)
    "question_Lb78Yy": "contact_person",      # Sizga qiziqish bildiradigan nomzod kim bilan bog'lanishi kerak?
    "question_MbN0Yl": "contact_phone",       # Nomzodlar bog'lanishi uchun raqamingiz
    "question_J6pyDr": "telegram_username",   # Telegram akkauntingiz (nickname)
    "question_g0dBZP": "contact_comment",     # Bog'lanmoqchi bo'lganlar uchun xabar qoldiring
}

# Map Tally option IDs to database enum values for Gender
GENDER_MAPPING = {
    "6403d166-35b0-405d-b17c-c173e104339e": "M",  # Erkak
    "47126feb-b81a-44e6-8a1b-14be45ed4154": "F",  # Ayol
}

# Map Tally option IDs to database enum values for Marital Status
MARITAL_STATUS_MAPPING = {
    "93f3ce52-782b-4c04-abc7-dc9c183fbb56": "S",  # Hech qachon oila qurmagan
    "03132d75-201a-4c2d-b9b8-9803f24d375d": "D",  # Ajrashgan
    "07240243-109c-4225-85fe-de8903e242f6": "W",  # Beva
    "c34b1bcc-00e2-48a3-b74b-fcb457222daa": "M",  # Boshqa (mapped to Married as fallback)
}

# Map Tally location option IDs to readable location names
LOCATION_MAPPING = {
    # For native_town and hometown
    "7d2a04b8-3351-48bb-a49b-96de0dc7a829": "Toshkent shahar",
    "fb0d9e6a-c4c6-41f3-85bf-f95ba8fd4682": "Toshkent shahar",
    "836c2b6c-ed8d-4d3d-9127-2d57df768fd9": "Toshkent shahar",
    
    "0a3ddcfd-1827-4be2-aba8-e075a7db17aa": "Toshkent viloyati",
    "6df76ed1-ed59-4c28-a89b-d07702f871af": "Toshkent viloyati",
    "31deae08-afb5-45a0-8fe5-717ce0edc021": "Toshkent viloyati",
    
    "18eb350e-09b3-47dc-a91e-c6ec0289b4a3": "Samarqand viloyati",
    "0c57fc07-2758-42fa-81a8-6bedb9d90465": "Samarqand viloyati",
    "2f3f3e82-b332-4043-a468-4684d116f61f": "Samarqand viloyati",
    
    "05bb1487-c51c-4a8d-aff3-463f2262931f": "Jizzax viloyati",
    "a4514ee5-b6ae-4419-873a-3f3b6e94ea04": "Jizzax viloyati",
    "2a85adef-1cbe-4b41-b0ac-b4eb740f6746": "Jizzax viloyati",
    
    "913b894c-55e1-48bb-b977-beadab6a7661": "Andijon viloyati",
    "7efd416f-45ab-424a-bcfd-56ed0d8fcd9d": "Andijon viloyati",
    "48c93d2a-2acd-42d7-8899-7ecad264b886": "Andijon viloyati",
    
    "7bfaeac8-9e3e-4b54-955d-a70121290b63": "Farg'ona viloyati",
    "19a646cc-9e4f-46f5-8c65-5fe37d733cb1": "Farg'ona viloyati",
    "48acf118-b847-43d1-836f-dbd009e36dac": "Farg'ona viloyati",
    
    "70f76179-49f7-4e2d-9b2d-70b744e3ce35": "Namangan viloyati",
    "e5b9809d-d754-484c-b5a2-35731241a72e": "Namangan viloyati",
    "221d1a0b-4261-4040-9e76-1a207fe6df17": "Namangan viloyati",
    
    "d865fdcc-04ce-4b15-83c8-b7cd3dd9034e": "Sirdaryo viloyati",
    "ba17bc6d-185e-45d1-8ab3-8786cdf90624": "Sirdaryo viloyati",
    "0d725f7e-6380-4163-bc8c-c6917f060b95": "Sirdaryo viloyati",
    
    "c3249113-0c6f-49e5-b274-beb521933ddd": "Qashqadaryo viloyati",
    "3d8950b5-a379-47df-b585-9297d835cc08": "Qashqadaryo viloyati",
    "3c510ac6-aa03-42bf-9bbf-d9ef899bd7f6": "Qashqadaryo viloyati",
    
    "d159c64a-45f3-4935-af15-d4cb71e55138": "Surxondaryo viloyati",
    "e53a280e-02da-45e7-9ebd-acf55b6c1461": "Surxondaryo viloyati",
    "3ea11363-a050-4ddd-9809-80f7a6dc2305": "Surxondaryo viloyati",
    
    "8ee5bdf7-68d7-40da-96b0-26ed40f24cca": "Navoiy viloyati",
    "80013ae6-c73c-4e38-a9cf-e13953a7c7ce": "Navoiy viloyati",
    "95f1c222-1f2d-42da-b010-53b44d84286e": "Navoiy viloyati",
    
    "46c222b1-a466-49f5-b483-6d0921a19a4d": "Buxoro viloyati",
    "96a2a4fa-2295-44a3-8559-c1b3bfcb4fd8": "Buxoro viloyati",
    "d1d313c7-bc9d-4a8d-92ec-94d16f8519d4": "Buxoro viloyati",
    
    "83309d91-eb79-478d-8b4b-d9ef92b5dd34": "Qoraqalpog'iston Respublikasi",
    "175f82be-8894-45eb-af3b-e7cb7fe6558e": "Qoraqalpog'iston Respublikasi",
    "f6b45697-4bd0-4cf5-909e-85c1bb6ad8c3": "Qoraqalpog'iston Respublikasi",
    
    "7d35e877-3647-4e76-927b-665321e44f6b": "Xorazm viloyati",
    "a60277ae-5ca3-49fe-8529-bde66574c234": "Xorazm viloyati",
    "7ead6071-3fe7-489c-b856-cbfd006914e8": "Xorazm viloyati",
}

# Map Tally language option IDs to language names
LANGUAGE_MAPPING = {
    "4de1597d-2762-4223-aec2-3d479e2e7edf": "O'zbek",
    "31c47367-7702-4545-99ee-98a7911713bf": "Tojik",
    "5b523bee-80d0-4be8-89ae-913c9586275f": "Rus",
    "e1c454d4-5cc2-45d9-b638-32b48fd41462": "Ingliz",
    "53dd750f-fd8b-4ebc-b98b-0da1313e9810": "Qozoq",
    "5e9fa463-7170-432f-bfc3-2982704989a6": "Turk",
    "217788f7-9ff1-4e41-a708-f01a1a59b13b": "Arab",
    "d6549d9f-93ba-4214-8869-3c4761c7fe1e": "Boshqa",
}

# Map Tally degree option IDs to database degree values (0-3)
DEGREE_MAPPING = {
    "c5c9d3ff-2d54-4f52-8426-25cc7bb440c3": 0,  # Litsey/ Kollej / Maktab
    "4acd4935-02c7-4b2a-80b8-58781ff2f6a8": 0,  # Litsey/ Kollej / Maktab (preferences)
    "16588022-d4fa-4b98-b7bb-555934be90d2": 1,  # Bakalavr
    "caaa8b26-a98b-4838-82b0-913b718110f0": 1,  # Bakalavr (preferences)
    "58a056b9-1017-40b9-a73d-91c7236b6f1d": 2,  # Magistratura
    "9265c201-104e-4e1f-935f-f6164f99565a": 2,  # Magistratura (preferences)
    "14f0dc5d-290b-4b81-b26e-d997fee27b1b": 3,  # Phd
    "13c11b9c-e0c3-405f-8415-d08294b45e71": 3,  # Phd (preferences)
}

# Map Tally field of study option IDs to field names
FIELD_OF_STUDY_MAPPING = {
    "967cf3e0-1b95-4265-b10d-c1d7ecc839e6": "Informatsion Texnologiyalar",
    "cf6d45aa-804c-4264-aff4-537e62312743": "Media va Jurnalistika",
    "847f32e0-10df-4e80-87ae-c00bf26a30a0": "Transport va Logistika",
    "a650df31-6ddd-4cbb-82b5-3357e14ee4ac": "Aloqa va Kommunikatsiya",
    "a563b670-7f34-4ef9-b712-da4ab792f17c": "Biznes va Menejment",
    "2175756c-1f1a-44a1-b94f-b527ef629322": "Moliya va Buxgalteriya",
    "85d623e2-a0d7-45e3-a0fc-9c5d62bb0ff1": "Boshqa gumanitar",
    "8f413ca2-a49c-4ee9-9eae-38f469b6c1f0": "Huquq va Qonun",
    "cef12dc4-f593-430b-a6f0-e4f1f4f7d948": "Psixologiya",
    "4a5e50ed-9e42-495f-9b75-e6faa55e478d": "Tibbiyot",
}

# Map Tally occupation option IDs to occupation names
OCCUPATION_MAPPING = {
    "89a32786-afe0-48ae-8cd6-bd3e2585a5ea": "Dasturchi",
    "21b17816-8472-41cd-a541-ff3df37f5fa4": "Dasturchi",
    "25100bf6-5bd5-4846-ab16-74883d52b94c": "Logistikachi",
    "72cded44-3fd1-4506-a997-18b7aae5079a": "Logistikachi",
    "523e572c-eaf8-487a-92bd-ad47f22a12fb": "Operator",
    "8be7f45f-5754-45f6-b83b-79c3770c1e2f": "Operator",
    "f09bc654-314b-4912-9ba4-dfd35c993ac3": "Sotuvchi",
    "426f6f9e-286c-42f3-844b-6989cf36de50": "Sotuvchi",
    "cf61b931-9a19-46e5-9dcc-f9bc8545d19e": "Analitik",
    "934439af-6e0c-4bc2-bada-38340a447ce4": "Analitik",
    "340aacc0-5465-4b89-8890-318c1a4a56ce": "Tadbirkor",
    "e7a5de98-086a-4440-9995-77fae18ea892": "Tadbirkor",
    "0726e7be-0159-45f2-a294-ef2b1b1135aa": "Menejer",
    "dd32da01-45d6-462d-9021-f837bd6977de": "Menejer",
    "23ea378b-94f3-49d8-9655-174f5c8b6f1b": "Buxgalter",
    "c9790d41-08aa-4a9b-b0d5-6b495b21eb21": "Buxgalter",
    "d8f32c7b-360a-40a5-b1d4-74b9c11b1640": "Boshqa",
    "487b5ccd-ee20-4804-baad-9595bee55297": "Boshqa",
    "5e1fff73-9e53-4f5e-988c-131df4e4a2cf": "Talaba",
    "f3c249ec-7680-4514-9e41-248e673c1bff": "Talaba",
}

# Map Tally religious level option IDs to database values (0-3)
RELIGIOUS_LEVEL_MAPPING = {
    "44c79fb3-df10-494a-b5b4-5da1017daf0c": 0,  # Dindor emasman
    "56f9eb2c-b688-4c79-885d-3bc958d5a528": 0,  # Dindor emas (preferences)
    "4adb2ffb-e5a6-4e88-8c25-d2f5339c3ff8": 1,  # Farz amallarni qisman bajaraman
    "0f59dd2c-6a1e-42db-90bf-7e7928f8a133": 1,  # Farz amallarni qisman bajarishi kerak (preferences)
    "85d3e858-42e9-470f-9a98-6b42a067a163": 2,  # Farz amallarni to'liq bajaraman
    "cbbfa680-0113-4a72-aaa6-39214c5cb2a0": 2,  # Farz amallarni to'liq bajarishi kerak (preferences)
    "93f348ad-459e-4997-863c-91fa6f48d0a9": 3,  # Farz va qo'shimcha amallarni doimiy bajraman
    "1731ccd1-d2f2-4945-8d82-d5b12f5eb956": 3,  # Farz va qo'shimcha amallarni doimiy bajarishi kerak (preferences)
}

# Map Tally habits column IDs to database values
# For MATRIX questions: rows are questions, columns are answers
HABITS_COLUMN_MAPPING = {
    "0ff1179c-1a7a-415f-ad63-cf296da44507": "n",  # Yo'q
    "a5fa56a2-9764-4b47-b395-7dccd0804e6c": "n",  # Yo'q (preferences)
    "2eb5838f-160a-4eea-8c4e-99d6f04ead12": "s",  # Ba'zida
    "e87b66de-2984-4398-9fe7-55fe5e67cd94": "s",  # Ba'zida (preferences)
    "96ba35a5-a648-4d87-9ede-27c08369b5c0": "y",  # Ha
    "311dcd34-1217-4e3c-bfab-b31509e5793e": "y",  # Ha (preferences)
}

# Map Tally habits row IDs to field names
HABITS_ROW_MAPPING = {
    "290c55eb-8213-4454-a1d0-d31a23a47eb4": "drinks",      # Ichasizmi?
    "d00ef8b5-e757-4f46-a557-0908ecb1c2e0": "drinks_preference",  # Ichadi (preferences)
    "6a79c94a-815e-4041-bc56-db1ebe56146f": "smokes",      # Chekasizmi?
    "6bd5909c-c916-4bc6-8021-24dec6dad819": "smokes_preference",  # Chekadi (preferences)
}

# Map Tally contact person option IDs to database text values
# For known options, use short codes (s, d, m, b)
# For "other" option with custom text, use the custom text directly (after pattern matching)
CONTACT_PERSON_MAPPING = {
    "1dabb031-466e-4661-815c-37cf91cce53c": "s",  # O'zim -> self
    "fcda8d7e-4d31-4661-9cc2-2100f67c301b": "d",  # Otam -> dad
    "5a137ecc-af53-4130-aee6-58808d417677": "m",  # Onam -> mom
    "c9575973-6957-4da8-9ae1-7f69d5fdd032": "b",  # Akam -> brother
    # Note: "other" option (3320c5a4-cb04-4324-9743-8ce79c8d5d5b) is handled specially
    # It will first try to match patterns below, otherwise use the raw custom text
}

# Contact person text patterns for "other" option
# If custom text matches these patterns, use the short code
# Otherwise, use the custom text as-is (e.g., "Qo'shnim", "Amakam", etc.)
CONTACT_PERSON_TEXT_PATTERNS = {
    "o'zim": "s",
    "özim": "s",
    "ozim": "s",
    "otam": "d",
    "ota": "d",
    "dad": "d",
    "father": "d",
    "onam": "m",
    "ona": "m",
    "mom": "m",
    "mother": "m",
    "akam": "b",
    "aka": "b",
    "brother": "b",
}
