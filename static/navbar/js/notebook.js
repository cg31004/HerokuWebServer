$(document).ready(function () {
    $("#evernote").click(function () {
        $("#content").load("/notebook");
    });
});