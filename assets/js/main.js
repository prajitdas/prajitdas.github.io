jQuery(document).ready(function(e){
	// Debug: Check jQuery and plugins availability
	console.log('Main.js loaded. jQuery version:', e.fn.jquery);
	console.log('RSS plugin available:', typeof e.fn.rss !== 'undefined');
	console.log('GitHub Activity available:', typeof GitHubActivity !== 'undefined');
	
	// Skill level bars animation
	e(".level-bar-inner").css("width","0");
	e(window).on("load",function(){
		e(".level-bar-inner").each(function(){
			var t=e(this).data("level");
			e(this).animate({width:t},800);
		});
	});
	
	// Tooltip for level labels
	e(".level-label").tooltip();
	
	// RSS feeds - only if RSS plugin is available
	function initRSSFeeds(retryCount) {
		retryCount = retryCount || 0;
		
		// Check if RSS target element exists
		var rssTarget = e("#rss-feeds");
		if (rssTarget.length === 0) {
			console.log('RSS target element #rss-feeds not found, skipping RSS initialization');
			return;
		}
		
		if (e.fn.rss && typeof e.fn.rss === 'function') {
			console.log('RSS plugin found, initializing feeds...');
			try {
				rssTarget.rss("http://feeds.feedburner.com/TechCrunch/startups",{
					limit:3,
					effect:"slideFastSynced",
					layoutTemplate:"<div class='item'>{entries}</div>",
					entryTemplate:'<h3 class="title"><a href="{url}" target="_blank">{title}</a></h3><div><p>{shortBodyPlain}</p><a class="more-link" href="{url}" target="_blank"><i class="fa fa-external-link"></i>Read more</a></div>',
					error: function() {
						console.log('RSS feed loading failed - feed URL may be unavailable');
					},
					success: function() {
						console.log('RSS feed loaded successfully');
					}
				});
			} catch(err) {
				console.log('RSS plugin error:', err);
			}
		} else if (retryCount < 30) { // Increased to 30 retries (3 seconds)
			console.log('RSS plugin not ready, retry', retryCount + 1);
			setTimeout(function() { initRSSFeeds(retryCount + 1); }, 100);
		} else {
			console.log('RSS plugin not available after', retryCount, 'retries');
		}
	}
	
	// Initialize RSS feeds with longer delay to ensure plugin is loaded
	setTimeout(initRSSFeeds, 200);
	
	// GitHub activity feed - only if GitHubActivity is available
	function initGitHubFeed(retryCount) {
		retryCount = retryCount || 0;
		
		if (typeof GitHubActivity !== 'undefined') {
			try {
				GitHubActivity.feed({username:"caseyscarborough",selector:"#ghfeed"});
			} catch(err) {
				console.log('GitHub Activity plugin error:', err);
			}
		} else if (retryCount < 30) { // Max 30 retries (3 seconds) - GitHub activity loads later
			// Retry after a short delay if GitHubActivity not loaded yet
			setTimeout(function() { initGitHubFeed(retryCount + 1); }, 100);
		} else {
			console.log('GitHub Activity plugin not available after retries');
		}
	}
	
	// Initialize GitHub feed with longer delay since it loads later
	setTimeout(initGitHubFeed, 200);
});