fetch('https://wkoelxkuk2.execute-api.us-east-1.amazonaws.com/v1/report/')
    .then(response => response.json())
    .then(report => {
        let table_customers = $("#customers tbody");
        let table_ingredients = $("#ingredients tbody");
        let table_month_revenue = $("#revenue tbody");
        let rows_customers = report.best_customers.map(element => createCustomersReportTemplate(element));
        let rows_ingredients = report.most_requested_ingredient.map(element => createIngredientsReportTemplate(element));
        let rows_revenue = report.date_with_most_revenue.map(element => createRevenueReportTemplate(element));
        table_customers.append(rows_customers);
        table_ingredients.append(rows_ingredients);
        table_month_revenue.append(rows_revenue)
    });

function createCustomersReportTemplate(report) {
    let template = $("#report-item-template")[0].innerHTML;
    return Mustache.render(template, report);
}

function createIngredientsReportTemplate(report){
    let template = $("#ingredient-item-template")[0].innerHTML;
    console.log(template)
    return Mustache.render(template, report);
}

function createRevenueReportTemplate(report){
    let template = $("#revenue-item-template")[0].innerHTML;
    console.log(template)
    return Mustache.render(template, report);
}

