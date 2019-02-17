$(".open").click(function () {
    console.log("0");
    var container = $(this).parents(".topic");
    var answer = container.find(".answer");
    var trigger = container.find(".faq-t");

    answer.slideToggle(200);

    if (trigger.hasClass("faq-o")) {
        console.log("1");
        trigger.removeClass("faq-o");
    }
    else {
        console.log("2");
        trigger.addClass("faq-o");
    }

    if (container.hasClass("expanded")) {
        console.log("3");
        container.removeClass("expanded");
    }
    else {
        console.log("4");
        container.addClass("expanded");
    }
});


jQuery(document).ready(function ($) {
    $('.question').each(function () {
        $(this).attr('data-search-term', $(this).text().toLowerCase() + $(this).find("ptag").text().toLowerCase());

    });

    $('.live-search-box').on('keyup', function () {

        var searchTerm = $(this).val().toLowerCase();

        $('.question').each(function () {

            if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) {
                $(this).parent().parent().show();
            } else {
                $(this).parent().parent().hide();
            }

        });

    });

});