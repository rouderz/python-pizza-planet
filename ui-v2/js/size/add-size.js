function postSize(size) {

    fetch('https://wkoelxkuk2.execute-api.us-east-1.amazonaws.com/v1/size/', {
        method: 'POST',
        body: JSON.stringify(size),
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
let sizeForm = $("#size-form");
sizeForm.submit(event => {

    let size = getSizeData();
    postSize(size);

    event.preventDefault();
    event.currentTarget.reset();
    setTimeout(() => window.location.href = '/app/size/sizes.html', 3000);

});

/**
 * Gets the order data with JQuery
 */
function getSizeData() {

    return {
        name: $("input[name='name']").val(),
        price: $("input[name='price']").val(),
    };
}

/**
 * Shows a notification when the order is accepted
 */
function showNotification() {
    let sizeAlert = $("#size-alert");
    sizeAlert.toggle();
    setTimeout(() => sizeAlert.toggle(), 5000);
}