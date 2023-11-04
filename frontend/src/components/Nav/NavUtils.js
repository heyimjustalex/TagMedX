import { deleteCookie } from '../../utils/cookie';
import { NextColor } from '../../consts/NextColor';

export function handleLogout(setUserId, router, notification) {
  notification.make(NextColor.SUCCESS, 'Logout', 'You have successfully log out.');
  setUserId(false);
  deleteCookie('token');
  router.push('/');
}