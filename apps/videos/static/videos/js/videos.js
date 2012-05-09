// Parse the hash at the end of the URL and return it as object.
// Example: '#t=3m&foo=bar' returns {t: '3m', foo: 'bar'}
// TODO: error handling
function parseLocationHash() {
  var parts = window.location.hash.slice(1).split('&'),
	  result = {};

  for (var i = 0, length = parts.length; i < length; i++) {
	var tuple = parts[i].split('=');
	result[tuple[0]] = tuple[1];
  }

  return result;
}

// Parse time string and return the value in seconds.
// Example: '3m16s' returns 196
// TODO: error handling
function parseTime(value) {
  var time = 0;

  var minutes = value.split('m');
  var seconds = minutes.slice(-1)[0].split('s');

  time = minutes.length > 1 ? parseInt(minutes[0]) * 60 : 0;
  time += seconds.length > 1 ? parseInt(seconds[0]) : 0;

  return time;
}

// Seek to specified time in the video and start playing.
function UnisubsSeekVideo(time) {
  // We need to wait until the player is initialized before we can set
  // a time. This just checks every second if a certain global is
  // defined.
  // FIXME: this does not mean the player/video is ready! I hope we
  //        find a better way to do this.
  if (typeof(unisubs) === "undefined") {
	setTimeout(function() { UnisubsSeekVideo(time); }, 1000);
	return;
  }

  var w = unisubs.widget.Widget.getAllWidgets()[0];
  w.playAt(time);
}

// Seek to specified time in the video and start playing.
function HTML5SeekVideo(time) {
  var v = document.getElementsByTagName("video")[0];

  function waitForMetadata() {
    if (v.readyState >= 1) {
      v.currentTime = time;
      v.play();
	  return;
	}

    setTimeout(waitForMetadata, 500);
  }

  waitForMetadata();
}

function updateVideoOffset(embed_type) {
  if (embed_type === "undefined") {
    return;
  }

  var config = parseLocationHash();
  if (typeof(config.t) === "undefined") {
    return;
  }

  var time = parseTime(config.t);

  if (embed_type === "unisubs") {
    UnisubsSeekVideo(time);
  } else if (embed_type === "html5") {
    HTML5SeekVideo(time);
  }
}
