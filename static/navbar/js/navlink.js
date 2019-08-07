$(document).ready(function () {
    $("#info").click(function () {
        $("#content").load("/info");
    });

    $("#evernote").click(function () {
        $("#content").load("/notebook");
    });

    $("#collection_movieline").click(function () {
        $("#content").load("/c1_movieline");
    });

});

