import { Chip, Tooltip, User } from '@nextui-org/react';
import { IconTrash } from '@tabler/icons-react';

import { NextColorMap } from '../../../consts/NextColorMap';

export function renderCell(item, columnKey) {
  const cellValue = item[columnKey];
  switch (columnKey) {
    case 'name':
      return (
        <User
          avatarProps={{
            radius: 'lg',
            fallback: `${cellValue[0]}${item.surname[0]}`,
            color: NextColorMap[(cellValue.codePointAt(0) + item.surname.codePointAt(0)) % 6]
          }}
          description={item.email}
          name={`${cellValue} ${item.surname}`}
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
          <Tooltip color="danger" content="Delete user">
            <span className="text-lg text-danger cursor-pointer active:opacity-50">
              <IconTrash />
            </span>
          </Tooltip>
        </div>
      );
    default:
      return cellValue;
  }
}