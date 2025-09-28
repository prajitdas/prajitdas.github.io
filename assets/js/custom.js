/*jslint browser: true, node: true, es6: true */
/*global jQuery */

(function (e) {
    'use strict';
    
    var siteController = {
        main_fun: function () {
            // Loader fade out
            e(window).load(function () {
                e('.loader').fadeOut('slow');
            });
            
            // Vegas slideshow initialization
            e(function () {
                e.vegas('slideshow', {
                    backgrounds: [
                        {src: 'assets/img/1.jpg', fade: 1000, delay: 9000},
                        {src: 'assets/img/2.jpg', fade: 1000, delay: 9000},
                        {src: 'assets/img/3.jpg', fade: 1000, delay: 9000},
                        {src: 'assets/img/sw.jpg', fade: 1000, delay: 9000}
                    ]
                })('overlay', {src: 'assets/plugins/vegas/overlays/15.png'});
            });
            
            // Headline animation
            e(function () {
                var headlineElement = e('#headLine'),
                    messages = ['WORKING..', 'LOADING..'],
                    currentIndex = -1;
                
                function animateHeadline() {
                    currentIndex = (currentIndex + 1) % messages.length;
                    headlineElement.html(messages[currentIndex])
                        .fadeIn(1000)
                        .delay(1000)
                        .fadeOut(1000, animateHeadline);
                }
                
                animateHeadline();
            });
        },
        
        initialization: function () {
            siteController.main_fun();
        }
    };
    
    e(document).ready(function () {
        siteController.main_fun();
    });
    
}(jQuery));