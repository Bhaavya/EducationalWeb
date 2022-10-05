$(function(){
    $('#explain_button').click(function() {
        alert("Explain Button Clicked");
        var query = "";
        console.log($("#textLayerid").text());
        if (window.getSelection) {
               query = window.getSelection().toString();

        }

    googleQueryExplanation(query)
            .then((results)=> {
                console.log(results);
                $.ajax({
                    type: "POST",
                    url:"/explain_function",
                    timeout: 3000,
                    contentType: "application/json;charset=utf-8",
                    data: JSON.stringify({ 'url':window.location.href,'searchString':  query,'slidesContext': $("#textLayerid").text() ,  'route': window.location.pathname, 'results':  results}),

                    success: function (data, status, xhr) {// success callback function
                            console.log(data);
                        }
                    });
            });
//    $.ajax({
//        type: "POST",
//        url:"/explain_function",
//        timeout: 3000,
//        contentType: "application/json;charset=utf-8",
//        data: JSON.stringify({ 'url':window.location.href,'searchString':  text,'slidesContext': $("#textLayerid").text() ,  'route': window.location.pathname}),
//
//        success: function (data, status, xhr) {// success callback function
//                console.log(data);
//            }
//        });

    });
});








