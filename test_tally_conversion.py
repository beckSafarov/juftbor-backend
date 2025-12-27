"""
Test script to validate Tally to User conversion.
Tests the converter with the sample_tally_response.json file.
"""
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.tally_converter import convert_tally_to_user
from app.schemas.user import UserCreate

def test_conversion():
    """Test converting sample Tally response to User format"""
    
    # Load sample Tally response
    with open("sample_tally_response.json", "r", encoding="utf-8") as f:
        tally_data = json.load(f)
    
    print("=" * 80)
    print("TALLY TO USER CONVERSION TEST")
    print("=" * 80)
    
    # Convert Tally data
    print("\n📥 Converting Tally response to User format...")
    user_data = convert_tally_to_user(tally_data)
    
    print("\n✅ Converted User Data:")
    print("-" * 80)
    for key, value in sorted(user_data.items()):
        print(f"  {key:20s}: {value}")
    
    # Validate with Pydantic schema
    print("\n🔍 Validating with UserCreate schema...")
    try:
        user_create = UserCreate(**user_data)
        print("✅ Validation successful!")
        
        print("\n📋 UserCreate Object:")
        print("-" * 80)
        print(user_create.model_dump_json(indent=2))
        
        return True
    except Exception as e:
        print(f"❌ Validation failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_conversion()
    sys.exit(0 if success else 1)
