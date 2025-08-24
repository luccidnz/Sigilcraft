
const fetch = require('node-fetch');

const BASE_URL = 'http://localhost:5000';

async function testAPI() {
  console.log('🧪 COMPREHENSIVE API TEST SUITE');
  console.log('================================');
  
  let allTestsPassed = true;
  
  // Test 1: Health Check
  try {
    console.log('\n1️⃣ Testing health endpoint...');
    const response = await fetch(`${BASE_URL}/api/health`);
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Health check passed:', data);
    } else {
      console.log('❌ Health check failed:', response.status);
      allTestsPassed = false;
    }
  } catch (error) {
    console.log('❌ Health check error:', error.message);
    allTestsPassed = false;
  }
  
  // Test 2: Pro Status Check
  try {
    console.log('\n2️⃣ Testing Pro status endpoint...');
    const response = await fetch(`${BASE_URL}/api/is-pro`);
    const contentType = response.headers.get('content-type');
    
    if (response.ok && contentType && contentType.includes('application/json')) {
      const data = await response.json();
      console.log('✅ Pro status check passed:', data);
    } else {
      console.log('❌ Pro status check failed:');
      console.log('   Status:', response.status);
      console.log('   Content-Type:', contentType);
      const text = await response.text();
      console.log('   Response:', text.substring(0, 200));
      allTestsPassed = false;
    }
  } catch (error) {
    console.log('❌ Pro status error:', error.message);
    allTestsPassed = false;
  }
  
  // Test 3: Pro Key Verification
  try {
    console.log('\n3️⃣ Testing Pro key verification...');
    const response = await fetch(`${BASE_URL}/api/verify-pro`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ key: 'test_key' })
    });
    
    const contentType = response.headers.get('content-type');
    
    if (response.ok && contentType && contentType.includes('application/json')) {
      const data = await response.json();
      console.log('✅ Pro key verification endpoint working:', data);
    } else {
      console.log('❌ Pro key verification failed:');
      console.log('   Status:', response.status);
      console.log('   Content-Type:', contentType);
      const text = await response.text();
      console.log('   Response:', text.substring(0, 200));
      allTestsPassed = false;
    }
  } catch (error) {
    console.log('❌ Pro key verification error:', error.message);
    allTestsPassed = false;
  }
  
  // Test 4: Test Endpoint
  try {
    console.log('\n4️⃣ Testing test endpoint...');
    const response = await fetch(`${BASE_URL}/api/test`);
    const contentType = response.headers.get('content-type');
    
    if (response.ok && contentType && contentType.includes('application/json')) {
      const data = await response.json();
      console.log('✅ Test endpoint passed:', data);
    } else {
      console.log('❌ Test endpoint failed:');
      console.log('   Status:', response.status);
      console.log('   Content-Type:', contentType);
      allTestsPassed = false;
    }
  } catch (error) {
    console.log('❌ Test endpoint error:', error.message);
    allTestsPassed = false;
  }
  
  // Test 5: Static Files
  try {
    console.log('\n5️⃣ Testing static file serving...');
    const response = await fetch(`${BASE_URL}/`);
    
    if (response.ok) {
      const text = await response.text();
      if (text.includes('Sigilcraft')) {
        console.log('✅ Static files served correctly');
      } else {
        console.log('❌ Static files not serving expected content');
        allTestsPassed = false;
      }
    } else {
      console.log('❌ Static files failed:', response.status);
      allTestsPassed = false;
    }
  } catch (error) {
    console.log('❌ Static files error:', error.message);
    allTestsPassed = false;
  }
  
  console.log('\n================================');
  if (allTestsPassed) {
    console.log('🎉 ALL TESTS PASSED! API is working correctly.');
  } else {
    console.log('❌ SOME TESTS FAILED. Please check the issues above.');
  }
  console.log('================================');
}

// Run tests with delay to allow server startup
setTimeout(testAPI, 2000);
