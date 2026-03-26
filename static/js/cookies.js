// Simple cookie consent manager
(function () {
  var COOKIE_NAME = 'gur_cookie_consent';
  var ONE_YEAR = 365 * 24 * 60 * 60; // seconds

  function getCookie(name) {
    return document.cookie.split('; ').find(function (row) {
      return row.startsWith(name + '=');
    });
  }

  function setCookie(name, value, maxAgeSeconds) {
    var parts = [
      name + '=' + encodeURIComponent(value),
      'path=/',
      'Max-Age=' + maxAgeSeconds,
      'SameSite=Lax'
    ];
    // Avoid setting Secure on http to prevent it being ignored in dev
    if (location.protocol === 'https:') parts.push('Secure');
    document.cookie = parts.join('; ');
  }

  function showBanner() {
    var banner = document.getElementById('cookie-banner');
    if (!banner) return;
    banner.style.display = 'block';
  }

  function hideBanner() {
    var banner = document.getElementById('cookie-banner');
    if (!banner) return;
    banner.style.display = 'none';
  }

  function onAccept() {
    setCookie(COOKIE_NAME, 'true', ONE_YEAR);
    hideBanner();
  }

  function init() {
    if (!getCookie(COOKIE_NAME)) {
      showBanner();
    }
    var acceptBtn = document.getElementById('cookie-accept');
    if (acceptBtn) acceptBtn.addEventListener('click', onAccept);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

