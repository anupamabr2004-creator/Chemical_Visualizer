#!/bin/bash
# Quick API Test Script - Run from terminal to verify backend connectivity

echo "Testing Chemical Equipment API Endpoints"
echo "=========================================="
echo ""

# Test 1: CORS Preflight
echo "Test 1: CORS Preflight Request"
curl -i -X OPTIONS http://127.0.0.1:8000/api/auth/login/ \
  -H "Origin: http://localhost:3001" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type"
echo ""
echo ""

# Test 2: Registration
echo "Test 2: User Registration"
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "apitest_'$(date +%s)'",
    "password": "TestPass123"
  }'
echo ""
echo ""

# Test 3: Login
echo "Test 3: User Login (requires valid registration first)"
echo "Note: Replace USERNAME and PASSWORD with registered credentials"
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass"
  }'
echo ""
echo ""

echo "Tests Complete!"
echo "Check responses above for:"
echo "  - CORS headers present (Access-Control-Allow-Origin)"
echo "  - Successful registration returns {message: ...}"
echo "  - Successful login returns {access: ..., refresh: ...}"
