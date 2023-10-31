function getCookie(name) {
  if (typeof document === 'undefined') return null;
  var value = '; ' + document?.cookie;
  var parts = value.split('; ' + name + '=');
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function deleteCookie(name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}


export { getCookie, deleteCookie }