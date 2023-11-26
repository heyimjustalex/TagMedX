import { Chip, Tooltip } from '@nextui-org/react';
import { IconTrash } from '@tabler/icons-react';

import { del, post } from '../../../utils/fetch';
import { NextColorMap } from '../../../consts/NextColorMap';
import { NextColor } from '../../../consts/NextColor';

export function renderCell(item, columnKey, setModal) {
  const cellValue = item[columnKey];
  switch (columnKey) {
    case 'type':
      return (
        <Chip className='capitalize' color={NextColorMap[item.type.toLowerCase()]} size='sm' variant='flat'>
          {cellValue}
        </Chip>
      );
    case 'actions':
      return (
        <div className="relative flex justify-end items-center gap-2">
          <Tooltip color="danger" content="Remove set" placement='left-start'>
            <span className="text-lg text-danger cursor-pointer active:opacity-50">
              <IconTrash onClick={() => setModal({ open: true, id: item.id, name: item.name })} />
            </span>
          </Tooltip>
        </div>
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
  const res = await post('sets',
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

export async function removeSet(id, setSent, setModal, setData, notification) {
  setSent(true);
  const res = await del(`sets/${id}`);

  if(res.ok) {
    setData(prev => ({ ...prev, sets: prev.sets.filter(e => e.id !== id)}));
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.SUCCESS, 'Set removed', `You have successfully removed ${res.body.name}.`);
  }
  else {
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.DANGER, 'Error', 'Could not remove set.');
  }
}