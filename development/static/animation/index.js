setTimeout(function () {
  $('.inner div').addClass('done');
  setTimeout(function () {
    $('.inner div').addClass('page');
    setTimeout(function () {
      $('.pageLoad').addClass('off');
      $('body, html').addClass('on');
    }, 500)
  }, 500)
}, 1500)