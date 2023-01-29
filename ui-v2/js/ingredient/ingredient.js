

fetch('https://wkoelxkuk2.execute-api.us-east-1.amazonaws.com/v1/ingredient')
    .then(response => response.json())
    .then(ingredients => {
        let rows = ingredients.map(element => createIngredientTemplate(element));
        let table = $("#ingredients tbody");
        table.append(rows);
    });


function createIngredientTemplate(ingredient) {
    let template = $("#ingredient-item-template")[0].innerHTML;
    return Mustache.render(template, ingredient);
}
