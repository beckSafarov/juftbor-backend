# User Creation Endpoint - Quick Summary

## ✅ What Was Created

### 1. Sample JSON Files
- **`sample_user.json`**: Male user example (Alisher Karimov)
- **`sample_user_female.json`**: Female user example (Madina Rahimova)

Both files contain all fields needed to create a user with realistic Uzbek data.

### 2. Pydantic Schemas (`app/schemas/`)
- **`UserCreate`**: Input validation for creating users
  - Required fields validation
  - Age validation (18+)
  - Field constraints (height, weight, degree, etc.)
  - Enum validation for gender, marital status, etc.
  
- **`UserResponse`**: Output format for user data
  - Converts SQLAlchemy models to JSON

- **`UserUpdate`**: Schema for future update endpoint

### 3. FastAPI Endpoints (`app/main.py`)

#### POST `/users` - Create User
- Accepts JSON matching `UserCreate` schema
- Validates all fields
- Checks for duplicate phone/telegram_id
- Returns created user with ID

#### GET `/users/{user_id}` - Get Single User
- Returns user by ID
- 404 if not found

#### GET `/users` - List Users
- Pagination support (skip, limit)
- Returns list of users

### 4. Test Files
- **`test_create_user.py`**: Python script to test endpoint
- **`API_TESTING.md`**: Complete testing guide

## 🚀 How to Use

### Step 1: Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=postgresql+asyncpg://user:pass@localhost/juftbor" > .env

# Initialize database
python init_db.py
```

### Step 2: Start Server
```bash
uvicorn app.main:app --reload
```

### Step 3: Test Endpoint

**Option A: Using test script**
```bash
python test_create_user.py
```

**Option B: Using curl**
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d @sample_user.json
```

**Option C: Using Swagger UI**
1. Visit http://localhost:8000/docs
2. Try the POST /users endpoint

## 📋 Sample User Fields Explained

### Required Fields
```json
{
  "full_name": "Alisher Karimov",        // Full name
  "birthdate": "1995-03-15",             // Must be 18+
  "gender": "M",                         // M or F
  "reg_phone": "+998901234567"           // Unique phone number
}
```

### Contact (at least one required)
```json
{
  "contact_phone": "+998901234567",      // Contact phone
  "telegram_id": 123456789               // Telegram user ID
}
```

### Optional Personal Info
```json
{
  "marital_status": "S",                 // S/M/D/W
  "native_town": "Tashkent",
  "hometown": "Samarkand",
  "languages": ["Uzbek", "Russian"],
  "height": 178,                         // cm
  "weight": 75,                          // kg
  "biography": "About me..."
}
```

### Optional Professional
```json
{
  "degree": 1,                           // 0-3
  "field_of_study": "Computer Science",
  "occupation": "Software Developer"
}
```

### Optional Lifestyle
```json
{
  "religious_level": 2,                  // 0-3
  "drinks": "n",                         // n/s/y
  "smokes": "n"                          // n/s/y
}
```

### Optional Contact Details
```json
{
  "contact_person": "s",                 // s/d/m/b/o
  "telegram_username": "alisher_dev",
  "contact_comment": "Prefer evening calls"
}
```

## ✨ Key Features

### Validation
- ✅ Age must be 18+
- ✅ Phone numbers must be unique
- ✅ Telegram IDs must be unique
- ✅ Height: 100-250cm
- ✅ Weight: 30-300kg
- ✅ Enums validated automatically

### Error Handling
- 400: Duplicate phone/telegram_id
- 422: Validation errors
- 404: User not found
- 500: Server errors

### Response Format
```json
{
  "id": 1,
  "full_name": "Alisher Karimov",
  "birthdate": "1995-03-15",
  "gender": "M",
  // ... all other fields
}
```

## 📝 Testing Multiple Users

Create different users by modifying:
1. `reg_phone` (must be unique)
2. `telegram_id` (must be unique)
3. Personal details

Example:
```bash
# Create male user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d @sample_user.json

# Create female user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d @sample_user_female.json
```

## 🎯 Next Steps

Now that users can be created, you can:
1. Add metadata endpoints (bot activation, etc.)
2. Add preferences endpoints (matching criteria)
3. Add interest endpoints (express interest)
4. Build telegram bot integration
5. Implement matching algorithm

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (when server running)
- **Full Testing Guide**: See `API_TESTING.md`
- **Models Documentation**: See `app/models/README.md`
- **Database Schema**: See `juftbor-db-production.sql`
