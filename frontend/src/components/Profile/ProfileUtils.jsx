export function checkInitYear(year) {
  return year &&
  !isNaN(parseInt(year)) &&
  (parseInt(year) < 1900 ||
  parseInt(year) > new Date().getFullYear())
}

export function compareChanges(user, newUser) {
  return (
    user.title === newUser.title &&
    user.name === newUser.name &&
    user.surname === newUser.surname &&
    user.e_mail === newUser.e_mail &&
    user.specialization === newUser.specialization &&
    user.practice_start_year === newUser.practice_start_year
  )
}