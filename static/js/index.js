/******************* Raw *******************/
const hello = "Hello";
/******************* Main *******************/

const fullname = (title, fname, lname) => {
    if (title == "01") {
        title = "Mr.";
    } else if (title == "02") {
        title = "Ms.";
    } else if (title == "03") {
        title = "Mrs.";
    }
    data = `${title} ${fname} ${lname}`;

    return data;
}

const dataTable = (data) => {
    if (data.length <= 5) {
        const $table = $("table");
        $table.removeClass("dataTable");
    } else {
        $(".dataTable").DataTable();
    }
}

const postData = async (url = "", data = {}) => {
    try {
        const req = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const res = await req.json();
        return res;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

const cap = (event, reg = 1, captype = 1) => {
    const id = event.target.id;
    const inputField = document.getElementById(id);
    var regvalue;
    if (captype == 1) {
        // flwordcap = First Letter Word Captilize
        firstLetterofWordCap(event);
    } else if (captype == 2) {
        // All Capitals
        capitalizeAll(event);
    }

    if (reg == 0) {
        // Cannot enter spaces .. for names .. for single words
        regvalue = /^[a-zA-Z]*$/;
    } else if (reg == 1) {
        // Can enter spaces .. for multiple words
        regvalue = /^[a-zA-Z\s]*$/;
    } else if (reg == 2) {
        // Can enter spaces and some special chars .. for multiple words and some special chars
        regvalue = /^[a-zA-Z0-9()/|.-\s]*$/
    } else if (reg == 3) {
        // for pancard
        regvalue = /^[A-Z0-9]*$/
    }

    inputField.addEventListener("input", function (event) {
        const pattern = regvalue;
        const inputValue = inputField.value;

        if (!pattern.test(inputValue)) {
            inputField.value = inputValue.slice(0, -1);
        }
    });
}

const number = (event, reg = 0, aadhar = 0) => {
    const id = event.target.id;
    const inputField = document.getElementById(id);
    var regvalue
    if (reg == 0) {
        // for pincode, contact
        regvalue = /^[0-9]*$/;
    } else if (reg == 1) {
        // aadhar card
        regvalue = /^[0-9\s]*$/;
    }

    if (aadhar == 1) {
        aadharNo(event);
    }

    inputField.addEventListener("input", function (event) {
        const pattern = regvalue;
        const inputValue = inputField.value;

        if (!pattern.test(inputValue)) {
            inputField.value = inputValue.slice(0, -1);
        }
    });
}


const makeMandatory = (value) => {
    let id = "#" + value;
    $(id).attr("required", "required");
}

const makeNonMandatory = (value) => {
    let id = "#" + value;
    $(id).removeAttr("required");
}

/******************* Helper *******************/
const firstLetterofWordCap = (event) => {
    const id = event.target.id;
    const inputField = document.getElementById(id);
    inputValue = inputField.value;

    inputValue = inputValue.replace(/\b\w/g, function (l) {
        return l.toUpperCase();
    });
    inputField.value = inputValue;
}

const capitalizeAll = (event) => {
    const id = event.target.id;
    const inputField = document.getElementById(id);
    inputValue = inputField.value;

    inputValue = inputValue.replace(/./g, function (l) {
        return l.toUpperCase();
    });
    inputField.value = inputValue;
}

const aadharNo = (event) => {
    const id = event.target.id;
    const inputField = document.getElementById(id);
    inputValue = inputField.value;

    inputValue = inputValue.replace(/[^0-9]/g, '').replace(/(\d{4})(?=\d)/g, '$1 ');
    inputField.value = inputValue;
}


/******************* Unused *******************/
const fieldValidation = (event) => {
    const id = event.target.id;
    const label = document.querySelector(`label[for='${id}']`);
    const labelText = label.textContent;
    const myField = document.getElementById(id);

    inputField.addEventListener("input", function (event) {
        if (myField.val == "") {
            myField.setCustomValidity("Please fill out " + labelText + " field");
        }
    });
}
