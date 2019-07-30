$(document).ready(function () {
    $("#info").click(function () {
        $("#content").load("/info");
    });
});