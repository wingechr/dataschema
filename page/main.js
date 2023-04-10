"use strict";

const JSONEditor = require("@json-editor/json-editor").JSONEditor;
const bs = require("bootstrap");


function getJson(url) {
return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.open("GET", url);
    request.send();
    request.onload = function() {
    resolve(JSON.parse(request.responseText));
    };
});
}



var url = "https://raw.githubusercontent.com/wingechr/dataschema/master/dataschema/data/tabular-data-package.schema.json"
getJson(url).then(function(schema){
    const editor = new JSONEditor(
        document.getElementById('editor'),
        {
            schema: schema,
            style: "bootstrap5"
        }
    );
})
