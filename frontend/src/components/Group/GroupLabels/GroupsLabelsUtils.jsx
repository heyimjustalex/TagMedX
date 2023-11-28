import { Chip } from '@nextui-org/react';

import { NextColorMap } from '../../../consts/NextColorMap';

export function renderCell(item, columnKey) {
  const cellValue = item[columnKey];
  switch (columnKey) {
    case 'role':
      return (
        <Chip className='capitalize' color={NextColorMap[item.role.toLowerCase()] || 'default'} size='sm' variant='flat'>
          {cellValue || ''}
        </Chip>
      );
    default:
      return cellValue;
  }
}