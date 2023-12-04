import { Chip, Tooltip } from '@nextui-org/react';
import { IconEdit, IconTrash } from '@tabler/icons-react';

import { del, post, put } from '../../../utils/fetch';
import { NextColor } from '../../../consts/NextColor';

export function renderCell(item, columnKey, setModal, setRemoveModal) {
  const cellValue = item[columnKey];
  switch (columnKey) {
    case 'color':
      return (
        <Chip className='capitalize' size='sm' variant='flat' classNames={{
          base: cellValue ? `bg-${cellValue}-100` : 'bg-zinc-200',
          content: cellValue ? `text-${cellValue}-500` : 'text-zinc-600'
        }}
        >
          {cellValue || 'default'}
        </Chip>
      );
    case 'actions':
      return (
        <div className='relative flex justify-end items-center gap-2'>
          <Tooltip content='Edit label' placement='top-end'>
            <span className='text-lg text-default-600 cursor-pointer active:opacity-50'>
              <IconEdit onClick={
                () => setModal({
                  open: true,
                  edit: true,
                  ...item,
                  color: new Set().add(item.color ? item.color : 'default')
                })}
              />
            </span>
          </Tooltip>
          <Tooltip color='danger' content='Remove label' placement='top-end'>
            <span className='text-lg text-danger cursor-pointer active:opacity-50'>
              <IconTrash onClick={() => setRemoveModal({ open: true, ...item })} />
            </span>
          </Tooltip>
        </div>
      );
    default:
      return cellValue;
  }
}

export async function addLabel(modal, setSent, setModal, setData, setId, notification) {
  setSent(true);
  const res = await post('labels',
    {
      id_set: setId,
      name: modal.name,
      description: modal.description,
      color: modal.color.values().next().value || null
    }
  );

  if(res.ok) {
    setData(prev => ({ ...prev, labels: [...prev.labels, res.body]}));
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.SUCCESS, 'Label created', `You have successfully created ${res.body.name} label.`);
  }
  else {
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.DANGER, 'Error', 'Could not create new label.');
  }
}

export async function editLabel(modal, setSent, setModal, setData, notification) {
  setSent(true);
  const res = await put(`labels/${modal.id}`,
    {
      name: modal.name,
      description: modal.description,
      color: modal.color.values().next().value || null
    }
  );

  if(res.ok) {
    setData(prev => ({
      ...prev,
      labels: prev.labels.map(e => {
        if(e.id === modal.id) return res.body;
        else return e;
      })
    }));
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.SUCCESS, 'Label saved', `You have successfully saved ${res.body.name} label.`);
  }
  else {
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.DANGER, 'Error', `Could not save ${res.body.name} label.`);
  }
}

export async function removeLabel(id, setModal, setSent, setData, notification) {
  setSent(true);
  const res = await del(`labels/${id}`);

  if(res.ok) {
    setData(prev => ({ ...prev, labels: prev.labels.filter(e => e.id !== id)}));
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.SUCCESS, 'Set removed', `You have successfully removed ${res.body.name} label.`);
  }
  else {
    setSent(false);
    setModal(prev => ({ ...prev, open: false }));
    notification.make(NextColor.DANGER, 'Error', 'Could not remove label.');
  }
}