#!/usr/bin/env python3
"""
Test script to verify hospital chatbot integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test that required environment variables are set"""
    print("🔍 Testing environment configuration...")
    
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with your API keys")
        return False
    
    print("✅ Environment variables configured")
    return True

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from src.graph import app
        print("✅ Chatbot graph imported successfully")
    except ImportError as e:
        print(f"❌ Chatbot graph import failed: {e}")
        return False
    
    try:
        from src.utils.ui_components import apply_custom_css
        print("✅ UI components imported successfully")
    except ImportError as e:
        print(f"❌ UI components import failed: {e}")
        return False
    
    return True

def test_chatbot():
    """Test the chatbot functionality"""
    print("🔍 Testing chatbot functionality...")
    
    try:
        from src.graph import app
        
        # Test with a simple question
        test_question = "What are your visiting hours?"
        print(f"Testing question: '{test_question}'")
        
        result = app.invoke(input={"question": test_question})
        response = result.get("generation", "")
        
        if response and len(response) > 0:
            print("✅ Chatbot responded successfully")
            print(f"Response preview: {response[:100]}...")
            return True
        else:
            print("❌ Chatbot returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Chatbot test failed: {e}")
        return False

def test_streamlit_components():
    """Test Streamlit components"""
    print("🔍 Testing Streamlit components...")
    
    try:
        # Test importing Streamlit components
        import streamlit as st
        
        # Test that we can use basic Streamlit functions
        # (This won't actually render, just check imports work)
        print("✅ Streamlit components accessible")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit component test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🏥 Hospital Chatbot Integration Test")
    print("=" * 40)
    
    tests = [
        test_environment,
        test_imports,
        test_chatbot,
        test_streamlit_components
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            print()
    
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The chatbot is ready for deployment.")
        print("\n🚀 To run the Streamlit app:")
        print("   streamlit run streamlit_app.py")
        print("\n🐳 To deploy with Docker:")
        print("   docker-compose up --build")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 