// Deferred JavaScript - Non-critical functionality loaded after page render
// Background slideshow and other enhancements that don't block initial paint

(function() {
    'use strict';
    
    // Lightweight Vegas-style background slideshow (replaces 4.4KB Vegas plugin)
    function initBackgroundSlideshow() {
        const images = [
            'assets/img/1.jpg',
            'assets/img/2.jpg', 
            'assets/img/3.jpg',
            'assets/img/sw.jpg'
        ];
        
        if (images.length === 0) return;
        
        let currentIndex = 0;
        const body = document.body;
        
        // Create background container
        const bgContainer = document.createElement('div');
        bgContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            transition: opacity 1s ease-in-out;
        `;
        
        body.insertBefore(bgContainer, body.firstChild);
        
        // Set initial background
        setBackground(0);
        
        function setBackground(index) {
            bgContainer.style.backgroundImage = `url('${images[index]}')`;
        }
        
        function nextSlide() {
            currentIndex = (currentIndex + 1) % images.length;
            
            // Create new background element for smooth transition
            const newBg = bgContainer.cloneNode();
            newBg.style.backgroundImage = `url('${images[currentIndex]}')`;
            newBg.style.opacity = '0';
            
            body.insertBefore(newBg, bgContainer);
            
            // Fade in new background
            setTimeout(() => {
                newBg.style.opacity = '1';
                setTimeout(() => {
                    bgContainer.remove();
                    bgContainer = newBg;
                }, 1000);
            }, 50);
        }
        
        // Change slide every 5 seconds
        setInterval(nextSlide, 5000);
    }
    
    // Enhanced smooth scrolling for internal links
    function initSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(function(link) {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    // Lazy loading for images below the fold
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const lazyImages = document.querySelectorAll('img[data-src]');
            
            const imageObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            lazyImages.forEach(function(img) {
                imageObserver.observe(img);
            });
        }
    }
    
    // Initialize deferred functionality
    function init() {
        console.log('Deferred JS loaded - background enhancements');
        
        // Only initialize slideshow if we're on a page that uses it
        const bodyClass = document.body.className;
        if (bodyClass.includes('slideshow') || document.querySelector('.header')) {
            initBackgroundSlideshow();
        }
        
        initSmoothScrolling();
        initLazyLoading();
    }
    
    // Load after critical content is rendered
    if (document.readyState === 'complete') {
        init();
    } else {
        window.addEventListener('load', init);
    }
    
})();