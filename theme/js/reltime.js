
// Generates human-readable relative timestamps for <time> elements with a
// `data-makerel` attribute and displays them.
// A heavily modified version of the Timeago jQuery plugin (http://timeago.yarp.com/)

var reltime = function() {

  var templates = {
    suffixAgo: "ago",
    suffixFromNow: "from now",
    on: "on",

    seconds: "less than a minute",
    minute: "about a minute",
    minutes: "%d minutes",
    hour: "about an hour",
    hours: "%d hours",
    day: "about a day",
    days: "%d days",
    month: "about a month",
    months: "%d months",
    year: "about a year",
    years: "%d years",
  };

  function inWords(distanceMillis) {
    // Produce a string representing the milliseconds in a human-readable way

    var suffix = distanceMillis < 0 ? templates.suffixFromNow : templates.suffixAgo;
    var seconds = Math.abs(distanceMillis) / 1000;
    var minutes = seconds / 60;
    var hours = minutes / 60;
    var days = hours / 24;
    var years = days / 365;

    function substitute(string, number) {
      return string.replace(/%d/i, number);
    }

    var words =
      seconds < 45 && substitute(templates.seconds, Math.round(seconds)) ||
      seconds < 90 && substitute(templates.minute, 1) ||
      minutes < 45 && substitute(templates.minutes, Math.round(minutes)) ||
      minutes < 90 && substitute(templates.hour, 1) ||
      hours < 24 && substitute(templates.hours, Math.round(hours)) ||
      hours < 42 && substitute(templates.day, 1) ||
      days < 30 && substitute(templates.days, Math.round(days)) ||
      days < 45 && substitute(templates.month, 1) ||
      days < 365 && substitute(templates.months, Math.round(days / 30)) ||
      years < 1.5 && substitute(templates.year, 1) ||
      substitute(templates.years, Math.round(years));

    return words + " " + suffix;
  }

  function diff(timestamp) {
    // Get the number of milliseconds distance from the current time
    return Date.now() - timestamp;
  }

  function doReplace(){
    // Go over all <time> elements with a "data-makerel" attribute, grab the
    // datetime attribute, calculate and display a fuzzy representation of it,
    // then remove the data-makerel attrbute so it's not processed again.

    var times = document.getElementsByTagName("time");
    for (var i = 0; i < times.length; i++){

      if (!times[i].hasAttribute("data-reltime"))
        break;

      var datetime = times[i].getAttribute("datetime");
      if (!datetime)
        break;

      var parsed = new Date(datetime);
      if (!parsed)
        break;

      times[i].innerHTML = inWords(diff(parsed.getTime())) + " " + templates.on + " " + times[i].innerHTML;
      times[i].title = parsed.toLocaleString();
      times[i].removeAttribute("data-reltime");
    }
  }

  return doReplace;
}();
