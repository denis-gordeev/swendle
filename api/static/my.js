function get_random_color() {
    var letters = '0123456789'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.round(Math.random() * 9)];
    }
    return color;
}

$("div.content.fg-dark.clear-float.color").each(function() {
    $(this).css("background-color", get_random_color());
});