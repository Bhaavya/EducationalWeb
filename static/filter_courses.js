// used for search bar in courses' and lectures' dropdown menu
function dropdownSearchbarFilterFunction(inputID, dropdownMenuID) {
  // var input, filter, ul, li, courseList, i;
  var input = document.getElementById(inputID); // finds the input according to the input's id
  var inputText = input.value.toUpperCase(); // takes in user's input string and puts it all in upper case
  var dropdownList = document.getElementById(dropdownMenuID); // gets the dropdown menu
  var links = dropdownList.getElementsByTagName("a"); // gets all the links to courses/lectures (which each have <a> tags)
  var name; // name of lecture/course
    for (i = 0; i < links.length; i++) {
    name = links[i].textContent; // gets the actual name of the course or lecture, including spaces
    // indexOf method returns -1 if the value is not found
    if (name.toUpperCase().indexOf(inputText) > -1) {
      links[i].style.display = "";
    } else {
      // no course name corresponds to user input so we delete course name from dropdown (i.e, "none")
      links[i].style.display = "none";
    }
  }
}