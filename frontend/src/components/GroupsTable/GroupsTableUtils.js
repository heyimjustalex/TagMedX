import { Chip } from '@nextui-org/react';

import { get } from '../../utils/fetch';
import { NextColorMap } from '../../consts/NextColorMap';
import { NextColor } from '../../consts/NextColor';

export function renderCell(item, columnKey) {
  const cellValue = item[columnKey];
  switch (columnKey) {
    case 'role':
      return (
        <Chip className='capitalize' color={NextColorMap[item.status]} size='sm' variant='flat'>
          {cellValue}
        </Chip>
      );
    default:
      return cellValue;
  }
}

export async function getGroups(setData, notification) {
  const res = await get('groups');
  if(res.ok) setData({ elements: res.body, ready: true });
  else notification.make(NextColor.DANGER, 'Error', 'Could not load groups.');
}