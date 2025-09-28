jQuery(document).ready(function(e){
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
		
		if (e.fn.rss) {
			try {
				e("#rss-feeds").rss("http://feeds.feedburner.com/TechCrunch/startups",{
					limit:3,
					effect:"slideFastSynced",
					layoutTemplate:"<div class='item'>{entries}</div>",
					entryTemplate:'<h3 class="title"><a href="{url}" target="_blank">{title}</a></h3><div><p>{shortBodyPlain}</p><a class="more-link" href="{url}" target="_blank"><i class="fa fa-external-link"></i>Read more</a></div>'
				});
			} catch(err) {
				console.log('RSS plugin error:', err);
			}
		} else if (retryCount < 20) { // Max 20 retries (2 seconds)
			// Retry after a short delay if RSS plugin not loaded yet
			setTimeout(function() { initRSSFeeds(retryCount + 1); }, 100);
		} else {
			console.log('RSS plugin not available after retries');
		}
	}
	
	// Initialize RSS feeds
	setTimeout(initRSSFeeds, 50);
	
	// GitHub activity feed - only if GitHubActivity is available
	function initGitHubFeed() {
		if (typeof GitHubActivity !== 'undefined') {
			GitHubActivity.feed({username:"caseyscarborough",selector:"#ghfeed"});
		} else {
			// Retry after a short delay if GitHubActivity not loaded yet
			setTimeout(initGitHubFeed, 100);
		}
	}
	
	// Initialize GitHub feed
	setTimeout(initGitHubFeed, 100);
});