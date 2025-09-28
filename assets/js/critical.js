// Critical JavaScript - Only above-the-fold functionality
// Replaces heavy jQuery dependency with lightweight vanilla JS
// Focus: Essential DOM manipulation without full jQuery overhead

(function() {
    'use strict';
    
    // Minimal DOM ready function (replaces jQuery document.ready)
    function domReady(callback) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', callback);
        } else {
            callback();
        }
    }
    
    // Lightweight animation utilities
    function animate(element, property, startValue, endValue, duration, unit) {
        unit = unit || '';
        const startTime = performance.now();
        const change = endValue - startValue;
        
        function updateValue(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (ease-out)
            const easedProgress = 1 - Math.pow(1 - progress, 3);
            const currentValue = startValue + (change * easedProgress);
            
            element.style[property] = currentValue + unit;
            
            if (progress < 1) {
                requestAnimationFrame(updateValue);
            }
        }
        
        requestAnimationFrame(updateValue);
    }
    
    // Simple tooltip functionality (replaces Bootstrap tooltips)
    function initTooltips() {
        const tooltipElements = document.querySelectorAll('[data-toggle="tooltip"]');
        
        tooltipElements.forEach(function(element) {
            let tooltip = null;
            
            element.addEventListener('mouseenter', function() {
                const title = element.getAttribute('data-original-title') || element.getAttribute('title');
                if (!title) return;
                
                tooltip = document.createElement('div');
                tooltip.className = 'tooltip-popup';
                tooltip.textContent = title;
                tooltip.style.cssText = `
                    position: absolute;
                    background: #000;
                    color: #fff;
                    padding: 5px 8px;
                    border-radius: 3px;
                    font-size: 12px;
                    z-index: 1000;
                    pointer-events: none;
                    opacity: 0;
                    transition: opacity 0.2s;
                `;
                
                document.body.appendChild(tooltip);
                
                // Position tooltip
                const rect = element.getBoundingClientRect();
                tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
                tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
                
                // Fade in
                setTimeout(() => tooltip.style.opacity = '1', 10);
            });
            
            element.addEventListener('mouseleave', function() {
                if (tooltip) {
                    tooltip.remove();
                    tooltip = null;
                }
            });
        });
    }
    
    // Skill level bar animations (replaces jQuery animations)
    function initSkillBars() {
        const skillBars = document.querySelectorAll('.level-bar-inner');
        
        // Initialize bars to 0 width
        skillBars.forEach(function(bar) {
            bar.style.width = '0%';
        });
        
        // Animate bars when page loads
        function animateSkillBars() {
            skillBars.forEach(function(bar, index) {
                const targetLevel = bar.getAttribute('data-level');
                const targetWidth = parseInt(targetLevel);
                
                // Stagger animations for visual effect
                setTimeout(function() {
                    animate(bar, 'width', 0, targetWidth, 800, '%');
                }, index * 100);
            });
        }
        
        // Trigger animation when scrolled into view or immediately if visible
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        animateSkillBars();
                        observer.disconnect();
                    }
                });
            });
            
            const skillsSection = document.querySelector('.skills');
            if (skillsSection) {
                observer.observe(skillsSection);
            }
        } else {
            // Fallback for browsers without IntersectionObserver
            window.addEventListener('load', animateSkillBars);
        }
    }
    
    // Initialize all functionality when DOM is ready
    domReady(function() {
        console.log('Critical JS loaded - vanilla implementation');
        initTooltips();
        initSkillBars();
    });
    
})();