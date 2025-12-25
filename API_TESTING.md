# Testing User Creation Endpoint

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Database
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/juftbor
```

### 3. Initialize Database
```bash
python init_db.py
```

This will create all tables in your PostgreSQL database.

## Running the API Server

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing the Create User Endpoint

### Method 1: Using the Test Script

```bash
pip install requests  # If not already installed
python test_create_user.py
```

### Method 2: Using curl

```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d @sample_user.json
```

### Method 3: Using HTTPie

```bash
pip install httpie
http POST localhost:8000/users < sample_user.json
```

### Method 4: Using Swagger UI

1. Go to http://localhost:8000/docs
2. Find the `POST /users` endpoint
3. Click "Try it out"
4. Copy the contents of `sample_user.json` into the request body
5. Click "Execute"

### Method 5: Using Python requests

```python
import requests

user_data = {
    "full_name": "Alisher Karimov",
    "birthdate": "1995-03-15",
    "gender": "M",
    "marital_status": "S",
    "reg_phone": "+998901234567",
    "telegram_id": 123456789,
    # ... other fields
}

response = requests.post("http://localhost:8000/users", json=user_data)
print(response.json())
```

## Endpoints Available

### 1. Create User
**POST** `/users`

Request body: See `sample_user.json` for example

Response (201 Created):
```json
{
  "id": 1,
  "full_name": "Alisher Karimov",
  "birthdate": "1995-03-15",
  "gender": "M",
  ...
}
```

### 2. Get User by ID
**GET** `/users/{user_id}`

Example:
```bash
curl http://localhost:8000/users/1
```

### 3. List All Users
**GET** `/users?skip=0&limit=10`

Example:
```bash
curl "http://localhost:8000/users?skip=0&limit=10"
```

## Sample User Data

The `sample_user.json` file contains a complete example with all fields:

**Required fields:**
- `full_name`: User's full name
- `birthdate`: Date of birth (must be 18+)
- `gender`: "M" or "F"
- `reg_phone`: Registration phone number (unique)

**At least one contact method required:**
- `contact_phone`: Contact phone number
- `telegram_id`: Telegram user ID

**Optional fields:**
- Personal: `marital_status`, `native_town`, `hometown`, `languages`, `height`, `weight`, `biography`
- Professional: `degree`, `field_of_study`, `occupation`
- Lifestyle: `religious_level`, `drinks`, `smokes`
- Contact: `contact_person`, `telegram_username`, `contact_comment`

## Validation Rules

The API validates:
- ✅ Age must be 18+ years
- ✅ Birthdate must be after 1940
- ✅ Height: 100-250cm (if provided)
- ✅ Weight: 30-300kg (if provided)
- ✅ Degree: 0-3 (if provided)
- ✅ Religious level: 0-3 (if provided)
- ✅ Drinks/Smokes: 'n', 's', or 'y' (if provided)
- ✅ Phone number must be unique
- ✅ Telegram ID must be unique (if provided)

## Error Responses

### User Already Exists (400)
```json
{
  "detail": "User with phone +998901234567 already exists"
}
```

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "birthdate"],
      "msg": "User must be at least 18 years old",
      "type": "value_error"
    }
  ]
}
```

### User Not Found (404)
```json
{
  "detail": "User with id 999 not found"
}
```

## Testing Multiple Users

To create multiple users, modify `sample_user.json` and change:
- `reg_phone` (must be unique)
- `telegram_id` (must be unique)
- Other personal details

Example: Create a second user
```bash
# Modify sample_user.json
# Change reg_phone to "+998901234568"
# Change telegram_id to 987654321

python test_create_user.py
```

## Troubleshooting

### Database Connection Error
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect
```
**Solution:** Check your `DATABASE_URL` in `.env` file

### Import Errors
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:** `pip install -r requirements.txt`

### Table Does Not Exist
```
sqlalchemy.exc.ProgrammingError: relation "users" does not exist
```
**Solution:** Run `python init_db.py` to create tables

### Port Already in Use
```
ERROR: [Errno 48] Address already in use
```
**Solution:** 
- Change port: `uvicorn app.main:app --reload --port 8001`
- Or kill existing process: `lsof -ti:8000 | xargs kill`

## Next Steps

1. ✅ Create user endpoint - DONE
2. Create endpoints for:
   - Metadata (bot activation, etc.)
   - Preferences (matching criteria)
   - Interests (expressing interest)
   - Matches (mutual interests)
   - Photos (profile images)
3. Implement authentication
4. Build telegram bot integration
5. Implement matching algorithm
