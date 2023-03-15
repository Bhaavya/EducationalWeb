var base_url = $('#base-url').data('val');

function log_action(new_slide_name,action,route_path) {
    console.log("Howdy");
    logdata = JSON.stringify({
          action: action,
          updated_slide: new_slide_name, 
          route: route_path
      });
    navigator.sendBeacon(base_url.concat('log_action'), logdata);
}
