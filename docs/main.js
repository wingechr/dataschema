const $ = require("jquery");
const JSONEditor = require("@json-editor/json-editor").JSONEditor;
import "bootstrap";
import "corejs-typeahead/dist/typeahead.jquery.js";


let form = document.getElementById("metaedit-form");
let defaultSchemaUrl = "https://json-schema.org/learn/examples/address.schema.json";
/* parse query args */

const _queryParams = new URLSearchParams(window.location.search);
const queryParams = Object.fromEntries(_queryParams.entries());
let schema_url = queryParams.schema || defaultSchemaUrl;
console.log(schema_url);


let options = {
  schema: {"$ref": schema_url},
  ajax: true,
  disable_properties: true,
  disable_collapse: false,
  disable_edit_json: true,
  prompt_before_delete: false,
  remove_empty_properties: true,
  disable_array_delete_last_row: false,
  disable_array_reorder: true,
  disable_array_delete_all_rows: false,
  array_controls_top: true,
  compact: true,
  theme: 'bootstrap4',
  show_errors: 'always', /* interaction, change, always, never*/
};
const editor = new JSONEditor(form, options);

editor.on('ready', function() {

});
/*
editor.on('ready', function() {


  let btnDownload = editor.root.getButton('Download', 'save');
  let btnUpload = editor.root.getButton('Upload', 'upload');

  let container = document.createElement("span");
  container.appendChild(btnDownload);
  container.appendChild(btnUpload);
  editor.root.header.appendChild(container);


  btnUpload.addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('file-upload').click();
  });

  document.getElementById('file-upload').addEventListener("change", function(e) {
    e.preventDefault();
    e.target.files[0].text().then(function(text) {
      let data = JSON.parse(text);
      console.log(data);
      editor.setValue(data);
    });
  });


  btnDownload.addEventListener('click', function(e) {
    e.preventDefault();
    let example = editor.getValue();
    let filename = 'example.json';
    let blob = new Blob([JSON.stringify(example, null, 2)], {
      type: "application/json;charset=utf-8",
    });

    if (window.navigator && window.navigator.msSaveOrOpenBlob) {
      window.navigator.msSaveOrOpenBlob(blob, filename);
    } else {
      let a = document.createElement('a');
      a.download = filename;
      a.href = URL.createObjectURL(blob);
      a.dataset.downloadurl = ['text/plain', a.download, a.href].join(':');

      a.dispatchEvent(new MouseEvent('click', {
        'view': window,
        'bubbles': true,
        'cancelable': false,
      }));
    }
  }, false);
});
*/


/*
    // Watch for changes in the "age" field
editor.watch('root.age',function() {
  // Get value from "age" field
  var value = editor.getEditor('root.age').getValue();
  // If zipvalue a 4 digit number?
  if (/\d{4}/.test(value)) {
    // Do an AJAX lookup using Bloodhound engine
    zipEngine.search(value, null, function(res) {
      console.log(value, res)
      if (res.length) {
        // Set the value of "name" field to the returned value
        editor.getEditor('root.name').setValue(res[2]);
      }
    });
  }
});

*/

/**
 *
 * @param {*} strs
 * @returns {*}
 */
function substringMatcher(strs) {
  console.log('strs', strs);
  return function findMatches(q, cb) {
    console.log('q', q);
    let matches = [];
    // regex used to determine if a string contains the substring `q`
    let substrRegex = new RegExp(q, 'i');

    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(strs, function(i, str) {
      if (substrRegex.test(str)) {
        matches.push(str);
      }
    });

    console.log('matches', matches);

    cb(matches);
  };
};

let states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
  'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii',
  'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
  'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
  'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
  'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
  'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
  'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
  'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming',
];

$('#the-basics .typeahead').typeahead({
  hint: true,
  highlight: true,
  minLength: 1,
},
{
  name: 'states',
  source: substringMatcher(states),
});
