
const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

if (JSON.parse(sessionArray) !== null) {
    var session = JSON.parse(sessionArray);
} else {
    var session = [];
}
console.log(session);


function addSessionAjax(session) {
    $.ajax({
        url: ajaxURL,
        type: "POST",
        dataType: "json",
        data: JSON.stringify({session: session}),
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': csrf
        },
        success: (data) => {
            console.log(data)
        },
        error: (error) => {
          console.log(error);
        }
      });
}

function updateClone(clone, count, parent, child, added, sectionCount, largeSection) {
    // updating all the names and ids of fields+elements in the clone
    for (input of clone.getElementsByTagName('input')) {
        input.id += `${largeSection}${sectionCount}${added}_${count}`;
        input.name += `${largeSection}${sectionCount}${added}_${count}`;
    }

    for (select of clone.getElementsByTagName('select')) {
        select.id += `${largeSection}${sectionCount}${added}_${count}`;
        select.name += `${largeSection}${sectionCount}${added}_${count}`;
    }

    for (label of clone.getElementsByTagName('label')) {
        label.htmlFor += `${largeSection}${sectionCount}${added}_${count}`;
    }

    for (div of clone.getElementsByTagName('div')) {
        if (div.id) {
            div.id += `${largeSection}${sectionCount}${added}_${count}`;
        }
    }

    for (a of clone.getElementsByTagName('a')) {
        // updating the aria-controls for bootstrap collapse functions 
        let ariaControls = a.getAttribute("aria-controls");
        a.setAttribute("aria-controls", `${ariaControls}${largeSection}${sectionCount}${added}_${count}`)
        a.href = `#${ariaControls}${largeSection}${sectionCount}${added}_${count}`;
    }

    for (btn of clone.getElementsByTagName('btn')) {
        let btnParent = btn.getAttribute("parent");
        let btnChild = btn.getAttribute("child");
        btn.setAttribute("parent", `${btnParent}${largeSection}${sectionCount}${added}_${count}`);
        btn.parent = `${parent}${largeSection}${sectionCount}${added}_${count}`;
        btn.setAttribute("child", `${btnChild}${largeSection}${sectionCount}${added}_${count}`);
        btn.child = `${child}${largeSection}${sectionCount}${added}_${count}`;
        // updating the ids of the remove button
        if (btn.id) {
            btn.id = `remove_${btnParent}${largeSection}${sectionCount}${added}_${count}`;
        }
    }
    console.log("remove_"+parent);
    let deleteButton;
    if (document.getElementById("remove_"+parent)) {
        deleteButton = document.getElementById("remove_"+parent);
        deleteButton.classList.remove("removefields_button");
    }
    
}

/**
    * adds an inner section in an original section
    * should only be used for original sections due to double naming
 */
function addFields(event) {
    let parent = event.currentTarget.getAttribute("parent");
    let child = event.currentTarget.getAttribute("child");
    let added = event.currentTarget.getAttribute("added");
    
    let sectionCount = "";
    if (added === "_inner") {
        let length = document.querySelector(`#${child}`).children.length-1;
        sectionCount = `_${length}`;
    }

    let count = document.querySelector(`#${parent}`).children.length - 1;
    let clone = document.querySelector(`#${parent}`).children[0].cloneNode(true);

    clone.id += `_added_${count}`;

    session.push(clone.id);

    updateClone(clone, count, parent, child, "_added", sectionCount, "");

    document.getElementById(parent).appendChild(clone);

    addSessionAjax(session);
}


/**
    * adds a major section
 */
function addSection(event) {
    // clones the original geolocation block and changes id and names according to count
    let parent = event.currentTarget.getAttribute("parent");
    let child = event.currentTarget.getAttribute("child");
    let added = event.currentTarget.getAttribute("added");
    let clone;

    // section id could include the "_{number}", or the "_zer", or both
    for (section of globalClones) {
        if (section.id === child || 
            section.id === child.substring(0, child.length - 2) || 
            section.id === child.substring(0, child.length - 4) ||
            section.id === child.substring(0, child.length - 6)) 
            {
                clone = section.cloneNode(true);
            }
    }

    let sectionCount = "";
    // sees if it's an inner function, checks for previous siblings
    // extracts the length of the block to use as naming
    if (added === "_inner") {
        if (event.currentTarget.previousElementSibling != null) {
            let length = event.currentTarget.previousElementSibling.id.slice(-1);
            if (!isNaN(length) && parseInt(length) >= 0) {
                sectionCount = `_${length}`;
            }
        }
    }

    let count = document.querySelector(`#${parent}`).children.length -1;
    let idOfSibling = document.querySelector(`#${child}`).id;
    
    // checks if it's in an added "sample" (largeSection)
    let largeSection = "";
    let largeSectionNaming = ["zer", "one", "two", "thr", "fou"];

    for (let i = 0; i < idOfSibling.length; i++) {
        if (idOfSibling[i] === "_" && largeSectionNaming.includes(idOfSibling.substring(i+1, i+4))) {
            largeSection = idOfSibling.substring(i, i+4);
            break;
        }
    }

    clone.id = `${idOfSibling}${added}_${count}`;

    session.push(clone.id);

    updateClone(clone, count, parent, child, added, sectionCount, largeSection);

    document.getElementById(parent).appendChild(clone);
    addSessionAjax(session);
}

// function made for sample and publication, since we're able to add several samples/publications, which requires unique naming.
// function is similar in setup, but has the additional naming added, which is also added to the other functions...
// ... in the form of largeSection
function addMajorSample(event) {
    let parent = event.currentTarget.getAttribute("parent");
    let child = event.currentTarget.getAttribute("child");
    let clone = globalClones[0].cloneNode(true);

    let count = document.querySelector(`#${parent}`).childElementCount-1;

    conversions = [
        ["0", "zer"],
        ["1", "one"],
        ["2", "two"],
        ["3", "thr"],
        ["4", "fou"]
    ]

    for (key of conversions) {
        if (count.toString() === key[0]) {
            count = key[1];
        }
    }

    clone.id = `${clone.id}_${count}`

    session.push(clone.id);

    updateClone(clone, count, parent, child, "", "", "")

    document.getElementById(parent).appendChild(clone);
    addSessionAjax(session);
}

/**
    * removes last child of any section, updates session
 */
function removeFields(event) {
    let parent = event.currentTarget.getAttribute("parent");
    let parentElement = document.getElementById(parent);

    // getting the last child's id to remove from the session
    let lastChild = parentElement.lastChild;

    let deleteButton = document.getElementById("remove_"+parent);

    // add class that does the animation for remove
    lastChild.classList.add("removefields_animation");

    if (parentElement.children.length == 2) {
        deleteButton.classList.add("removefields_animation");
    }

    // checks if there are added fields within the section that should also be deleted
    let subDeletes = [];
    for (div of lastChild.getElementsByTagName('div')) {
        if (session.includes(div.id)) {
            subDeletes.push(div.id);
        }
    }

    // filter session to remove last child and subdeletes
    session = session.filter(e => e !== lastChild.id && !subDeletes.includes(e));
    // update backend session
    addSessionAjax(session);

    // removing last child
    setTimeout(() => {
        parentElement.removeChild(lastChild);
        // removes class animation from button
        deleteButton.classList.remove("removefields_animation");
        if (parentElement.children.length == 1) {
            // adds display none to button if only one field left
            deleteButton.classList.add("removefields_button");
        }
      }, 400)

}