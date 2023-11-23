import { put } from '../../utils/fetch';
import { NextColor } from '../../consts/NextColor';

export async function handleSaveUser(user, setSent, setUser, notification) {
  setSent(true);
  
  const res = await put('users/update', { 
    e_mail: user.e_mail,
    name: user.name,
    surname: user.surname,
    title: user.title,
    specialization: user.specialization,
    practice_start_year: user.practice_start_year
  });

  if(res.ok) {
    setUser({ ...res.body });
    setSent(false);
    notification.make(NextColor.SUCCESS, 'User saved', 'You have successfully saved your settings.');
  }
  else {
    setSent(false);
    notification.make(NextColor.DANGER, 'User error', 'Could not save user settings.');
  }
}

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