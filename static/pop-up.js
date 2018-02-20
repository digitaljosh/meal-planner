
// {/* <button onclick="myFunction()">food</button> */}

// THE FOLLOWING IS FROM RICKS HARRY POTTER PROMPT 
function dinnerFunction() {
    var txt;
    // var day = document.createElement('input');
    // $(inputDate).attr('type', 'text')
    //var recipe = prompt("What's for dinner", "search");
    // if using day as button var day = document.getElementById("date").value;
    var date = prompt("What day?", "2018-02-24")
    if (recipe == null || recipe == "") {
        txt = "User cancelled the prompt.";
    } else {
        txt = "You want " + recipe + " for dinner?";
        //check if recipe in db, retrieve recipe object and insatite day or
        // send recipe to spoontacular api and instantiate with returned data
        // then add day to events.json
        // add a date query/prompt
    }
    //document.getElementById("day-num-whatever").innerHTML = recipe;
    document.getElementById("pop-up-confirm").innerHTML = date;
}