function postBeverage(beverage) {

    fetch('https://wkoelxkuk2.execute-api.us-east-1.amazonaws.com/v1/beverage/', {
        method: 'POST',
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
    postBeverage(beverage);

    event.preventDefault();
    event.currentTarget.reset();
    setTimeout(() => window.location.href = '/app/beverage/beverages.html', 3000);
});

/**
 * Gets the order data with JQuery
 */
function getBeverageData() {

    return {
        name: $("input[name='name']").val(),
        price: $("input[name='price']").val(),
    };
}

/**
 * Shows a notification when the order is accepted
 */
function showNotification() {
    let beverageAlert = $("#beverage-alert");
    beverageAlert.toggle();
    setTimeout(() => beverageAlert.toggle(), 5000);

}