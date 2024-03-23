var d = {}; // This will be populated with the data from project_names.json

// Populate the technology dropdown
function populateTechnologyDropdown() {
  var technologyDropdown = document.getElementById('technologyDropdown');
  technologyDropdown.innerHTML = '';

  var defaultOption = document.createElement('option');
  defaultOption.textContent = 'Select Technology';
  defaultOption.disabled = true;
  defaultOption.selected = true;
  technologyDropdown.appendChild(defaultOption);

  for (var technology in d) {
    var option = document.createElement('option');
    option.value = technology;
    option.textContent = technology;
    technologyDropdown.appendChild(option);
  }
}

// Populate the project dropdown based on selected technology
function populateProjectDropdown() {
  var projectDropdown = document.getElementById('projectDropdown');
  var technologyDropdown = document.getElementById('technologyDropdown');
  var selectedTechnology = technologyDropdown.value;
  projectDropdown.innerHTML = '';

  var defaultOption = document.createElement('option');
  defaultOption.textContent = 'Select Project';
  defaultOption.disabled = true;
  defaultOption.selected = true;
  projectDropdown.appendChild(defaultOption);

  if (selectedTechnology && d[selectedTechnology]) {
    Object.keys(d[selectedTechnology]).forEach(function(projectName) {
      var option = document.createElement('option');
      option.value = projectName;
      option.textContent = projectName;
      projectDropdown.appendChild(option);
    });
  }
}

// Populate the repository dropdown based on selected project
function populateRepoDropdown() {
  var repoDropdown = document.getElementById('repoDropdown');
  var technologyDropdown = document.getElementById('technologyDropdown');
  var projectDropdown = document.getElementById('projectDropdown');
  var selectedTechnology = technologyDropdown.value;
  var selectedProject = projectDropdown.value;
  repoDropdown.innerHTML = '';

  if (selectedTechnology && selectedProject && d[selectedTechnology][selectedProject]) {
    d[selectedTechnology][selectedProject].forEach(function(repo) {
      var option = document.createElement('option');
      option.value = repo;
      option.textContent = repo;
      repoDropdown.appendChild(option);
    });
  }
}

// Modify the filter function to filter project names only
function filterProjectDropdown() {
  var input, filter, options, i;
  input = document.getElementById('searchInput');
  filter = input.value.toUpperCase();
  options = document.getElementById('projectDropdown').getElementsByTagName('option');

  for (i = 0; i < options.length; i++) {
    var txtValue = options[i].textContent || options[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      options[i].style.display = "";
    } else {
      options[i].style.display = "none";
    }
  }
}

// Adjust the loadProjectNames function to also populate the technology dropdown
function loadProjectNames() {
  fetch('project_names.json')
    .then(response => response.json())
    .then(data => {
      d = data;
      populateTechnologyDropdown();
    })
    .catch(error => console.error('Error loading the project names:', error));
}

document.addEventListener('DOMContentLoaded', function() {
  loadProjectNames();
});
