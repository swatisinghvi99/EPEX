// here we read the projects information and then update the various HTML elements
// first we read the email info
// next the commit info
// project information
// this provides commit stats , email stats and project information details

function UpdateprojectInfo() {
  var this_project = document.getElementById("projectDropdown").value;
  var selected_repo = document.getElementById("repoDropdown").value;


  var curr_month = document.getElementById("Month").value;
  
  document.getElementById("pro_month1").innerHTML = curr_month;
  document.getElementById("pro_month").innerHTML = curr_month;

  // Fetch project information from new_about_data regardless of repo selection
  fetch(`./UPDATED_Data/new/new_about_data/${this_project.replace('/', '_')}.json`)
    .then(response => response.json())
    .then(project_info => {
      Actual_change(project_info, null, null);
      const jsonFilePath = `./UPDATED_Data/new/new_month_intervals/${selected_repo}.json`;

      // If a repo is selected, also fetch date intervals from new_month_intervals
      if (selected_repo) {
        return fetch(jsonFilePath)
          .then(response => response.json())
          .then(to_from_info => {
            var to_dates = to_from_info[curr_month];
            updateSliderMax(jsonFilePath); // Update the slider max based on the number of months in JSON data
            Actual_change(project_info, to_dates, to_from_info); 
            return; 
          });
      }
      // If no repo is selected, just update the project info without repo-specific details
      Actual_change(project_info, null, null);
    })
    .catch(error => console.error('Error fetching project or date interval info:', error));
}


function updateSliderMax(jsonFilePath) {
  fetch(jsonFilePath)
    .then(response => response.json())
    .then(data => {
      const numberOfMonths = Object.keys(data).length;
      const slider = document.getElementById("MaxIncubation");
      slider.max = numberOfMonths;
      
    })
    .catch(error => console.error('Error updating slider max:', error));
}

// function Actual_change(email_info, commit_info, project_info, to_dates) {
function Actual_change(project_info, to_dates, to_from_info) {
  document.getElementById("link").innerHTML = `<a href="${project_info.project_url}" target="_blank">${project_info.project_name}</a>`;
  document.getElementById("status").innerHTML = project_info.status;
  
  if (to_dates && to_from_info) {
    // Set start and end dates by finding the earliest and latest dates from to_from_info
    var all_dates = Object.values(to_from_info).reduce((acc, val) => acc.concat(val), []);
    var start_date = all_dates[0]; 
    var end_date = all_dates[all_dates.length - 1];
  
    document.getElementById("start1").innerHTML = start_date;
    document.getElementById("end1").innerHTML = end_date;
    document.getElementById("from").innerHTML = to_dates[0];
    document.getElementById("to").innerHTML = to_dates[1];
    document.getElementById("reports_month").innerHTML = `${to_dates[0]}~${to_dates[1]}`;
    document.getElementById("month_period_start").innerHTML = start_date;
    document.getElementById("month_period_end").innerHTML = end_date;
  } else {
    document.getElementById("start1").innerHTML = '';
    document.getElementById("end1").innerHTML = '';
    document.getElementById("from").innerHTML = '';
    document.getElementById("to").innerHTML = '';
    document.getElementById("reports_month").innerHTML = '';
    document.getElementById("month_period_start").innerHTML = '';
    document.getElementById("month_period_end").innerHTML = '';
  }

  document.getElementById("tech").innerHTML = project_info.tech;
  // document.getElementById("num_emails").innerHTML = Math.floor(
  //   email_info.num_emails
  // );

  // document.getElementById("num_senders").innerHTML = Math.floor(
  //   email_info.num_senders.toFixed(2)
  // );
  // document.getElementById("email_per_dev").innerHTML = Math.floor(
  //   email_info.email_per_dev
  // );
  // document.getElementById("reports_month").innerHTML =
  //   project_info.start_date + "~" + project_info.end_date;

  // document.getElementById("num_commits").innerHTML = Math.floor(
  //   commit_info.num_commits
  // );s
  // document.getElementById("num_committers").innerHTML = Math.floor(
  //   commit_info.num_committers
  // );
  // document.getElementById("commit_per_dev").innerHTML = Math.floor(
  //   commit_info.commit_per_dev
  // );
  // document.getElementById("mentor").innerHTML = project_info.mentor;

  // Process releases if present
  var releases = project_info.releases;
  var repoLinkElement = document.getElementById('repo_link');

  if (releases && releases.length > 0) {
      repoLinkElement.innerHTML = '';
      var fragment = document.createDocumentFragment();

      releases.forEach(function(release, index) {
          var link = document.createElement('a');
          link.href = release.url;
          link.textContent = release.name + ' (' + release.date + ')';
          link.target = '_blank';

          fragment.appendChild(link);
          if (index < releases.length - 1) {
              fragment.appendChild(document.createTextNode(', '));
          }
      });

      repoLinkElement.appendChild(fragment);
  } else {
      // Handle case with no releases
      repoLinkElement.textContent = 'No releases';
  }

  document.getElementById("pro_title").innerHTML = project_info.project_name;
  document.getElementById("pro_title1").innerHTML = project_info.project_name;
  document.getElementById("pro_title2").innerHTML = project_info.project_name;
  
}

document.addEventListener('DOMContentLoaded', function() {
  if (typeof populateRepoDropdown === 'function') {
    document.getElementById('projectDropdown').addEventListener('change', function() {
      populateRepoDropdown();
    });
  }

  if (typeof UpdateprojectInfo === 'function') {
    document.getElementById('repoDropdown').addEventListener('change', function() {
      UpdateprojectInfo();
    });
  }
});