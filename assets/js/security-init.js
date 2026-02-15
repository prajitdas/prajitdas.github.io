(function() {
    'use strict';

    // 1. Service Worker Registration
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/sw.js', {
                scope: '/'
            }).then(function(registration) {
                // ServiceWorker registered
            }).catch(function(err) {
                // ServiceWorker registration failed
            });
        });
    }

    // 2. Google Analytics Initialization (Respects Do Not Track)
    (function() {
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
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-GT4GRDDMVN', {
            anonymize_ip: true,
            respect_dnt: true
        });
    })();

    // 3. Core Web Vitals Monitoring
    function sendWebVitals() {
        if ('PerformanceObserver' in window) {
            // Largest Contentful Paint (LCP)
            new PerformanceObserver((entryList) => {
                const entries = entryList.getEntries();
                const lastEntry = entries[entries.length - 1];
                if (window.gtag) {
                    gtag('event', 'web_vitals', {
                        name: 'LCP',
                        value: Math.round(lastEntry.startTime),
                        custom_parameter_1: 'performance'
                    });
                }
            }).observe({entryTypes: ['largest-contentful-paint']});

            // First Input Delay (FID)
            new PerformanceObserver((entryList) => {
                const firstInput = entryList.getEntries()[0];
                if (window.gtag) {
                    gtag('event', 'web_vitals', {
                        name: 'FID',
                        value: Math.round(firstInput.processingStart - firstInput.startTime),
                        custom_parameter_1: 'performance'
                    });
                }
            }).observe({entryTypes: ['first-input']});

            // Cumulative Layout Shift (CLS)
            let clsValue = 0;
            new PerformanceObserver((entryList) => {
                for (const entry of entryList.getEntries()) {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                    }
                }
                if (window.gtag) {
                    gtag('event', 'web_vitals', {
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

    // 4. jQuery Availability Check
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

    // 5. Performance Optimizations (Prefetch & Page Load Time)
    if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
            ['assets/docs/resume/resume-prajit-das-032225.pdf', 'assets/docs/cv/cv-prajit-kumar-das.pdf', 'assets/img/projects/MobipediaLogo.png'].forEach(href => {
                const link = document.createElement('link');
                link.rel = 'prefetch';
                link.href = href;
                document.head.appendChild(link);
            });
        });
    }
    window.addEventListener('load', () => {
        if (window.gtag && performance.timing) {
            const t = performance.timing.loadEventEnd - performance.timing.navigationStart;
            if (t > 0) gtag('event', 'page_load_time', {event_category: 'Performance', value: Math.round(t)});
        }
    });

    // 6. Load Google Fonts (replaces inline onload handler to avoid CSP 'unsafe-inline')
    (function() {
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;1,300;1,400&family=Montserrat:wght@400;700&family=Open+Sans&display=optional';
        document.head.appendChild(link);
    })();

})();
