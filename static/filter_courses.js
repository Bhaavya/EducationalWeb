// @param: inputID is id of the user's text input; dropdownMenuID is id of relevant dropdown menu (e.g, lecture, courses, etc)
// Filters dropdown menu items according to matches with user input. Note that spacing does not matter.
 function dropdownSearchbarFilterFunction(inputID, dropdownMenuID) {
      var input = document.getElementById(inputID);
      var inputText = input.value.toUpperCase().replace(/\s/g, '');
      var dropdownList = document.getElementById(dropdownMenuID);
      var links = dropdownList.getElementsByTagName("a");
      for (i = 0; i < links.length; i++) {
        var name = links[i].innerText.replace(/\s/g, '');
        if (name.toUpperCase().indexOf(inputText) > -1) {
          links[i].style.display = "";
        } else {
          links[i].style.display = "none";
        }
      }
    }