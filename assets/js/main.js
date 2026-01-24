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

        // ⚡ Palette Enhancement: Accessibility for new tabs
        // Automatically adds warning for screen readers on links opening in new tabs
        e('a[target="_blank"]').each(function() {
            var $link = e(this);

            // Ensure security attribute is present
            if (!$link.attr('rel')) {
                $link.attr('rel', 'noopener');
            } else if ($link.attr('rel').indexOf('noopener') === -1) {
                $link.attr('rel', $link.attr('rel') + ' noopener');
            }

            // Check if it already has screen reader text or label
            if ($link.find('.sr-only').length === 0 && !$link.attr('aria-label')) {
                $link.append(' <span class="sr-only">(opens in a new tab)</span>');
            }
        });

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

        backToTop.on('click', function (evt) {
            evt.preventDefault();

            // Respect reduced motion preference
            var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
            var duration = prefersReducedMotion ? 0 : 600;

            jQuery('html, body').animate({scrollTop: 0}, duration).promise().then(function() {
                // Move focus to top-level element to maintain keyboard context
                // This ensures keyboard users aren't lost after the button disappears
                jQuery('.navbar-brand').focus();
            });

            return false;
        });

        /* ⚡ Bolt Optimization: Robust Mobile Menu Initialization */
        // Replaces redundant inline scripts and polling from index.html
        // Consolidates logic into the main bundle for better performance
        var $toggleButton = e('.navbar-toggle');
        var $navbarCollapse = e('.navbar-collapse');

        if ($toggleButton.length && $navbarCollapse.length) {
            // Replace the button to remove any existing/conflicting event listeners
            // and remove data-toggle to prevent double-handling by Bootstrap
            var $cleanButton = $toggleButton.clone();
            $cleanButton.removeAttr('data-toggle');
            $toggleButton.replaceWith($cleanButton);

            $cleanButton.on('click', function(evt) {
                evt.preventDefault();
                evt.stopPropagation();
                $navbarCollapse.toggleClass('in');
            });
        }
    });
}());