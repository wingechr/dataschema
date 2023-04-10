"use strict";

require("bootstrap");

// eslint-disable-next-line max-len
const defaultSchemaUrl = "https://raw.githubusercontent.com/wingechr/dataschema/master/dataschema/data/tabular-data-package.schema.json";
const JSONEditor = require("@json-editor/json-editor").JSONEditor;
// eslint-disable-next-line no-unused-vars
let editor;

/**
 *
 * @param {str} url
 * @returns {Promise}
 */
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


getJson(defaultSchemaUrl).then(function(schema) {
  editor = new JSONEditor(
      document.getElementById('editor'),
      {
        schema: schema,
        theme: "bootstrap5",
      },
  );
});
