// here we read the projects information and then update the various HTML elements
// first we read the email info
// next the commit info
// project information
// this provides commit stats , email stats and project information details

function UpdateprojectInfo() {
  var this_project = document.getElementById("projectDropdown").value;
  
  console.log(this_project);
  var curr_month = document.getElementById("Month").value;

  // var new_file_path = alias_to_name[this_project] + "_" + curr_month;
  // set the months for the tech and social net
  document.getElementById("pro_month1").innerHTML = curr_month;
  document.getElementById("pro_month").innerHTML = curr_month;

  // try {
  //   email_info = JSON.parse(
  //     readTextFile(`./UPDATED_Data/new/email_measures/${new_file_path}.json`)
  //   );
  // } catch {}
  // try {
  //   commit_info = JSON.parse(
  //     readTextFile(`./UPDATED_Data/new/commits_measure/${new_file_path}.json`)
  //   );
  // } catch (err) {
  //   commit_info = {};
  //   commit_info.num_commits = 0;
  //   commit_info.num_committers = 0;
  //   commit_info.commit_per_dev = 0;
  // }
  project_info = JSON.parse(
    readTextFile(
      `./UPDATED_Data/new/new_about_data/${this_project}.json`
    )
  );

  to_from_info = JSON.parse(
    readTextFile(
      `./UPDATED_Data/new/new_month_intervals/aaspe.json`
    )
  );

  var to_dates = to_from_info[curr_month];
  Actual_change(project_info, to_dates);
}

// function Actual_change(email_info, commit_info, project_info, to_dates) {

function Actual_change(project_info, to_dates) {
  console.log(project_info)
  document.getElementById("link").innerHTML =
    '<a href="' +
    `${project_info.project_url}` +
    '" target="_blank" > ' +
    project_info.project_name +
    "</a>";
  document.getElementById("status").innerHTML = project_info.status;
  // document.getElementById("sponsor").innerHTML = project_info.sponsor;
  document.getElementById("start1").innerHTML = project_info.start_date;
  document.getElementById("end1").innerHTML = project_info.end_date;

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
  document.getElementById("tech").innerHTML = project_info.tech;
  var releases = project_info.releases;
  var repoLinkElement = document.getElementById('repo_link');

  if (releases.length > 0) {
      // Clear previous content
      repoLinkElement.innerHTML = '';

      // Create a document fragment to hold the links
      var fragment = document.createDocumentFragment();

      releases.forEach(function(release, index) {
          var link = document.createElement('a');
          link.href = release.url;
          link.textContent = release.name + ' (' + release.date + ')';
          link.target = '_blank';

          fragment.appendChild(link);

          // Add comma separator if not the last item
          if (index < releases.length - 1) {
              fragment.appendChild(document.createTextNode(', '));
          }
      });

      repoLinkElement.appendChild(fragment);
  } else {
      // Handle case with no releases or reviews
      repoLinkElement.textContent = 'No releases or reviews';
  }

  document.getElementById("from").innerHTML = to_dates[0];
  document.getElementById("to").innerHTML = to_dates[1];
  document.getElementById("reports_month").innerHTML =
    to_dates[0] + "~" + to_dates[1];

  document.getElementById("pro_title").innerHTML = project_info.project_name;
  document.getElementById("pro_title1").innerHTML = project_info.project_name;
  document.getElementById("pro_title2").innerHTML = project_info.project_name;
  // document.getElementById("month_period_start").innerHTML = project_info.start_date;
  // document.getElementById("month_period_end").innerHTML = project_info.end_date;
}

function email_aggregate(email_info) {
  document.getElementById("num_emails").innerHTML = Math.floor(
    email_info.num_emails
  );

  document.getElementById("num_senders").innerHTML = Math.floor(
    email_info.num_senders.toFixed(2)
  );
  document.getElementById("email_per_dev").innerHTML = Math.floor(
    email_info.email_per_dev
  );
}

function commit_aggregate(commit_info) {
  document.getElementById("num_commits").innerHTML = Math.floor(
    commit_info.num_commits
  );
  document.getElementById("num_committers").innerHTML = Math.floor(
    commit_info.num_committers
  );
  document.getElementById("commit_per_dev").innerHTML = Math.floor(
    commit_info.commit_per_dev
  );
}

$("#chk").prop("checked", false);
//
function UpdateMaxIncubation() {
  var slider = document.getElementById("MaxIncubation");

  slider.max = project_info.incubation_time;
  slider.min = 1;
  slider.value = slider.min;

  document.getElementById("Month").innerHTML =
    '<output id="Month">' + slider.min + "</output>";

  var max_time = parseInt(project_info.incubation_time);

  d3.csv(new_paths, function (error, data) {
    if (error) throw error;

    // format the data
    data.forEach(function (d) {
      d.date = +d.date;
      d.close = +d.close;
    });
    // set the incubation length
    document.getElementById("MaxIncubation").max = data.length;
  });
  console.log(data.length);
  updateSliderRange(1, data.length);
}
function update_month_id(the_current_month) {
  document.getElementById("Month").innerHTML = the_current_month;
}
