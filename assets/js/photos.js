$(document).ready(function() {
    $('#intro').css('min-height', $(window).height());
    $('#intro .dark-cover').height($('#intro').height());
    $('#intro .intro-text').css('top', $('#intro').height()/2.5 - $('#intro .intro-text').height()/2);
    $('#intro .dark-cover.fader').delay(200).animate({'opacity': 0}, 5000);

    $('#view-button').delay(3000).fadeTo(1000, 1);
    $('#view-button a').click(function(e) {
        e.preventDefault();
        $('html, body').animate({scrollTop: $("#intro").height()}, 1000);
    }).delay(3000).fadeTo(1000, 1);

    $('.yip-link').magnificPopup({
        type: 'image',
        image: {
            verticalFit: true,
            titleSrc: 'data-caption'
        },
        gallery:{enabled:true}
    });
});