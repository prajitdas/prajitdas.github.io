// Service Worker for Advanced Caching Strategy
// Version: 2025.10.1

const CACHE_NAME = 'prajitdas-cache-v2025.11.1';
const STATIC_CACHE_NAME = 'prajitdas-static-v2025.11.1';
const DYNAMIC_CACHE_NAME = 'prajitdas-dynamic-v2025.11.1';

// Critical resources for immediate caching (LCP optimization)
const CRITICAL_ASSETS = [
  '/',
  '/index.html',
  '/assets/img/Profile.jpg?v=2025.11'
];

// Resources to cache immediately
const STATIC_ASSETS = [
  ...CRITICAL_ASSETS,
  '/assets/css/bootstrap.min.css?v=2025.11',
  '/assets/css/font-awesome.min.css?v=2025.11',
  '/assets/css/styles.css?v=2025.11',
  '/assets/plugins/vegas/jquery.vegas.min.css?v=2025.11',
  '/assets/js/jquery-3.7.1.min.js?v=2025.11',
  '/assets/plugins/vegas/jquery.vegas.min.js?v=2025.11',
  '/assets/js/bootstrap.min.js?v=2025.11',
  '/assets/js/main.js?v=2025.11',
  '/assets/plugins/vegas/images/loading.gif',
  '/assets/plugins/vegas/overlays/01.png',
  '/assets/plugins/vegas/overlays/15.png',
  '/assets/img/1.jpg',
  '/assets/img/2.jpg',
  '/assets/img/3.jpg',
  '/assets/img/sw.jpg',
  '/assets/img/favicon.ico',
  '/assets/docs/publications/wordcloud.png?v=2025.11',
  '/assets/img/projects/MobipediaLogo.png'
];

// Cache strategies for different resource types
const CACHE_STRATEGIES = {
  // Long-term cache for static assets (1 year)
  static: {
    maxAge: 31536000, // 1 year
    patterns: [/\.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$/]
  },
  // Medium-term cache for HTML (1 day with stale-while-revalidate)
  html: {
    maxAge: 86400, // 1 day
    staleWhileRevalidate: 31536000, // 1 year
    patterns: [/\.html$/, /\/$/]
  },
  // Short-term cache for API responses (1 hour)
  api: {
    maxAge: 3600, // 1 hour
    patterns: [/\/api\//, /\.json$/]
  }
};

// Install event - cache static assets
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Caching static assets...');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('Service Worker: Static assets cached');
        return self.skipWaiting();
      })
      .catch(err => {
        console.error('Service Worker: Failed to cache static assets', err);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(cacheName => {
            // Delete old versions of our caches
            return cacheName.startsWith('prajitdas-') && 
                   cacheName !== STATIC_CACHE_NAME && 
                   cacheName !== DYNAMIC_CACHE_NAME;
          })
          .map(cacheName => {
            console.log('Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          })
      );
    })
    .then(() => {
      console.log('Service Worker: Activated');
      return self.clients.claim();
    })
  );
});

// Fetch event - implement caching strategies
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }
  
  // Skip external requests (different origin)
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }
  
  const url = new URL(event.request.url);
  const pathname = url.pathname;
  
  // Determine cache strategy
  let strategy = 'static';
  if (CACHE_STRATEGIES.html.patterns.some(pattern => pattern.test(pathname))) {
    strategy = 'html';
  } else if (CACHE_STRATEGIES.api.patterns.some(pattern => pattern.test(pathname))) {
    strategy = 'api';
  }
  
  event.respondWith(handleRequest(event.request, strategy));
});

// Handle requests based on caching strategy
async function handleRequest(request, strategy) {
  const url = new URL(request.url);
  const cacheKey = request.url;
  
  try {
    switch (strategy) {
      case 'static':
        return await cacheFirst(request, STATIC_CACHE_NAME);
      
      case 'html':
        return await staleWhileRevalidate(request, DYNAMIC_CACHE_NAME);
      
      case 'api':
        return await networkFirst(request, DYNAMIC_CACHE_NAME);
      
      default:
        return await cacheFirst(request, STATIC_CACHE_NAME);
    }
  } catch (error) {
    console.error('Service Worker: Request failed', error);
    return new Response('Service Worker: Request failed', {
      status: 503,
      statusText: 'Service Unavailable'
    });
  }
}

// Cache-first strategy (for static assets)
async function cacheFirst(request, cacheName) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    // Add cache headers for client-side caching
    const response = cachedResponse.clone();
    response.headers.set('Cache-Control', 'public, max-age=31536000, immutable');
    return response;
  }
  
  // Not in cache, fetch from network
  const networkResponse = await fetch(request);
  
  if (networkResponse.ok) {
    const cache = await caches.open(cacheName);
    cache.put(request, networkResponse.clone());
  }
  
  return networkResponse;
}

// Stale-while-revalidate strategy (for HTML)
async function staleWhileRevalidate(request, cacheName) {
  const cachedResponse = await caches.match(request);
  const networkResponse = fetch(request).then(response => {
    if (response.ok) {
      const cache = caches.open(cacheName);
      cache.then(c => c.put(request, response.clone()));
    }
    return response;
  });
  
  // Return cached version immediately if available
  if (cachedResponse) {
    // Update cache in background
    networkResponse.catch(() => {}); // Ignore network errors
    return cachedResponse;
  }
  
  // Wait for network if no cached version
  return networkResponse;
}

// Network-first strategy (for API calls)
async function networkFirst(request, cacheName) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    // Network failed, try cache
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    throw error;
  }
}

// Background sync for offline functionality
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  // Implement background sync logic here
  console.log('Service Worker: Background sync triggered');
}