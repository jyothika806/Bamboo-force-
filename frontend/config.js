/**
 * Bamboo Force AI — shared frontend configuration.
 * Single source of truth for API base URL.
 * 
 * For production deployment, update baseUrl to your production domain.
 * For local development, use http://127.0.0.1:8000 or http://localhost:8000
 */
window.APP_CONFIG = {
    baseUrl: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? "http://127.0.0.1:8000" 
        : `${window.location.protocol}//${window.location.hostname}:8000`,
    requestTimeoutMs: 30000,
};
