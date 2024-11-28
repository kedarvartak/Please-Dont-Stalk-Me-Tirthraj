// Environment-based API URL
export const API_URL = {
    development: 'http://localhost:8000',
    production: 'https://your-production-api.com'  // deployment sathi
};

// Get current environment
const environment = import.meta.env.MODE || 'development';

// Export the base URL
export const BASE_URL = API_URL[environment]; 