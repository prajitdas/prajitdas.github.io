/*jslint browser: true, node: true */
/*global jQuery, console */

(function () {
    'use strict';

    jQuery(document).ready(function (e) {
        // Debug: Check jQuery availability
        console.log('Main.js loaded. jQuery version:', e.fn.jquery);

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

        // Note: RSS and GitHub Activity plugin initialization removed 
        // since target elements (#rss-feeds, #ghfeed) don't exist on the page
    });
}());