//used in base.html
var base_url = $('#base-url').data('val');


var hideExp = function() {

	// Unset the css properties
	$("#explanation-container").css("z-index", "-1");
	$(".main_row").css("-webkit-filter", "brightness(1.0) blur(0px)");

	// Hide all contents in container
	toggleNoResultsFound(false);
	toggleNoQuery(false);
	toggleExplanation(false);

	// Disable Logging
	helpBut = document.getElementById('helpfulButton');
	notHelpBut = document.getElementById('notHelpfulButton');
	helpBut.removeEventListener("click", logExp, true);
	helpBut.removeEventListener("click", logExp, true);
	notHelpBut.removeEventListener("contextmenu", logExp, true);
	notHelpBut.removeEventListener("contextmenu", logExp, true);
};

// Function expression for explanation container with no query selected
// Used by hideExp
var toggleNoQuery = function(isVisible) {
	var displayMode = isVisible ? "block" : "none";
	$("#no-explain-text").css("display", displayMode);
	$("#docs-div").css("display", displayMode);
	$("#explain_title").css("display", "None");
};

// Function expression for explanation container with 0 results
// Used by hideExp
var toggleNoResultsFound = function(isVisible) {
	var displayMode = isVisible ? "block" : "none";
	$("#no-explain-results").css("display", displayMode);
	$("#explain_title").css("display", displayMode);
	$("#docs-div").css("display", displayMode);
};

// Function expression for explanation container with results
// Used by hideExp to toggle the explanation 
var toggleExplanation = function(isVisible) {
	var displayMode = isVisible ? "block" : "none";
	$("#docs-div").css("display", displayMode);
	$("#explain_title").css("display", displayMode);
	$("#helpfulButton").css("display", displayMode);
	$("#notHelpfulButton").css("display", displayMode);
	$("#google-search-div").css("display", "none"); // Richa: changed from none to displaymode
};

// Function expression used for looking up in google
var googleResultItemHTML = (result) => {
    item = document.createElement("li");
    item.innerHTML =`
        <a href=${result.link}><h5>${result.title}</h5></a>
        <p><b>${result.displayLink}</b></p>
        <p>${result.htmlSnippet}</p>
    `
    return item;
}
//Used by displaySearch, which is a helper function for the explain function
var googleResultsListHMTL = (results) => {
    searchList = document.createElement("ul");
    searchList.className = "scrollable-search-list";
    for (result of results) {
        searchList.appendChild(googleResultItemHTML(result));
    }
    return searchList;
}
// Used by explain_button function
var displaySearch = function(results) {
	resultHTML = googleResultsListHMTL(results);
	$("#google-search-div").css("display", "block"); // not needed here
	searchDisplay = document.getElementById("google-search-div");
	// Clearing the previous content of searchDisplay
	if (searchDisplay.firstChild) {
		searchDisplay.removeChild(searchDisplay.firstChild);
	}
	searchDisplay.appendChild(resultHTML);
};

 // Used to log helpful button
var logExp = function(isHelpful, expId, expTerm) {
	logdata = JSON.stringify({
		action: isHelpful + '###EXP_###' + expTerm + '###' + expId,
		route: window.location.pathname
	});
	navigator.sendBeacon(base_url.concat('log_action'), logdata);

};

//explain button click steps once it is clicked
$(function() {
	$('#explain_button').click(function() {

		// initialize query of length 0
		var query = "";
		

		// Initialize explanation container visibility
		toggleNoResultsFound(false);
		toggleNoQuery(false);
		toggleExplanation(true);

		// get query from window selection
		if (window.getSelection) {
			query = window.getSelection().toString();
		} 

		// Update the CSS properties of explanation container on popup
		$("#explanation-container").css("z-index", "1200");
		$(".main_row").css("-webkit-filter", "brightness(0.7) blur(2px)");

		if (query.length > 0) {
			// Adds the explanation header and sets data-query attribute
			document.getElementById("explain_title").innerHTML = `Explanation for ${query}`;
			moreBut = document.getElementById("explain_title");
			moreBut.setAttribute("data-query", query);

			// Add event listeners to log user activity for explanation container
			helpBut = document.getElementById('helpfulButton');
			notHelpBut = document.getElementById('notHelpfulButton');
			helpBut.addEventListener('click', function() {
				logExp('1', '', query);
			}, true);
			helpBut.addEventListener('contextmenu', function() {
				logExp('1', '', query);
			}, true);
			notHelpBut.addEventListener('click', function() {
				logExp('0', '', query);
			}, true);
			notHelpBut.addEventListener('contextmenu', function() {
				logExp('0', '', query);
			}, true);
			var postAjaxRequest = function(isGoogleSearch, results) {
				$.ajax({
					type: "POST",
					url: base_url.concat('explain_query'),
					timeout: 3000,
					contentType: "application/json;charset=utf-8",
					data: JSON.stringify({
						'url': window.location.href,
						'searchString': query,
						'slidesContext': $("#textLayerid").text(),
						'route': window.location.pathname,
						'results': results
					}),

					success: function(data) { // success callback function

						// Adding this check for results.length again as textbook search may also return 0 results
						if (data.rankedResult.length > 0) {
						// explanation container is already turned on
							displaySearch(data.rankedResult);
						} else {
                            toggleExplanation(false);
							toggleNoResultsFound(true);
						}
					}
				});
			};

			// if 410, the API will look from the textbook and the result list should be empty
			if (window.location.href.toString().includes("CS%20410")) {
				postAjaxRequest(false, "");
			} else {
				// if other courses, API needs results to be ranked
				googleQueryExplanation(query)
					.then((results) => {
							postAjaxRequest(true, results);
					});
			}
		} else {
           // If invalid query is selected
            toggleExplanation(false);
			toggleNoQuery(true);
		}
	});
});
