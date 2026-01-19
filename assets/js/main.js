/*jslint browser: true, node: true */
/*global jQuery, console */

(function () {
    'use strict';

    jQuery(document).ready(function (e) {
        // Skill level bars animation
        e('.level-bar-inner').css('width', '0');

        // ⚡ Bolt Optimization: Use IntersectionObserver to animate only when visible
        // This improves initial load performance and provides better UX
        if ('IntersectionObserver' in window) {
            var observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        var $elem = e(entry.target);
                        var levelWidth = $elem.data('level');
                        $elem.animate({width: levelWidth}, 800);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            e('.level-bar-inner').each(function() {
                observer.observe(this);
            });
        } else {
            // Fallback for older browsers: animate immediately on ready (faster than window.load)
            e('.level-bar-inner').each(function () {
                var levelWidth = e(this).data('level');
                e(this).animate({width: levelWidth}, 800);
            });
        }

        // Tooltip for level labels
        e('.level-label').tooltip();

        // Tooltip for social links
        e('.social a').tooltip({ placement: 'bottom' });

        // Note: RSS and GitHub Activity plugin initialization removed 
        // since target elements (#rss-feeds, #ghfeed) don't exist on the page

        /* Back to Top */
        var backToTop = e('#back-to-top');
        e(window).scroll(function () {
            if (e(this).scrollTop() > 200) {
                backToTop.fadeIn();
            } else {
                backToTop.fadeOut();
            }
        });

        backToTop.on('click', function (e) {
            e.preventDefault();
            jQuery('html, body').animate({scrollTop: 0}, 600);
            return false;
        });

        /* Mobile Menu Initialization */
        // Consolidated from multiple inline scripts in index.html for better performance
        var $navbarToggle = jQuery('.navbar-toggle');
        var $navbarCollapse = jQuery('.navbar-collapse');

        if ($navbarToggle.length && $navbarCollapse.length) {
            // Remove any existing listeners to avoid duplicates
            $navbarToggle.off('click').on('click', function(event) {
                event.preventDefault();
                event.stopPropagation();

                if ($navbarCollapse.hasClass('in')) {
                    $navbarCollapse.removeClass('in');
                    $navbarCollapse.css('display', '');
                } else {
                    $navbarCollapse.addClass('in');
                    $navbarCollapse.css('display', 'block');
                }
            });

            // Add pointer events for touch devices
            $navbarToggle.css({
                'cursor': 'pointer',
                'touch-action': 'manipulation'
            });
        }
    });
}());