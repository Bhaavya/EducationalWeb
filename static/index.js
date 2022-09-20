var base_url = 'http://localhost:8097/'
var hideExp = function(){
    toggleExplanationContainer(false);

//    explanation_container = document.getElementById('explanation-container');
    $("#explanation-container").css("z-index", "-1");

    helpBut = document.getElementById('helpfulButton');
    notHelpBut = document.getElementById('notHelpfulButton');
    helpBut.removeEventListener("click", logExp, true); 

    helpBut.removeEventListener("click", logExp, true); 
    notHelpBut.removeEventListener("contextmenu", logExp, true); 
    notHelpBut.removeEventListener("contextmenu", logExp, true); 
}

var docDiv = (doc,searchString) => {
    console.log('bb',doc)
    return(`<div class="card">
     <div class="card-header">
<div style="display: flex;justify-content: space-between;">


         <b style="font-size:14pt;margin-left: 10px;
    padding: 10px;">Explanation of \"${searchString}\"</b>
    <span id="close" style="cursor:pointer;float:right;background:transparent;display:inline-block;
    padding:4px; margin:10px; font-size: 12pt; font-weight: bold;" onclick="hideExp()">X</span>
</div>
</div>
      <div class="card-body">
        <span id='explain_div' style= "display:inline-block; 
    margin:10px;
    padding:10px;
    word-break:break-all;">${doc}</span>
        <br>
    </div>
    </div>`
        );
   
}



var test = function(){
    return "blah";
}

// var socket = io.connect('http://' + document.domain + ':' + location.port);
// console.log("io",io)

var toggleNoExplainText = function(isVisible) {
    displayMode = isVisible ? "block" : "none";
    $("#no-explain-text").css("display", displayMode);
}

var toggleExplanationContainer = function(isVisible) {
    displayMode = isVisible ? "block" : "none";
    $("#docs-div").css("display", displayMode);
    $("#helpfulButton").css("display", displayMode);
    $("#notHelpfulButton").css("display", displayMode);
    $("#google-search-div").css("display","none");
}

var googleResultItemHTML = (result) => {
    item = document.createElement("li");
    item.innerHTML =`
        <a href=${result.link}><h5>${result.title}</h5></a>
        <p><b>${result.displayLink}</b></p>
        <p>${result.htmlSnippet}</p>
    `
    return item;
}

var googleResultsListHMTL = (results) => {
    searchList = document.createElement("ul");
    searchList.className = "scrollable-search-list";
    for (result of results) {
        searchList.appendChild(googleResultItemHTML(result));
    }
    return searchList;
}

var displayGoogleSearch = function(results) {
    resultHTML = googleResultsListHMTL(results);
    $("#google-search-div").css("display", "block");
    searchDisplay = document.getElementById("google-search-div");
    if(searchDisplay.firstChild){
        searchDisplay.removeChild(searchDisplay.firstChild)
    }
    searchDisplay.appendChild(resultHTML);
}

var googleSearchExp = function() {
    $("#google-search-div").empty();
    $("#google-search-div").css("display", "block");
    query = document.getElementById("explain_title").getAttribute("data-query");
    if (query.length > 0) {
        googleQueryExplanation(query)
            .then((results)=> {
                displayGoogleSearch(results);
            })
    }
}

var doGoogleSearch = function(query,txtbook) {
    // query = document.getElementById("search-explanation").getAttribute("data-query");
    context = localStorage.getItem("context"); 
    console.log('dg',context,query)
    if (query.length > 0) {
        toggleExplanationContainer(true);
                    toggleNoExplainText(false);
                    document.getElementById("explain_title").innerHTML = `Explanation for ${query}`;
                    moreBut = document.getElementById("explain_title");
                    moreBut.setAttribute("data-query", query);
                    helpBut = document.getElementById('helpfulButton');
                    notHelpBut = document.getElementById('notHelpfulButton');
                    helpBut.addEventListener('click', function() {
                        logExp('1','',query);
                    } , true);

                    helpBut.addEventListener('contextmenu', function() {
                        logExp('1','',query);
                    } , true);

                    notHelpBut.addEventListener('click', function() {
                        logExp('0','',query);
                    } , true);
                    notHelpBut.addEventListener('contextmenu', function() {
                        logExp('0','',query);
                    } , true);
	 if (txtbook == true){
		  var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {};

                xhttp.open("POST", base_url.concat('txt_search'), true);
                xhttp.setRequestHeader("Content-type", "application/json;charset=utf-8");
                xhttp.send(JSON.stringify({  'query': query}));

	 }
	    else{
        googleQueryExplanation(query)
            .then((results)=> {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {};

                xhttp.open("POST", base_url.concat('google_search'), true);
                xhttp.setRequestHeader("Content-type", "application/json;charset=utf-8");
                xhttp.send(JSON.stringify({ 'results':  results, 'context': context , 'query': query}));
            })
	    }
    }
    else{
         toggleExplanationContainer(false);
                    toggleNoExplainText(true);
    }
}


$(document).ready(function(){
    var source = new EventSource(base_url.concat('streamexplainintro'));
    source.addEventListener('publish', function(event) {
        var data = JSON.parse(event.data);
        console.log("The server says " + data.message);
        $("#explanation-container").css("z-index", "1200");
        if (data.message == "explain"){
            console.log(data.searchString)
            
	
            console.log(data.is_410)
	    localStorage.setItem("context", data.context)
              

            doGoogleSearch(data.searchString,data.is_410);
		
             }
        else{
            if (data.message == "google-search-result"){
                displayGoogleSearch(data.rankedResult);
            }
        }
    }, false);
    source.addEventListener('error', function(event) {
        console.log("Error"+ event)
        // alert("Failed to connect to event stream. Is Redis running?");
    }, false);
// var socket = io()
// socket.connect('http://timan.cs.illinois.edu/', {path:'/eduweb_csintro/socket.io'},{transports: ['websocket']});

// socket.on('message', function(params) {
//     console.log("1")
//     console.log(params['searchString'])
//             localStorage.setItem("context", params['context'])
//                  // doSearch(searchString);

//                  doGoogleSearch(params['searchString']);
//             });

// socket.on('google-search-result', function(searchResults) {
//         displayGoogleSearch(searchResults);
//     });

toggleNoExplainText(false);
    toggleExplanationContainer(false);
});

var logExp = function(isHelpful,expId,expTerm){
    logdata = JSON.stringify({
            action: isHelpful+'###EXP_###'+expTerm+'###'+expId,
            route: window.location.pathname
          });
            navigator.sendBeacon(base_url.concat('log_action'), logdata);
         
}
var doSearch = function(searchString) {
    const data = {
        "searchString": searchString,
    }
    console.log("2")
    console.log(searchString)
    if (searchString!='')
    {
       
    var num_fetched_res = 0
    fetch(base_url.concat('search'), {
    // fetch("http://expertsearch.centralus.cloudapp.azure.com/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    }).then(response => {
        response.json().then(data => {
            console.log("bbb",data)
            
            const doc = data.explanation;
            
            $("#docs-div").empty();
            if (data.num_results>0){
                $("#docs-div").append(
                    docDiv(doc,searchString)
                );
            
          
            $("#helpfulButton").css("display", "block");
            $("#notHelpfulButton").css("display", "block");

     helpBut = document.getElementById('helpfulButton');
     notHelpBut = document.getElementById('notHelpfulButton');
      helpBut.addEventListener('click', function() {
          logExp('1',data.file_names,searchString);
      } , true);

      helpBut.addEventListener('contextmenu', function() {
          logExp('1',data.file_names,searchString);
      } , true);

      notHelpBut.addEventListener('click', function() {
          logExp('0',data.file_names,searchString);
      } , true);
        notHelpBut.addEventListener('contextmenu', function() {
          logExp('0',data.file_names,searchString);
      } , true);
       
  
        
         // else{
        //    $("#loadMoreButton").css("display", "none")
        }
        else{
            $("#docs-div").append(`<h3 style="text-align: center;margin-top:20px;">No Explanation Found</h3>`);
        }
        
       })


    });
}
}



