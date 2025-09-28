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
	function initRSSFeeds() {
		if (e.fn.rss) {
			e("#rss-feeds").rss("http://feeds.feedburner.com/TechCrunch/startups",{
				limit:3,
				effect:"slideFastSynced",
				layoutTemplate:"<div class='item'>{entries}</div>",
				entryTemplate:'<h3 class="title"><a href="{url}" target="_blank">{title}</a></h3><div><p>{shortBodyPlain}</p><a class="more-link" href="{url}" target="_blank"><i class="fa fa-external-link"></i>Read more</a></div>'
			});
		} else {
			// Retry after a short delay if RSS plugin not loaded yet
			setTimeout(initRSSFeeds, 100);
		}
	}
	
	// Initialize RSS feeds
	setTimeout(initRSSFeeds, 100);
	
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