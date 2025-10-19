/**
 * Custom Service Worker Configuration for ADK Training Hub PWA
 * 
 * This file handles:
 * - Offline page injection when navigation fails
 * - External resource caching (fonts, images, etc.)
 * - Google Analytics API caching for offline resilience
 * - GitHub API caching for stats
 * - Improved offline UX
 */

import { registerRoute, NavigationRoute } from 'workbox-routing';
import { CacheFirst, StaleWhileRevalidate, NetworkFirst } from 'workbox-strategies';
import { CacheExpiration } from 'workbox-expiration';
import { Queue } from 'workbox-background-sync';

/**
 * Main export function that receives debugging and offline mode parameters
 */
export default function swCustom({ debug, offlineMode }) {
  if (debug) {
    console.log('🔧 [Custom SW] Initializing custom service worker configuration');
    console.log('🔧 [Custom SW] Offline mode:', offlineMode);
  }

  // ============================================================
  // 1. OFFLINE PAGE FALLBACK FOR NAVIGATION
  // ============================================================
  
  // Create a handler for navigation requests that fail
  const offlineFallback = async (event) => {
    try {
      // Try to fetch the requested page
      const response = await fetch(event.request);
      return response;
    } catch (error) {
      if (debug) {
        console.log('🔧 [Custom SW] Navigation failed, showing offline page:', event.request.url);
      }
      
      // Return the offline page for any failed navigation
      const offlineResponse = await caches.match('/adk_training/offline.html');
      return offlineResponse || new Response('Offline', { status: 503 });
    }
  };

  // Register navigation route for offline fallback
  const navigationRoute = new NavigationRoute(offlineFallback, {
    // Matches HTML navigation requests
    allowlist: [/^(?!.*\.(js|css|png|jpg|jpeg|svg|gif|webp|woff|woff2|ttf|eot)$)/],
    denylist: [
      /^\/api\//,
      /^\/admin\//,
    ],
  });

  registerRoute(navigationRoute);

  if (debug) {
    console.log('✅ [Custom SW] Registered navigation offline fallback');
  }

  // ============================================================
  // 2. EXTERNAL RESOURCES CACHING STRATEGY
  // ============================================================

  // Google Fonts - Cache first, very long TTL
  registerRoute(
    ({ url }) => url.origin === 'https://fonts.googleapis.com',
    new CacheFirst({
      cacheName: 'google-fonts-stylesheets',
      plugins: [
        new CacheExpiration({
          maxEntries: 30,
          maxAgeSeconds: 365 * 24 * 60 * 60, // 1 year
        }),
      ],
    })
  );

  // Google Fonts CDN - Cache first, very long TTL
  registerRoute(
    ({ url }) => url.origin === 'https://fonts.gstatic.com',
    new CacheFirst({
      cacheName: 'google-fonts-webfonts',
      plugins: [
        new CacheExpiration({
          maxEntries: 30,
          maxAgeSeconds: 365 * 24 * 60 * 60, // 1 year
        }),
      ],
    })
  );

  // Images - Cache first with expiration
  registerRoute(
    ({ request }) => request.destination === 'image',
    new CacheFirst({
      cacheName: 'images-cache',
      plugins: [
        new CacheExpiration({
          maxEntries: 100,
          maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
        }),
      ],
    })
  );

  // Stylesheets and scripts - Stale while revalidate
  registerRoute(
    ({ request }) => 
      request.destination === 'style' || 
      request.destination === 'script',
    new StaleWhileRevalidate({
      cacheName: 'static-resources',
      plugins: [
        new CacheExpiration({
          maxEntries: 60,
          maxAgeSeconds: 24 * 60 * 60, // 1 day
        }),
      ],
    })
  );

  // Documents - Network first with cache fallback
  registerRoute(
    ({ request }) => request.destination === 'document',
    new NetworkFirst({
      cacheName: 'documents-cache',
      networkTimeoutSeconds: 5,
      plugins: [
        new CacheExpiration({
          maxEntries: 50,
          maxAgeSeconds: 7 * 24 * 60 * 60, // 7 days
        }),
      ],
    })
  );

  if (debug) {
    console.log('✅ [Custom SW] Registered external resource caching strategies');
  }

  // ============================================================
  // 3. EXTERNAL API CACHING (GitHub, Google Analytics, etc.)
  // ============================================================

  // GitHub API - Stale while revalidate with longer cache
  registerRoute(
    ({ url }) => url.origin === 'https://api.github.com',
    new StaleWhileRevalidate({
      cacheName: 'github-api-cache',
      plugins: [
        new CacheExpiration({
          maxEntries: 20,
          maxAgeSeconds: 24 * 60 * 60, // 1 day
        }),
      ],
    })
  );

  // Google Analytics - Network first, don't fail on connection issues
  registerRoute(
    ({ url }) => 
      url.origin === 'https://www.google-analytics.com' ||
      url.origin === 'https://www.googletagmanager.com',
    new NetworkFirst({
      cacheName: 'google-analytics-cache',
      networkTimeoutSeconds: 2,
      plugins: [
        new CacheExpiration({
          maxEntries: 10,
          maxAgeSeconds: 60 * 60 * 24, // 1 day
        }),
      ],
    })
  );

  if (debug) {
    console.log('✅ [Custom SW] Registered external API caching strategies');
  }

  // ============================================================
  // 4. OFFLINE DETECTION & NOTIFICATIONS
  // ============================================================

  // Listen for fetch events to detect offline status
  self.addEventListener('fetch', (event) => {
    // Only log for debugging
    if (debug && event.request.method === 'GET') {
      event.waitUntil(
        fetch(event.request)
          .then(() => {
            // Online
            self.clients.matchAll().then((clients) => {
              clients.forEach((client) => {
                client.postMessage({
                  type: 'ONLINE_STATUS',
                  isOnline: true,
                });
              });
            });
          })
          .catch(() => {
            // Offline
            self.clients.matchAll().then((clients) => {
              clients.forEach((client) => {
                client.postMessage({
                  type: 'ONLINE_STATUS',
                  isOnline: false,
                });
              });
            });
          })
      );
    }
  });

  // ============================================================
  // 5. BACKGROUND SYNC FOR OFFLINE ACTIONS
  // ============================================================

  // Create a queue for offline actions that should be synced later
  const actionQueue = new Queue('adk-training-action-queue', {
    maxRetentionTime: 24 * 60, // Retry for up to 24 hours
  });

  // Listen for messages from the client to queue actions
  self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'QUEUE_ACTION') {
      if (debug) {
        console.log('🔧 [Custom SW] Queueing action:', event.data.action);
      }
      
      // Queue the action for later sync
      actionQueue.pushRequest({
        request: new Request('/adk_training/api/sync', {
          method: 'POST',
          body: JSON.stringify(event.data.action),
          headers: {
            'Content-Type': 'application/json',
          },
        }),
      });
    }
  });

  if (debug) {
    console.log('✅ [Custom SW] Registered background sync listeners');
  }

  // ============================================================
  // 6. PERIODIC BACKGROUND SYNC (if supported)
  // ============================================================

  if ('periodicSync' in self.registration) {
    self.addEventListener('periodicsync', (event) => {
      if (event.tag === 'adk-training-sync') {
        if (debug) {
          console.log('🔧 [Custom SW] Periodic sync triggered');
        }
        
        event.waitUntil(
          // Perform periodic updates here (e.g., sync content, check for updates)
          fetch('/adk_training/api/check-updates')
            .then((response) => {
              if (debug && response.ok) {
                console.log('✅ [Custom SW] Periodic sync completed successfully');
              }
            })
            .catch((error) => {
              if (debug) {
                console.log('⚠️ [Custom SW] Periodic sync failed:', error.message);
              }
            })
        );
      }
    });

    if (debug) {
      console.log('✅ [Custom SW] Registered periodic background sync');
    }
  }

  if (debug) {
    console.log('✅ [Custom SW] Custom service worker configuration complete');
  }
}
