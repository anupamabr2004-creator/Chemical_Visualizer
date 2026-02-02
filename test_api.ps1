# PowerShell API Test Script - Run from terminal to verify backend connectivity

Write-Host "Testing Chemical Equipment API Endpoints" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: CORS Preflight
Write-Host "Test 1: CORS Preflight Request" -ForegroundColor Yellow
Write-Host "Checking if backend accepts requests from localhost:3001..." -ForegroundColor Gray

$corsTest = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/login/" `
  -Method Options `
  -Headers @{
    "Origin" = "http://localhost:3001"
    "Access-Control-Request-Method" = "POST"
    "Access-Control-Request-Headers" = "Content-Type"
  } `
  -ErrorAction SilentlyContinue

if ($corsTest) {
    Write-Host "CORS Headers:" -ForegroundColor Green
    if ($corsTest.Headers["Access-Control-Allow-Origin"]) {
        Write-Host "  ✓ Access-Control-Allow-Origin: $($corsTest.Headers['Access-Control-Allow-Origin'])" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Access-Control-Allow-Origin header missing!" -ForegroundColor Red
    }
}
Write-Host ""

# Test 2: Registration
Write-Host "Test 2: User Registration" -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$testUsername = "apitest_$timestamp"

$regResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/register/" `
  -Method Post `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body (@{
    username = $testUsername
    password = "TestPass123"
  } | ConvertTo-Json) `
  -ErrorAction SilentlyContinue

if ($regResponse) {
    $regData = $regResponse.Content | ConvertFrom-Json
    Write-Host "Registration Response:" -ForegroundColor Green
    Write-Host ($regData | ConvertTo-Json | Out-String) -ForegroundColor Green
    Write-Host "  Created test user: $testUsername" -ForegroundColor Cyan
} else {
    Write-Host "Registration failed" -ForegroundColor Red
}
Write-Host ""

# Test 3: Login with newly created user
Write-Host "Test 3: User Login" -ForegroundColor Yellow
Write-Host "Logging in with: $testUsername" -ForegroundColor Gray

$loginResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/login/" `
  -Method Post `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body (@{
    username = $testUsername
    password = "TestPass123"
  } | ConvertTo-Json) `
  -ErrorAction SilentlyContinue

if ($loginResponse) {
    $loginData = $loginResponse.Content | ConvertFrom-Json
    Write-Host "Login Response:" -ForegroundColor Green
    if ($loginData.access) {
        Write-Host "  ✓ Access token received" -ForegroundColor Green
        Write-Host "  Token (first 50 chars): $($loginData.access.Substring(0, [Math]::Min(50, $loginData.access.Length)))..." -ForegroundColor Cyan
    }
    if ($loginData.error) {
        Write-Host "  ✗ Error: $($loginData.error)" -ForegroundColor Red
    }
} else {
    Write-Host "Login failed" -ForegroundColor Red
}
Write-Host ""

# Test 4: Get datasets (requires valid token)
if ($loginData -and $loginData.access) {
    Write-Host "Test 4: Fetch Datasets (Authenticated)" -ForegroundColor Yellow
    Write-Host "Using access token from login above..." -ForegroundColor Gray
    
    $datasetsResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/equipment/datasets/" `
      -Method Get `
      -Headers @{ 
        "Authorization" = "Bearer $($loginData.access)"
        "Content-Type" = "application/json"
      } `
      -ErrorAction SilentlyContinue
    
    if ($datasetsResponse) {
        $datasetsData = $datasetsResponse.Content | ConvertFrom-Json
        Write-Host "Datasets Response:" -ForegroundColor Green
        Write-Host "  Count: $($datasetsData.Count)" -ForegroundColor Cyan
        if ($datasetsData.Count -gt 0) {
            Write-Host "  Latest dataset: $($datasetsData[0].name)" -ForegroundColor Cyan
        } else {
            Write-Host "  No datasets yet (this is normal for new user)" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "Tests Complete!" -ForegroundColor Cyan
Write-Host "If all tests passed, your frontend-backend integration is working! ✓" -ForegroundColor Green
