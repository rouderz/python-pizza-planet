/**
 * Fetch the orders and append to the table
 * 
 * ****************************
 * Please change 'json/orders.json' 
 * with your service endpoint below
 * ****************************
 */
fetch('https://wkoelxkuk2.execute-api.us-east-1.amazonaws.com/v1/order/')
    .then(response => response.json())
    .then(orders => {
        let rows = orders.map(element => createOrderTemplate(element));
        let table = $("#orders tbody");
        table.append(rows);
    });

/**
 * Find the template tag and populate it with the data
 * @param order 
 */
function createOrderTemplate(order) {
    let template = $("#order-item-template")[0].innerHTML;
    return Mustache.render(template, order);
}
