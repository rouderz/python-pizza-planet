
function fetchIngredient(_id) {
    fetch(`https://wkoelxkuk2.execute-api.us-east-1.amazonaws.com/v1/ingredient/id/${_id}`)
        .then(response => response.json())
        .then(ingredient => {
            $("#_id").val(ingredient._id);
            $("#name").val(ingredient.name);
            $("#price").val(ingredient.price);

        });
}

function loadInformation() {
    let urlParams = new URLSearchParams(window.location.search);
    let _id = urlParams.get('_id');
    fetchIngredient(_id)
}

function putIngredient(ingredient) {

    fetch('https://wkoelxkuk2.execute-api.us-east-1.amazonaws.com/v1/ingredient/', {
        method: 'PUT',
        body: JSON.stringify(ingredient),
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
let ingredientForm = $("#ingredient-form");
ingredientForm.submit(event => {

    let ingredient = getIngredientData();
    putIngredient(ingredient);

    event.preventDefault();
    event.currentTarget.reset();
    setTimeout(() => window.location.href = '/app/ingredient/ingredients.html', 3000);
});

/**
 * Gets the ingredient data with JQuery
 */
function getIngredientData() {
    return {
        _id: $("input[id='_id']").val(),
        name: $("input[id='name']").val(),
        price: $("input[id='price']").val()
    };
}

/**
 * Shows a notification when the ingredient is accepted
 */
function showNotification() {
    let ingredientAlert = $("#ingredient-alert");
    ingredientAlert.toggle();
    setTimeout(() => ingredientAlert.toggle(), 5000);
}


window.onload = loadInformation;