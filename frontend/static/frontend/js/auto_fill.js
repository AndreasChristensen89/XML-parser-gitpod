
$(document).ready(function () {
    let data;
    if (JSON.parse(uploaded_data) !== null) {
        data = JSON.parse(uploaded_data);
    } else {
        data = null;
    }
    if (data === null) {
        let btn = document.getElementById("fill_in_button");
        btn.disabled = true;

    } else {
        let clearData = document.getElementById("clearSampleData");
        clearData.style.display = "block";

        let insertBtn = document.getElementById("fillInSampleData");
        insertBtn.style.display = "block";
    }
    
    let experimentalistUid;
    let laboratoryUid;
    if (document.getElementById("autofill_experimentalist_uid")) {
        experimentalistUid = document.getElementById("autofill_experimentalist_uid").getAttribute("data-autofill");
    }
    if (document.getElementById("autofill_laboratory_uid")) {
        laboratoryUid = document.getElementById("autofill_laboratory_uid").getAttribute("data-autofill");
    }
    

    // get form and children
    let form = document.getElementById("form");
    let children = form.querySelectorAll("*");
    // loop through children and insert value on match
    for (child of children) {
        if (child.id === "id_experimentalists_x_experimentalist_uid") {
            child.value = experimentalistUid;
        } else if (child.id === "id_experiment_x_laboratory_uid") {
            child.value = laboratoryUid;
        }

    }
});

function fillInUploadedData() {
    // parse dictionary with JSON
    let data;
    if (JSON.parse(uploaded_data) !== null) {
        data = JSON.parse(uploaded_data);
    } else {
        data = null;
    }
    let selectElements = document.forms['form'].getElementsByTagName('select')
    let inputElements = document.forms['form'].getElementsByTagName('input')
    
    // loop through dictionary
    for (const [key, value] of Object.entries(data)) {
        for (e of selectElements) {
            if (e.name === `${value[0]}_x_${value[1]}`) {
                console.log(`Searched ${value[0]}_x_${value[1]}`)
                console.log(`Found ${e}`)
                console.log(`The current element value is "${e.value}"`)
                console.log(`The attempted input to insert is is ${value[2]}`)
                e.value = value[2];
                console.log(`The new element value is "${e.value}"`)
                break;
            }
        }
        for (e of inputElements) {
            if (e.name === `${value[0]}_x_${value[1]}`) {
                console.log(`Searched ${value[0]}_x_${value[1]}`)
                console.log(`Found ${e}`)
                console.log(`The current element value is "${e.value}"`)
                console.log(`The attempted input to insert is is ${value[2]}`)
                e.value = value[2];
                console.log(`The new element value is "${e.value}"`)
                break;
            }
        }
      }
}

