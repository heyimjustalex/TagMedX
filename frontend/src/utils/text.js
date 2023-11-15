export function generateRandomString(length) {
  let randomString = '';

  for (let i = 0; i < length; i++) {
    const randomCharCode = Math.floor(Math.random() * (126 - 33 + 1) + 33);
    randomString += String.fromCharCode(randomCharCode);
  }

  return randomString;
}

export function capitalize(word) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}