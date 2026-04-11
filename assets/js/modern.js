document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('read-more-btn');
    const moreContent = document.getElementById('about-more');

    if (btn && moreContent) {
        btn.addEventListener('click', function() {
            if (moreContent.classList.contains('visible')) {
                moreContent.classList.remove('visible');
                btn.innerHTML = 'Read More <i class="fas fa-chevron-down"></i>';
            } else {
                moreContent.classList.add('visible');
                btn.innerHTML = 'Read Less <i class="fas fa-chevron-up"></i>';
            }
        });
    }

    // Email obfuscation
    const emailLink = document.getElementById('email-link');
    if (emailLink) {
        const user = 'prajitdas';
        const domain = 'gmail.com';
        emailLink.addEventListener('mouseover', function() {
            this.href = 'mailto:' + user + '@' + domain;
        });
        emailLink.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '#') {
                e.preventDefault();
                window.location.href = 'mailto:' + user + '@' + domain;
            }
        });
    }
});
