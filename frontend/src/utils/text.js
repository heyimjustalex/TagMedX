export function generateRandomString(length) {
  let randomString = '';

  for (let i = 0; i < length; i++) {
    const randomCharCode = Math.floor(Math.random() * (126 - 33 + 1) + 33);
    randomString += String.fromCharCode(randomCharCode);
  }

  return randomString;
}

export function capitalize(text) {
  if(text) return text.charAt(0).toUpperCase() + text.slice(1);
  else return '';
}