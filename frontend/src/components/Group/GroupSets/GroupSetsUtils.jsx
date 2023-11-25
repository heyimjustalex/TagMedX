import { Chip } from '@nextui-org/react';

import { post } from '../../../utils/fetch';
import { NextColorMap } from '../../../consts/NextColorMap';
import { NextColor } from '../../../consts/NextColor';

export function renderCell(item, columnKey) {
  const cellValue = item[columnKey];
  switch (columnKey) {
    case 'type':
      return (
        <Chip className='capitalize' color={NextColorMap[item.type.toLowerCase()]} size='sm' variant='flat'>
          {cellValue}
        </Chip>
      );
    default:
      return cellValue;
  }
}

export function checkPackageSize(size) {
  return Boolean(size) &&
  !isNaN(parseInt(size)) &&
  (parseInt(size) < 10 ||
  parseInt(size) > 100)
}

export async function addSet(values, setSent, onClose, setData, groupId, notification) {
  setSent(true);
  const res = await post('sets/create',
    {
      id_group: groupId,
      name: values.name,
      type: values.type.values().next().value,
      description: values.description,
      package_size: values.packageSize
    }
  );

  if(res.ok) {
    setData(prev => ({ ...prev, sets: [...prev.sets, res.body]}));
    setSent(false);
    onClose();
    notification.make(NextColor.SUCCESS, 'Set created', `You have successfully created ${res.body.name}.`);
  }
  else {
    setSent(false);
    onClose();
    notification.make(NextColor.DANGER, 'Error', 'Could not create new set.');
  }
}