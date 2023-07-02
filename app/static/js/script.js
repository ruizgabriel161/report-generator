$(document).ready(function() {
    var eventSource = new EventSource('/status');

    eventSource.onmessage = function(event) {
        var status = event.data;
        $('#status').text(status);
    };
});