

const GOOGLE_SEARCH_API  = $('#GOOGLE-SEARCH-API').data('val');
const CX = $('#CX').data('val');
const API_KEY = $('#API-KEY').data('val');

//Used by explain.js file
//Called in slide.html


// Used for gapi.load("client", init)
function init() {
    gapi.client.setApiKey(API_KEY);
    gapi.client.load(GOOGLE_SEARCH_API)
        .then(() => { console.log("GAPI client loaded for API"); })
        .catch( (err) => { console.error("Error loading GAPI client for API", err); });
}

// Used in explain.js by by the explain_button function
function googleQueryExplanation(query) {
    return gapi.client.search.cse.list({
        "cx": CX,
        "q": query
    })
        .then((response) => {
            // Handle the results here (response.result has the parsed body).
            if (response.status==200) {
                return response.result.items;
            } else {
                return [];
            }
        })
        .catch( (err) => { 
            console.error("Execute error", err); 
            return [];
        });
}

gapi.load("client", init);
