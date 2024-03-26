function make_chart_alt() {
  var this_project = document.getElementById("repoDropdown").value;
  // we have stored the name_to_id conversion in order to convert the project name to ids
  // console.log(ids)
  // get which projects folder we need to access
  var link =
    "./UPDATED_Data/new/new_forecast/" +
    this_project +
    "_" +
    "f_data.csv";

  console.log(link);
  d3.select("#my_dataviz").html(null);

  draw1(link);
}

function draw1(link) {
  // set the dimensions and margins of the graph

  var margin = { top: 20, right: 20, bottom: 20, left: 65 },
    width = 900 - margin.left - margin.right,
    height = 130 - margin.top - margin.bottom;

  // bisector
  var bisectDate = d3.bisector(function (d) {
    return d.date;
  }).left;

  // set the ranges
  var x = d3.scaleLinear().range([0, width]);
  var y = d3.scaleLinear().range([height, 0]);

  // define the area
  var area = d3
    .area()
    .x(function (d) {
      return x(d.date);
    })
    .y0(height)
    .y1(function (d) {
      return y(d.close);
    });

  // define the line
  var valueline = d3
    .line()
    .x(function (d) {
      return x(d.date);
    })
    .y(function (d) {
      return y(d.close);
    });

  // append the svg obgect to the body of the page
  // appends a 'group' element to 'svg'
  // moves the 'group' element to the top left margin
  const f = d3.format(".1f");
  var svg = d3
    .select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var lineSvg = svg.append("g");
  var focus = svg
    .append("g") // **********
    .style("display", "none");
  //

  var new_paths = `${link}`;
  // get the data
  d3.csv(new_paths, function (error, data) {
    if (error) throw error;

    // format the data
    data.forEach(function (d) {
      d.date = +d.date;
      d.close = +d.close;
    });

    // scale the range of the data
    x.domain(
      d3.extent(data, function (d) {
        return d.date;
      })
    );
    y.domain([
      0,
      d3.max(data, function (d) {
        return d.close;
      }),
    ]);

    // Add the valueline path.
    lineSvg
      .append("path") // **********
      .attr("class", "line")
      .attr("d", valueline(data));

    // add the area
    svg.append("path").data([data]).attr("class", "area").attr("d", area);

    // add the valueline path.
    svg.append("path").data([data]).attr("class", "line").attr("d", valueline);

    // add the X Axis and Y axis

    svg
      .append("g")
      // .attr("class", "axis")
      .attr("class", "forecast")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).ticks(15))
      .style("stroke-width", "0.7px")
      // .style("fill", "white")
      // .style("stroke", "white")
      .selectAll("text")
      .attr("class", "forecast")
      .style("text-anchor", "end")
      .attr("dx", "-.1em")
      .attr("dy", "0.5em");
    // .style("fill", "white");
    // .attr("transform", "rotate(-45)");

    // Add the y Axis
    svg
      .append("g")
      .attr("class", "forecast")
      .style("stroke-width", "0.5px")
      // .style("fill", "black")
      // .style("stroke", "black")
      .call(d3.axisLeft(y).ticks(5))
      .selectAll("text")
      .attr("class", "forecast")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.1em");
    // .attr("transform", "rotate(-45)");

    svg
      .append("text")
      .attr(
        "transform",
        "translate(" + width / 2 + " ," + (height + margin.top + 11) + ")"
      )
      .style("text-anchor", "middle");

    //   y axis label
    svg
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x", 0 - height / 2)
      .attr("dy", "1em")
      .attr("fill", "black")
      .style("font", "10px ")
      .style("text-anchor", "middle")
      .text("Forecast Value");

    // x axis

    svg
      .append("text")
      .attr("x", width - 50)
      .attr("y", height - 12)
      .attr("dx", "1em")
      .attr("fill", "yellow")
      .style("font", "10px ")
      .style("text-anchor", "middle")
      .text("Months");

    focus
      .append("line")
      .attr("class", "x")
      .style("stroke", "salmon")
      .style("stroke-dasharray", "3,3")
      .style("opacity", 0.5)
      .attr("y1", 0)
      .attr("y2", height);

    // append the y line
    focus
      .append("line")
      .attr("class", "y")
      .style("stroke", "salmon")
      .style("stroke-dasharray", "3,3")
      .style("opacity", 0.7)
      .attr("x1", width)
      .attr("x2", width);

    focus
      .append("circle") // **********
      .attr("class", "y") // **********
      .style("fill", "green") // **********
      .style("stroke", "black") // **********
      .attr("r", 8); // **********

    // append the rectangle to capture mouse               // **********
    svg
      .append("rect") // **********
      .attr("width", width) // **********
      .attr("height", height) // **********
      .style("fill", "none") // **********
      .style("pointer-events", "all") // **********
      // .on("mouseover", function() { focus.style("display", null); })
      // .on("mouseout", function() { focus.style("display", "none"); })
      .on("mousemove", mousemove);
    // **********

    focus
      .append("text")
      .attr("class", "y2")
      .attr("dx", 8)
      .style("fill", "black")
      .attr("dy", "0em");

    focus
      .append("text")
      .attr("class", "y4")
      .style("fill", "black")
      .attr("dx", 8)
      .attr("dy", "2em");

    svg
      .append("rect")
      .attr("width", width)
      .attr("height", height)
      .style("fill", "none")
      .style("pointer-events", "all")
      .on("mouseover", function () {
        focus.style("display", null);
      })
      .on("mouseout", function () {
        focus.style("display", "none");
      })
      .on("click", mouseclick)
      .on("mousemove", mousemove);

    function mouseclick() {
      var x0 = x.invert(d3.mouse(this)[0]),
        i = bisectDate(data, x0, 1),
        d0 = data[i - 1],
        d1 = data[i],
        d = x0 - d0.date > d1.date - x0 ? d1 : d0;
    }

    function mousemove() {
      var x0 = x.invert(d3.mouse(this)[0]),
        i = bisectDate(data, x0, 1),
        d0 = data[i - 1],
        d1 = data[i],
        d = x0 - d0.date > d1.date - x0 ? d1 : d0;
      // console.log(x0);

      focus
        .select("circle.y")
        .attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")");

      focus
        .select("text.y1")
        .attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")")
        .text(f(d.close));

      focus
        .select("text.y2")
        .attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")")
        .text(f(d.close));

      // for the motnhs text
      focus
        .select("text.y3")
        .attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")")
        // .text(formatDate(d.date));
        .text(d.date);
      // for the motnhs text
      focus
        .select("text.y4")
        .attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")")
        // .text(formatDate(d.date));
        .text(d.date);

      focus
        .select(".x")
        .attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")")
        .attr("y2", height - y(d.close));

      focus
        .select(".y")
        .attr("transform", "translate(" + width * -1 + "," + y(d.close) + ")")
        .attr("x2", width + width);
    } // **********
    //  red dot
    var data1 = [data[0]];
    var theCircle1 = svg
      .append("circle")
      .data(data1)
      .attr("cx", function (d) {
        return x(d.date);
      })
      .attr("cy", function (d) {
        return y(d.close);
      })
      .attr("stroke", "black")
      .style("fill", "purple")
      .attr("r", 7);
    var theCircle2 = svg
      .append("circle")
      .data(data1)
      .attr("cx", function (d) {
        return x(d.date);
      })
      .attr("cy", function (d) {
        return y(d.close);
      })
      .attr("stroke", "black")
      .style("fill", "yellow")
      .attr("r", 7);
    var x0 = 0,
      i = bisectDate(data, x0, 1),
      d0 = data[i - 1],
      d1 = data[i],
      d = x0 - d0.date > d1.date - x0 ? d1 : d0;
    // console.log(x0);

    var the_line = svg
      .append("line")
      // .select(".x")
      .style("stroke-dasharray", "5,5") //dashed array for line
      .style("stroke", "steelblue")
      .attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")")
      .attr("y2", height - y(d.close));

    function changeSize4b(b_value) {
      var data2 = [data[b_value - 1]];
      theCircle2
        .data(data2)
        // .transition()
        // .duration(400)
        .attr("cx", function (d) {
          return x(d.date);
        })
        .attr("cy", function (d) {
          return y(d.close);
        });
    }

    function changeSize4(b_value) {
      var data2 = [data[b_value - 1]];
      theCircle1
        .data(data2)
        // .transition()
        // .duration(400)
        .attr("cx", function (d) {
          return x(d.date);
        })
        .attr("cy", function (d) {
          return y(d.close);
        });
    }

    html5Slider.noUiSlider.on("update", function (values, handle) {
      var value = values[handle];
      if (handle) {
        // inputNumber.value = value;
        changeSize4(value);
      } else {
        b_value1 = Math.round(value);
        changeSize4b(b_value1);
      }
    });
  });
}
