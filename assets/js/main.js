/*jslint browser: true, node: true */
/*global jQuery, console */

(function () {
    'use strict';

    jQuery(document).ready(function (e) {
        // Debug: Check jQuery availability
        console.log('Main.js loaded. jQuery version:', e.fn.jquery);

        // Skill level bars animation
        e('.level-bar-inner').css('width', '0');
        e(window).on('load', function () {
            e('.level-bar-inner').each(function () {
                var levelWidth = e(this).data('level');
                e(this).animate({width: levelWidth}, 800);
            });
        });

        // Tooltip for level labels
        e('.level-label').tooltip();

        // Note: RSS and GitHub Activity plugin initialization removed 
        // since target elements (#rss-feeds, #ghfeed) don't exist on the page

        // Back to Top button functionality
        var $backToTop = e('#back-to-top');
        e(window).on('scroll', function () {
            if (e(this).scrollTop() > 300) {
                $backToTop.fadeIn();
            } else {
                $backToTop.fadeOut();
            }
        });

        $backToTop.on('click', function (event) {
            event.preventDefault();
            e('html, body').animate({scrollTop: 0}, 600);
        });
    });
}());