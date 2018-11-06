function myautocomplete(inp, hidden, arr) {
    // the autocomplete function takes two arguments,
    // the text field element and an array of possible autocompleted values:

    console.log(arr);
    var currentFocus;

    // execute a function when someone writes in the text field:
    inp.addEventListener("input", function(e) {
        var listContainer, listItem, val = this.value;

        // close any already open lists of autocompleted values
        closeAllLists();
        if (!val) { 
            return false;
        }

        currentFocus = -1;

        // create a DIV element that will contain the items (values):
        listContainer = document.createElement("DIV");
        listContainer.setAttribute("id", this.id + "autocomplete-list");
        listContainer.setAttribute("class", "autocomplete-items");

        // append the DIV element as a child of the autocomplete container:
        this.parentNode.appendChild(listContainer);

        // for each item in the array...
        for (var idx = 0; idx < arr.length; idx++) {
            // check if the item starts with the same letters as the text field value:

            if (arr[idx]["name"].toUpperCase().includes(val.toUpperCase())) {
                // create a DIV element for each matching element:
                listItem = document.createElement("DIV");
                listItem.innerHTML += "<span>" + arr[idx]["name"] + "</span>";

                // insert a input field that will hold the current array item's value:
                listItem.innerHTML += "<input type='hidden' value='"+ arr[idx]["id"] +"'>";

                // execute a function when someone clicks on the item value (DIV element):
                listItem.addEventListener("click", function(e) {
                    // insert the value for the autocomplete text field:
                    inp.value = this.getElementsByTagName("span")[0].innerHTML.trim();
                    hidden.value = this.getElementsByTagName("input")[0].value.trim();

                    // close the list of autocompleted values,
                    // (or any other open lists of autocompleted values:
                    closeAllLists();
                });
                listContainer.appendChild(listItem);
            }
        }
    });

    // execute a function presses a key on the keyboard:
    inp.addEventListener("keydown", function(e) {
        hidden.value = null;

        var listContainer = document.getElementById(this.id + "autocomplete-list");

        if (listContainer) {
            listContainer = listContainer.getElementsByTagName("div");
        }

        if (e.keyCode == 40) {
            // If the arrow DOWN key is pressed,
            // increase the currentFocus variable:
            currentFocus++;

            // and and make the current item more visible:
            addActive(listContainer);
        } else if (e.keyCode == 38) { //up
            // If the arrow UP key is pressed,
            // decrease the currentFocus variable:
            currentFocus--;

            // and and make the current item more visible:
            addActive(listContainer);
        } else if (e.keyCode == 13) {
            // If the ENTER key is pressed, prevent the form from being submitted,
            e.preventDefault();
            if (currentFocus > -1) {
                // and simulate a click on the "active" item:
                if (listContainer) {
                    listContainer[currentFocus].click();
                }
            }
        }
    });

    function addActive(listContainer) {
        // a function to classify an item as "active":
        if (!listContainer) {
            return false;
        }

        // start by removing the "active" class on all items:
        removeActive(listContainer);

        if (currentFocus >= listContainer.length) {
            currentFocus = 0;
        }

        if (currentFocus < 0) {
            currentFocus = (listContainer.length - 1);
        }

        // add class "autocomplete-active":
        listContainer[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(listContainer) {
        // a function to remove the "active" class from all autocomplete items:
        for (var i = 0; i < listContainer.length; i++) {
            listContainer[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        // close all autocomplete lists in the document,
        // except the one passed as an argument:
        var listContainer = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < listContainer.length; i++) {
            if (elmnt != listContainer[i] && elmnt != inp) {
                listContainer[i].parentNode.removeChild(listContainer[i]);
            }
        }
    }

    // execute a function when someone clicks in the document:
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}
