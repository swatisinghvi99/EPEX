var d = {}; // This will be populated with the data from project_names.json

var categories = ["Automotive", "Digital Twin", "Cloud Development", "Eclipse Project", "EE4J", "Adoptium", "IoT", 
"LocationTech", "Modeling", "PolarSys", "RT", "SOA Platform", "Technology", "Tools", "Science", 
"Web Tools Platform", "AsciiDoc", "OpenHW Group", "Oniro"];

function populateCombinedDropdown() {
  var combinedDropdown = document.getElementById('txt_ide');
  combinedDropdown.innerHTML = ''; 

  var defaultOption = document.createElement('option');
  defaultOption.textContent = 'Select a project';
  defaultOption.disabled = true;
  defaultOption.selected = true;
  combinedDropdown.appendChild(defaultOption);

  for (var category in d) {
    var group = document.createElement('optgroup');
    group.label = category;

    d[category].forEach(function(product) {
      var option = document.createElement('option');
      option.value = product;
      option.textContent = product;
      group.appendChild(option);
    });

    combinedDropdown.appendChild(group);
  }
}

function filterDropdown() {
  var input, filter, optgroups, options, i, j, hasVisibleChildren;
  input = document.getElementById('searchInput');
  filter = input.value.toUpperCase();
  optgroups = document.getElementById('txt_ide').getElementsByTagName('optgroup');

  for (i = 0; i < optgroups.length; i++) {
    options = optgroups[i].getElementsByTagName('option');
    hasVisibleChildren = false;
    for (j = 0; j < options.length; j++) {
      if (options[j].textContent.toUpperCase().indexOf(filter) > -1) {
        options[j].style.display = "";
        hasVisibleChildren = true;
      } else {
        options[j].style.display = "none";
      }
    }
    optgroups[i].style.display = hasVisibleChildren ? "" : "none";
  }
}

// Load the project names from project_names.json
function loadProjectNames() {
  fetch('project_names.json')
    .then(response => response.json())
    .then(data => {
      d = data;
      populateCombinedDropdown();
    })
    .catch(error => console.error('Error loading the project names:', error));
}

document.addEventListener('DOMContentLoaded', function() {
  loadProjectNames();
});

document.getElementById('searchInput').addEventListener('keyup', filterDropdown);
