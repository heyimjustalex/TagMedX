import { Chip, Tooltip, User } from '@nextui-org/react';
import { IconTrash } from '@tabler/icons-react';

import { NextColorMap } from '../../../consts/NextColorMap';
import { NextColor } from '../../../consts/NextColor';
import { del } from '../../../utils/fetch';

export function renderCell(item, columnKey, setModal) {
  
  const cellValue = item[columnKey];

  switch (columnKey) {
    case 'name':
      return (
        <User
          avatarProps={{
            radius: 'lg',
            fallback: `${cellValue[0]}${item.surname[0]}`,
            color: NextColorMap[(cellValue.codePointAt(0) + item.surname.codePointAt(0)) % 5 + 1]
          }}
          description={item.e_mail}
          name={`${item.title || ''} ${cellValue} ${item.surname}`}
        >
          {item.email}
        </User>
      );
    case 'role':
      return (
        <Chip className='capitalize' color={NextColorMap[item.role.toLowerCase()]} size='sm' variant='flat'>
          {cellValue}
        </Chip>
      );
    case 'action':
      return (
        <div className="relative flex justify-end items-center gap-2">
        {
          item.role === 'Admin'
          ? <Tooltip content="Cannot remove admin" placement='left-start'>
              <span className="text-lg text-default cursor-pointer active:opacity-50">
                <IconTrash />
              </span>
          </Tooltip>
          : <Tooltip color="danger" content="Remove user" placement='left-start'>
            <span className="text-lg text-danger cursor-pointer active:opacity-50">
              <IconTrash onClick={() => setModal({ open: true, user: item })} />
            </span>
          </Tooltip>
        }
        </div>
      );
    case 'practice_start_year':
      return cellValue ? new Date().getFullYear() - parseInt(cellValue) : 0;
    default:
      return cellValue;
  }
}

export async function removeUser(user, groupId, setModal, setSent, setData, notification) {
  setSent(true);
  const res = await del(`groups/${groupId}/user/${user?.user_id}`);
  if(res.ok) {
    setData(prev => ({ ...prev, users: prev.users.filter(e => e.user_id !== user.user_id)}));
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.SUCCESS, 'User removed', `You have successfully removed ${user.name} ${user.surname} from the group.`);
  }
  else {
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.DANGER, 'Error', `Could not remove ${user.name} ${user.surname} from the group.`);
  }
}