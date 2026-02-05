/*jslint browser: true, node: true */
/*global jQuery, console */

(function () {
    'use strict';

    jQuery(document).ready(function (e) {
        // ⚡ Bolt Optimization: Calculate years of experience dynamically
        // Moved from inline script in index.html to reduce HTML size and improve caching
        (function() {
            var today = new Date();
            var pastDate = new Date(2025, 3, 12); // April 12, 2025

            // Calculate the difference in milliseconds
            var timeDifference = today.getTime() - pastDate.getTime();

            // Convert milliseconds to years
            // 4012 + 2465 is the base days of experience calculated previously
            var years = (4012+2465)/365.25 + Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 365.25));

            // Update the DOM element
            var yearsElement = document.getElementById('years-experience');
            if (yearsElement) {
                yearsElement.textContent = Math.floor(years) + ' years';
            }
        })();

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
        e('.level-label').tooltip({
            placement: 'left',
            animation: true,
            title: function () {
                return e(this).closest('.item').find('.level-bar-inner').attr('data-level');
            }
        });

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

        // ⚡ Palette Enhancement: Add icons to publication links
        // Adds visual cues and improves scannability for publication resources
        e('.publications-container .bibtexitem a').each(function() {
            var $link = e(this);
            var text = $link.text().trim().toLowerCase();

            // Skip if icon already exists
            if ($link.find('i.fa').length > 0) return;

            var iconMap = {
                'bib': { icon: 'fa-file-code-o', label: 'BibTeX citation' },
                'pdf': { icon: 'fa-file-pdf-o', label: 'PDF document' },
                '.pdf': { icon: 'fa-file-pdf-o', label: 'PDF document' },
                'doi': { icon: 'fa-external-link', label: 'DOI link' },
                'arxiv': { icon: 'fa-archive', label: 'arXiv preprint' },
                'http': { icon: 'fa-globe', label: 'External link' },
                'https': { icon: 'fa-globe', label: 'External link' },
                'link': { icon: 'fa-globe', label: 'External link' },
                'slides': { icon: 'fa-slideshare', label: 'Presentation slides' },
                'video': { icon: 'fa-play-circle', label: 'Watch video' },
                'abstract': { icon: 'fa-align-left', label: 'Read abstract' }
            };

            var config = iconMap[text];

            // Handle fuzzy matches
            if (!config) {
                if (text.indexOf('.pdf') !== -1) {
                    config = iconMap.pdf;
                } else if (text.indexOf('http') === 0) {
                    config = iconMap.http;
                }
            }

            if (config) {
                $link.prepend('<i class="fa ' + config.icon + '" aria-hidden="true"></i> ');
                if (!$link.attr('aria-label')) {
                    $link.attr('aria-label', config.label);
                }
            }
        });

        /* Back to Top */
        var backToTop = e('#back-to-top');

        // ⚡ Bolt Optimization: Use IntersectionObserver to toggle 'Back to Top' visibility
        // This avoids high-frequency scroll event listeners on the main thread
        if ('IntersectionObserver' in window) {
            var headerObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    // If header is NOT intersecting (scrolled out of view), show button
                    if (!entry.isIntersecting) {
                        backToTop.addClass('visible');
                    } else {
                        backToTop.removeClass('visible');
                    }
                });
            }, { threshold: 0 });

            var header = document.querySelector('.header');
            if (header) {
                headerObserver.observe(header);
            } else {
                // Fallback if header not found
                e(window).scroll(function () {
                    if (e(this).scrollTop() > 200) {
                        backToTop.addClass('visible');
                    } else {
                        backToTop.removeClass('visible');
                    }
                });
            }
        } else {
            // Fallback for older browsers
            e(window).scroll(function () {
                if (e(this).scrollTop() > 200) {
                    backToTop.addClass('visible');
                } else {
                    backToTop.removeClass('visible');
                }
            });
        }

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
                var expanded = $navbarCollapse.hasClass('in');
                $cleanButton.attr('aria-expanded', expanded);
            });
        }

        /* ⚡ Bolt Optimization: Initialize Vegas Slideshow */
        // Moved from inline script in index.html for better caching and performance
        // Only load on desktop (>768px) and if user prefers motion to save bandwidth
        var isDesktop = window.matchMedia("(min-width: 769px)").matches;
        var prefersMotion = window.matchMedia("(prefers-reduced-motion: no-preference)").matches;

        if (e.vegas && isDesktop && prefersMotion) {
            e.vegas("slideshow", {
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
            })("overlay", {src: "assets/plugins/vegas/overlays/15.png"});
        }

        /* ⚡ Bolt Optimization: Lazy Load YouTube Video */
        // Replaces inline onclick and global function with event delegation
        e(document).on('click', '.js-play-youtube', function() {
            var videoId = e(this).data('video-id');
            var containerId = 'youtube-' + videoId;
            var container = document.getElementById(containerId);

            if (container) {
                var iframe = document.createElement('iframe');
                iframe.src = 'https://www.youtube.com/embed/' + videoId + '?autoplay=1';
                iframe.frameBorder = '0';
                iframe.allowFullscreen = true;
                iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
                iframe.title = '3 Minute Thesis competition video';

                // Clear container and append iframe
                while (container.firstChild) {
                    container.removeChild(container.firstChild);
                }
                container.appendChild(iframe);

                // ⚡ Palette Enhancement: Focus Management
                // Move focus to the iframe/container to prevent loss of context for keyboard users
                container.setAttribute('tabindex', '-1');
                container.focus();
            }
        });
    });
}());