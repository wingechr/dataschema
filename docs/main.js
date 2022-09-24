let form = document.getElementById("metaedit-form");

/* parse query args */

const _queryParams = new URLSearchParams(window.location.search);
const queryParams = Object.fromEntries(_queryParams.entries());
console.log(queryParams);

let schema_url = queryParams.schema;


/*

var zipEngine = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace("navn"),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: "https://dawa.aws.dk/postnumre/%QUERY",
    wildcard: "%QUERY",
    cache: true
  }
});
zipEngine.clearPrefetchCache();
zipEngine.clearRemoteCache();
zipEngine.initialize();
*/

/*
var nameEngine = new Bloodhound({
  local: ['dog', 'pig', 'moose'],
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  datumTokenizer: Bloodhound.tokenizers.whitespace
});
*/

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
let editor = new JSONEditor(form, options);


editor.on('ready', function() {
  /* download button */


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
});
