import axios from 'axios';

export const checkServiceHealth = async () => {
  const services = {
    auth: 'http://localhost:8001',
    user: 'http://localhost:8002'
  };

  const results = {
    auth: false,
    user: false,
    message: ''
  };

  try {
    await axios.get(`${services.auth}/api/v1/system/health-check`);
    results.auth = true;
    console.log('Auth service is running');
  } catch (error) {
    console.error('Auth service error:', error);
    results.message = 'Authentication Service is not running. Please start the service.';
    return results;
  }

  try {
    await axios.get(`${services.user}/api/v1/system/health-check`);
     results.user = true;
    console.log('User service is running');
  } catch (error) {
    console.error('User service error:', error);
    results.message = 'User Service is not running. Please start the service.';
    return results;
  }

  return results;
};