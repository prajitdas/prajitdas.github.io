/*jslint browser: true, node: true */
/*global jQuery, console, performance, navigator, window, document, PerformanceObserver */

// 1. Service Worker Registration
(function() {
    'use strict';
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/sw.js', {
                scope: '/'
            }).then(function(registration) {
                // ServiceWorker registered
            }).catch(function(err) {
                console.error('SW registration failed: ', err);
            });
        });
    }
})();

// 2. Web Vitals
(function() {
    'use strict';
    // Monitor Core Web Vitals
    function sendWebVitals() {
        if ('PerformanceObserver' in window) {
            // Largest Contentful Paint (LCP)
            new PerformanceObserver(function(entryList) {
                var entries = entryList.getEntries();
                var lastEntry = entries[entries.length - 1];
                if (window.gtag) {
                    window.gtag('event', 'web_vitals', {
                        name: 'LCP',
                        value: Math.round(lastEntry.startTime),
                        custom_parameter_1: 'performance'
                    });
                }
            }).observe({entryTypes: ['largest-contentful-paint']});

            // First Input Delay (FID)
            new PerformanceObserver(function(entryList) {
                var firstInput = entryList.getEntries()[0];
                if (window.gtag) {
                    window.gtag('event', 'web_vitals', {
                        name: 'FID',
                        value: Math.round(firstInput.processingStart - firstInput.startTime),
                        custom_parameter_1: 'performance'
                    });
                }
            }).observe({entryTypes: ['first-input']});

            // Cumulative Layout Shift (CLS) - basic monitoring
            var clsValue = 0;
            new PerformanceObserver(function(entryList) {
                var entries = entryList.getEntries();
                var i;
                for (i = 0; i < entries.length; i += 1) {
                    if (!entries[i].hadRecentInput) {
                        clsValue += entries[i].value;
                    }
                }
                if (window.gtag) {
                    window.gtag('event', 'web_vitals', {
                        name: 'CLS',
                        value: Math.round(clsValue * 1000),
                        custom_parameter_1: 'performance'
                    });
                }
            }).observe({entryTypes: ['layout-shift']});
        }
    }

    // Load Web Vitals monitoring after page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', sendWebVitals);
    } else {
        sendWebVitals();
    }
})();

// 3. Google Analytics
(function() {
    'use strict';
    // Check if analytics should be loaded (respects ad blockers)
    if (navigator.doNotTrack === '1' || window.doNotTrack === '1') {
        return; // Respect Do Not Track
    }

    // Load gtag with error handling
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-GT4GRDDMVN';
    script.onerror = function() {
        // Silently handle ad blocker or network errors
        console.log('Analytics blocked or unavailable');
    };
    document.head.appendChild(script);

    // Initialize gtag
    window.dataLayer = window.dataLayer || [];
    function gtag(){window.dataLayer.push(arguments);}
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', 'G-GT4GRDDMVN', {
        anonymize_ip: true,
        respect_dnt: true
    });
})();

// 4. Idle Resource Prefetching & Analytics Performance Event
(function() {
    'use strict';
    if ('requestIdleCallback' in window) {
        window.requestIdleCallback(function() {
            ['assets/docs/resume/resume-prajit-das-032225.pdf', 'assets/docs/cv/cv-prajit-kumar-das.pdf', 'assets/img/projects/MobipediaLogo.png'].forEach(function(href) {
                var link = document.createElement('link');
                link.rel = 'prefetch';
                link.href = href;
                document.head.appendChild(link);
            });
        });
    }
    window.addEventListener('load', function() {
        if (window.gtag && performance.timing) {
            var t = performance.timing.loadEventEnd - performance.timing.navigationStart;
            if (t > 0) {
                window.gtag('event', 'page_load_time', {event_category: 'Performance', value: Math.round(t)});
            }
        }
    });
})();

// 5. jQuery Check
(function() {
    'use strict';
    document.addEventListener('DOMContentLoaded', function() {
        // Triple-check jQuery is available and functional
        if (!window.jQuery || typeof window.jQuery !== 'function') {
            console.error('jQuery still not available or not functional in DOMContentLoaded');
            return;
        }

        // Ensure jQuery.fn exists
        if (!window.jQuery.fn) {
            console.error('jQuery.fn not available');
            return;
        }
    });
})();

// 6. Font Loading
(function() {
    'use strict';
    // Load fonts asynchronously to avoid render blocking (replacing inline onload handler)
    var link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;1,300;1,400&family=Montserrat:wght@400;700&family=Open+Sans&display=optional';
    link.rel = 'stylesheet';
    link.media = 'all';
    document.head.appendChild(link);
})();
