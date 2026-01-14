// Security Enhancements & Optimization Scripts
// Moved from inline to external file to improve Content Security Policy (CSP) posture
// This helps reduce XSS attack surface by minimizing inline scripts.

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

    // Cache API implementation for manual resource caching
    if ('caches' in window) {
        const CACHE_NAME = 'prajitdas-v2025.11';
        const urlsToCache = [
            '/',
            '/assets/css/bootstrap.min.css?v=2025.11',
            '/assets/css/font-awesome.min.css?v=2025.11',
            '/assets/css/styles.css?v=2025.11',
            '/assets/plugins/vegas/jquery.vegas.min.css?v=2025.11',
            '/assets/js/jquery-3.7.1.min.js?v=2025.11',
            '/assets/js/jquery-migrate-3.5.2.min.js?v=2025.11',
            '/assets/plugins/vegas/jquery.vegas.min.js?v=2025.11',
            '/assets/js/bootstrap.min.js?v=2025.11',
            '/assets/js/main.js?v=2025.11'
        ];

        // Pre-cache critical resources
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(urlsToCache);
        }).catch(function(e) {
            // console.error('Cache addAll failed', e);
        });
    }

    // 2. Web Vitals
    function sendWebVitals() {
        if ('PerformanceObserver' in window) {
            // Largest Contentful Paint (LCP)
            try {
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
            } catch (e) {}

            // First Input Delay (FID)
            try {
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
            } catch (e) {}

            // Cumulative Layout Shift (CLS)
            try {
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
            } catch (e) {}
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', sendWebVitals);
    } else {
        sendWebVitals();
    }

    // 3. Google Analytics
    if (navigator.doNotTrack !== '1' && window.doNotTrack !== '1') {
        var script = document.createElement('script');
        script.async = true;
        script.src = 'https://www.googletagmanager.com/gtag/js?id=G-GT4GRDDMVN';
        script.onerror = function() { console.log('Analytics blocked or unavailable'); };
        document.head.appendChild(script);

        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        window.gtag = gtag; // Make global
        gtag('js', new Date());
        gtag('config', 'G-GT4GRDDMVN', {
            anonymize_ip: true,
            respect_dnt: true
        });
    }

    // 4. Years of Experience
    (function() {
        const today = new Date();
        const pastDate = new Date(2025, 3, 12); // April 12, 2025
        const timeDifference = today.getTime() - pastDate.getTime();
        const years = (4012+2465)/365.25 + Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 365.25));

        const yearsElement = document.getElementById('years-experience');
        if (yearsElement) {
            yearsElement.textContent = Math.floor(years) + ' years';
        }
    })();

    // 5. Performance Optimizations (Gravatar & Prefetch)
    (function() {
        // Gravatar
        const gravatarImg = new Image();
        gravatarImg.onload = function() {
            const profileImg = document.getElementById('donottouch');
            if (profileImg) {
                profileImg.src = 'https://www.gravatar.com/avatar/e5cfbe92fef3aa2d6e21a720bf22c2a7?s=200';
                profileImg.srcset = 'https://www.gravatar.com/avatar/e5cfbe92fef3aa2d6e21a720bf22c2a7?s=200 1x, https://www.gravatar.com/avatar/e5cfbe92fef3aa2d6e21a720bf22c2a7?s=400 2x';
            }
        };
        gravatarImg.src = 'https://www.gravatar.com/avatar/e5cfbe92fef3aa2d6e21a720bf22c2a7?s=200';

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
                if (t > 0) window.gtag('event', 'page_load_time', {event_category: 'Performance', value: Math.round(t)});
            }
        });
    })();

    // 6. Mobile Menu & Vegas
    document.addEventListener('DOMContentLoaded', function() {
         // Mobile hamburger menu fallback
        function initMobileMenu() {
            function setupMenu() {
                var toggleButton = document.querySelector('.navbar-toggle');
                var navbarCollapse = document.querySelector('.navbar-collapse');

                if (toggleButton && navbarCollapse) {
                    // Clone to remove old listeners
                    var newButton = toggleButton.cloneNode(true);
                    toggleButton.parentNode.replaceChild(newButton, toggleButton);

                    var toggleFunc = function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        if (navbarCollapse.classList.contains('in')) {
                            navbarCollapse.classList.remove('in');
                             // Force display toggle for some bootstrap versions behavior
                             navbarCollapse.style.display = 'none';
                        } else {
                            navbarCollapse.classList.add('in');
                            navbarCollapse.style.display = 'block';
                        }
                    };

                    newButton.addEventListener('click', toggleFunc);
                    newButton.addEventListener('touchend', toggleFunc);

                    // Add pointer events for any touch device
                    newButton.style.cursor = 'pointer';
                    newButton.style.webkitTapHighlightColor = 'rgba(0,0,0,0.1)';
                    newButton.style.userSelect = 'none';
                }
            }

            setupMenu();
            setTimeout(setupMenu, 1000);
            setTimeout(setupMenu, 2000);
        }

        initMobileMenu();

        // Vegas
        if (window.jQuery && window.jQuery.fn.vegas) {
            window.jQuery(function() {
                 window.jQuery.vegas("slideshow", {
                    backgrounds: [{
                        src: "assets/img/1.jpg",
                        fade: 1e3,
                        delay: 9e3
                    }, {src: "assets/img/2.jpg", fade: 1e3, delay: 9e3}, {
                        src: "assets/img/3.jpg",
                        fade: 1e3,
                        delay: 9e3
                    }, {
                        src: "assets/img/sw.jpg",
                        fade: 1e3,
                        delay: 9e3
                    }]
                })("overlay", {src: "assets/plugins/vegas/overlays/15.png"})
            });
        }
    });

})();

// 7. Global Functions (YouTube)
window.loadYouTubeVideo = function(videoId) {
    const container = document.getElementById('youtube-' + videoId);
    if (!container) return;

    const iframe = document.createElement('iframe');

    iframe.src = 'https://www.youtube.com/embed/' + videoId + '?autoplay=1';
    iframe.frameBorder = '0';
    iframe.allowFullscreen = true;
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    iframe.title = '3 Minute Thesis competition video';

    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
    container.appendChild(iframe);
};
