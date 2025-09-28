jQuery(document).ready(function(e){
	// Debug: Check jQuery availability
	console.log('Main.js loaded. jQuery version:', e.fn.jquery);
	
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
	
	// Note: RSS and GitHub Activity plugin initialization removed 
	// since target elements (#rss-feeds, #ghfeed) don't exist on the page
});