
fetch('https://wkoelxkuk2.execute-api.us-east-1.amazonaws.com/v1/size/')
    .then(response => response.json())
    .then(sizes => {
        let rows = sizes.map(element => createSizeTemplate(element));
        let table = $("#sizes tbody");
        table.append(rows);
    });


function createSizeTemplate(size) {
    let template = $("#size-item-template")[0].innerHTML;
    return Mustache.render(template, size);
}
