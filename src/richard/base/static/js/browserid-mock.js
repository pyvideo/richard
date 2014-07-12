// A replacement for the JS of django-browserid to be used when authentication
// with browserid is not possible (e.g. no internet connection available).
//
// What it does is calling directly into the server-side views with dummy data,
// this can only work when the server doesn't check credentials.

(function($) {
  'use strict';

  $(function() {

    $(document).on('click', '.browserid-login', function(e) {
      e.preventDefault();

      var loginRedirect = $(this).data('next');
      var loginForm = $('#browserid-form');
      loginForm.find('input[name="next"]').val(loginRedirect);
      loginForm.find('input[name="assertion"]').val("dummy");
      loginForm.submit();
    });

    $(document).on('click', '.browserid-logout', function(e) {
      e.preventDefault();

      window.location = $(this).attr('href');
    });

  });
})(jQuery);
