$(document).ready(function () {
    $(".content-section-text").mousemove(function (e) {
        var hoverText = $(this).find(".hover-text");
        var textWidth = hoverText.width();
        var textHeight = hoverText.height();
        var mouseX = e.pageX - $(this).offset().left;
        var mouseY = e.pageY - $(this).offset().top;

        // Calculate the position of the hover text
        var posX = mouseX + textWidth / 1.5;
        var posY = mouseY - textHeight / 1.2;

        // Update the position of the hover text
        hoverText.css({
            left: posX,
            top: posY
        });
    });
});