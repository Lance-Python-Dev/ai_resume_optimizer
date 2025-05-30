"""
Script to check if the OpenAI API key is properly configured.
This helps debug environment variable issues.
"""

import os  # For accessing environment variables
from dotenv import load_dotenv  # For loading .env files

def check_env_setup():
    """Check if the environment is properly configured for OpenAI API."""
    
    print("🔍 Checking environment setup...\n")
    
    # Step 1: Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Read and display .env file contents (without showing the actual key)
        with open('.env', 'r') as f:
            content = f.read().strip()
            if content:
                print("✅ .env file has content")
                # Check if it contains OPENAI_API_KEY
                if 'OPENAI_API_KEY' in content:
                    print("✅ OPENAI_API_KEY found in .env file")
                else:
                    print("❌ OPENAI_API_KEY not found in .env file")
                    return False
            else:
                print("❌ .env file is empty")
                return False
    else:
        print("❌ .env file not found")
        print("Please create a .env file with: OPENAI_API_KEY=your_key_here")
        return False
    
    # Step 2: Load environment variables
    print("\n🔄 Loading environment variables...")
    load_dotenv()
    
    # Step 3: Check if the key is accessible
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OPENAI_API_KEY loaded successfully")
        # Show first and last 4 characters for verification (security)
        masked_key = f"{api_key[:7]}...{api_key[-4:]}"
        print(f"🔑 Key format: {masked_key}")
        
        # Validate key format
        if api_key.startswith('sk-') and len(api_key) > 20:
            print("✅ API key format looks correct")
            return True
        else:
            print("❌ API key format seems incorrect")
            print("OpenAI keys should start with 'sk-' and be longer than 20 characters")
            return False
    else:
        print("❌ OPENAI_API_KEY not found in environment")
        return False

def test_openai_connection():
    """Test if we can connect to OpenAI with the API key."""
    try:
        # Import OpenAI library
        import openai
        print("\n🔗 Testing OpenAI connection...")
        
        # Create OpenAI client
        client = openai.OpenAI()
        
        # Make a simple API call to test the connection
        response = client.models.list()
        print("✅ Successfully connected to OpenAI API")
        print(f"📊 Available models: {len(response.data)} models found")
        return True
        
    except ImportError:
        print("❌ OpenAI library not installed")
        print("Run: pip install openai")
        return False
    except Exception as e:
        print(f"❌ Failed to connect to OpenAI: {e}")
        print("Please check your API key and internet connection")
        return False

def main():
    """Main function to run all environment checks."""
    print("🚀 OpenAI Environment Checker\n")
    
    # Check environment setup
    env_ok = check_env_setup()
    
    if env_ok:
        # Test OpenAI connection
        connection_ok = test_openai_connection()
        
        if connection_ok:
            print("\n🎉 Everything is set up correctly!")
            print("You can now run your resume optimizer.")
        else:
            print("\n⚠️  Environment is configured but connection failed.")
    else:
        print("\n❌ Environment setup incomplete.")
        print("\nTo fix this:")
        print("1. Create a .env file in this directory")
        print("2. Add this line: OPENAI_API_KEY=your_actual_key_here")
        print("3. Replace 'your_actual_key_here' with your real OpenAI API key")

if __name__ == "__main__":
    main()