import { Chip, Tooltip } from '@nextui-org/react';
import { IconEdit, IconTrash } from '@tabler/icons-react';

import { del, post, put } from '../../../utils/fetch';
import { NextColorMap } from '../../../consts/NextColorMap';
import { NextColor } from '../../../consts/NextColor';

export function renderCell(item, columnKey, setModal, setRemoveModal) {
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
          <Tooltip content="Edit set" placement='top-end'>
            <span className="text-lg text-default-600 cursor-pointer active:opacity-50">
              <IconEdit onClick={
                () => setModal({
                  open: true,
                  edit: true,
                  id: item.id,
                  name: item.name,
                  type: new Set().add(item.type),
                  description: item.description,
                  packageSize: item.package_size
                })}
              />
            </span>
          </Tooltip>
          <Tooltip color="danger" content="Remove set" placement='top-end'>
            <span className="text-lg text-danger cursor-pointer active:opacity-50">
              <IconTrash onClick={() => setRemoveModal({ open: true, id: item.id, name: item.name })} />
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

export async function addSet(modal, setSent, setModal, setData, groupId, notification) {
  setSent(true);
  const res = await post('sets',
    {
      id_group: groupId,
      name: modal.name,
      type: modal.type.values().next().value,
      description: modal.description,
      package_size: modal.packageSize
    }
  );

  if(res.ok) {
    setData(prev => ({ ...prev, sets: [...prev.sets, res.body]}));
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.SUCCESS, 'Set created', `You have successfully created ${res.body.name}.`);
  }
  else {
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.DANGER, 'Error', 'Could not create new set.');
  }
}

export async function editSet(modal, setSent, setModal, setData, groupId, notification) {
  setSent(true);
  const res = await put(`sets/${modal.id}`,
    {
      id_group: groupId,
      name: modal.name,
      type: modal.type.values().next().value,
      description: modal.description,
      package_size: modal.packageSize
    }
  );

  if(res.ok) {
    setData(prev => ({
      ...prev,
      sets: prev.sets.map(e => {
        if(e.id === modal.id) return res.body;
        else return e;
      })
    }));
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.SUCCESS, 'Set saved', `You have successfully saved changes in ${res.body.name}.`);
  }
  else {
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.DANGER, 'Error', `Could not save changes in ${res.body.name}.`);
  }
}

export async function removeSet(id, setModal, setSent, setData, notification) {
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