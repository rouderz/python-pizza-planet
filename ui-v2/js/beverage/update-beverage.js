
function fetchBeverage(_id) {
    fetch(`https://wkoelxkuk2.execute-api.us-east-1.amazonaws.com/v1/beverage/id/${_id}`)
        .then(response => response.json())
        .then(beverage => {
            $("#_id").val(beverage._id);
            $("#name").val(beverage.name);
            $("#price").val(beverage.price);

        });
}

function loadInformation() {
    let urlParams = new URLSearchParams(window.location.search);
    let _id = urlParams.get('_id');
    fetchBeverage(_id)
}

function putBeverage(beverage) {
    fetch('https://wkoelxkuk2.execute-api.us-east-1.amazonaws.com/v1/beverage/', {
        method: 'PUT',
        body: JSON.stringify(beverage),
        headers: {
            "Content-Type": "application/json; charset=utf-8",
        },
    })
        .then(res => res.json())
        .then(res => showNotification());


}

/**
 * Get the form and submit it with fetch API
 */
let beverageForm = $("#beverage-form");
beverageForm.submit(event => {

    let beverage = getBeverageData();
    putBeverage(beverage);

    event.preventDefault();
    event.currentTarget.reset();
    setTimeout(() => window.location.href = '/app/beverage/beverages.html', 3000);
});

/**
 * Gets the beverage data with JQuery
 */
function getBeverageData() {
    console.log({
        _id: $("input[id='_id']").val(),
        name: $("input[id='name']").val(),
        price: $("input[id='price']").val()
    })
    return {
        _id: $("input[id='_id']").val(),
        name: $("input[id='name']").val(),
        price: $("input[id='price']").val()
    };
}

/**
 * Shows a notification when the beverage is accepted
 */
function showNotification() {
    let beverageAlert = $("#beverage-alert");
    beverageAlert.toggle();
    setTimeout(() => beverageAlert.toggle(), 5000);
}


window.onload = loadInformation;