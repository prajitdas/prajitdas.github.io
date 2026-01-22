// Enhanced CSI with better loading UX for publications
window.onload = function() {
	var elements = document.getElementsByTagName('*'),
		i;
	for (i in elements) {
		if (elements[i].hasAttribute && elements[i].hasAttribute('data-include')) {
			enhancedFragment(elements[i], elements[i].getAttribute('data-include'));
		}
	}
	
	function enhancedFragment(el, url) {
		var localTest = /^(?:file):/,
			xmlhttp = new XMLHttpRequest(),
			status = 0,
			container = document.getElementById('publications-container'),
			isPublications = url.includes('publications');

		xmlhttp.onreadystatechange = function() {
			if (xmlhttp.readyState == 4) {
				status = xmlhttp.status;
			}
			if (localTest.test(location.href) && xmlhttp.responseText) {
				status = 200;
			}
			if (xmlhttp.readyState == 4 && status == 200) {
				// Success - replace content
				// SECURITY: Basic sanitization - ensure we are only replacing with expected content
				// Ideally use DOMPurify, but for now we rely on trusted source
				el.outerHTML = xmlhttp.responseText;
				if (isPublications && container) {
					container.className = 'publications-loaded';
				}
			} else if (xmlhttp.readyState == 4 && status !== 200) {
				// Error - show fallback
				if (isPublications && container) {
					container.innerHTML = '<div class="publications-error">' +
						'<i class="fa fa-exclamation-triangle"></i> ' +
						'Unable to load publications. <a href="' + url + '" target="_blank" rel="noopener">' +
						'<i class="fa fa-external-link"></i> View Publications</a>' +
						'</div>';
				}
			}
		}

		try { 
			xmlhttp.open("GET", url, true);
			xmlhttp.send();
		} catch(err) {
			// Error handling
			if (isPublications && container) {
				container.innerHTML = '<div class="publications-error">' +
					'<i class="fa fa-exclamation-triangle"></i> ' +
					'Error loading publications. <a href="' + url + '" target="_blank" rel="noopener">' +
					'<i class="fa fa-external-link"></i> View Publications</a>' +
					'</div>';
			}
		}
	}
}
