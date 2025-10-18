#!/usr/bin/env python3
"""
Test script to verify Tree Whisperer setup
"""

import sys
import os
import importlib.util

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing Python imports...")
    
    required_modules = [
        'flask',
        'openai', 
        'mysql.connector',
        'redis',
        'sqlparse',
        'dotenv'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            if module == 'mysql.connector':
                import mysql.connector
            elif module == 'dotenv':
                from dotenv import load_dotenv
            else:
                __import__(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All required modules imported successfully")
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import Config
        print(f"  ✅ Config loaded")
        print(f"  - DB Host: {Config.DB_HOST}")
        print(f"  - DB Name: {Config.DB_NAME}")
        print(f"  - OpenAI Model: {Config.OPENAI_MODEL}")
        print(f"  - Rate Limit: {Config.RATE_LIMIT_PER_MINUTE}/min")
        return True
    except Exception as e:
        print(f"  ❌ Config error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🗄️ Testing database connection...")
    
    try:
        from database_connection import DatabaseConnection
        
        with DatabaseConnection() as db:
            if db.test_connection():
                print("  ✅ Database connection successful")
                
                # Test a simple query
                result = db.execute_query("SELECT COUNT(*) as count FROM tree_species")
                if result:
                    print(f"  ✅ Query test successful: {result[0]['count']} tree species found")
                else:
                    print("  ⚠️ No data found in database")
                
                return True
            else:
                print("  ❌ Database connection failed")
                return False
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        print("  💡 Make sure MySQL is running and database is set up")
        return False

def test_ai_generator():
    """Test AI SQL generator"""
    print("\n🤖 Testing AI SQL generator...")
    
    try:
        from ai_sql_generator import AISQLGenerator
        
        generator = AISQLGenerator()
        
        # Test domain validation
        tree_question = "What is the tallest tree species?"
        non_tree_question = "What is the weather today?"
        
        if generator.is_tree_forest_related(tree_question):
            print("  ✅ Tree question validation works")
        else:
            print("  ❌ Tree question validation failed")
            return False
            
        if not generator.is_tree_forest_related(non_tree_question):
            print("  ✅ Non-tree question rejection works")
        else:
            print("  ❌ Non-tree question rejection failed")
            return False
        
        # Test SQL validation
        valid_sql = "SELECT * FROM tree_species"
        invalid_sql = "DROP TABLE tree_species"
        
        is_valid, message = generator.validate_sql(valid_sql)
        if is_valid:
            print("  ✅ Valid SQL validation works")
        else:
            print(f"  ❌ Valid SQL validation failed: {message}")
            return False
            
        is_valid, message = generator.validate_sql(invalid_sql)
        if not is_valid:
            print("  ✅ Invalid SQL rejection works")
        else:
            print("  ❌ Invalid SQL rejection failed")
            return False
        
        print("  ✅ AI SQL generator tests passed")
        return True
        
    except Exception as e:
        print(f"  ❌ AI generator error: {e}")
        return False

def test_rate_limiter():
    """Test rate limiter"""
    print("\n⏱️ Testing rate limiter...")
    
    try:
        from rate_limiter import RateLimiter
        
        limiter = RateLimiter()
        
        # Test rate limit check
        is_allowed, message = limiter.check_rate_limit("test_user")
        if is_allowed:
            print("  ✅ Rate limiter allows first request")
        else:
            print(f"  ❌ Rate limiter blocked first request: {message}")
            return False
        
        # Test usage stats
        stats = limiter.get_usage_stats()
        if 'daily_usage' in stats:
            print("  ✅ Usage stats retrieval works")
        else:
            print("  ❌ Usage stats retrieval failed")
            return False
        
        print("  ✅ Rate limiter tests passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Rate limiter error: {e}")
        return False

def main():
    """Run all tests"""
    print("🌲 Tree Whisperer Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config,
        test_database_connection,
        test_ai_generator,
        test_rate_limiter
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Tree Whisperer is ready to use.")
        print("\nNext steps:")
        print("1. Set your OPENAI_API_KEY in .env file")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
