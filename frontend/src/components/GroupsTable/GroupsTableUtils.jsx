import { Chip } from '@nextui-org/react';

import { get, post } from '../../utils/fetch';
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

export async function addGroup(name, setSent, onClose, setData, notification) {
  setSent(true);
  const res = await post('groups/join', { name: name });
  if(res.ok) {
    setData(prev => { return { elements: [res.body, ...prev.elements], ready: true }});
    setSent(false);
    onClose();
    notification.make(NextColor.DANGER, 'Group created', `You have successfully created ${res.body.name}.`);
  }
  else {
    setSent(false);
    onClose();
    notification.make(NextColor.DANGER, 'Error', 'Could not add new group.');
  }
}

export async function joinGroup(connectionString, setSent, onClose, setData, notification) {
  setSent(true);
  const res = await post('groups/join', { connection_string: connectionString });
  if(res.ok) {
    setData(prev => { return { elements: [res.body, ...prev.elements], ready: true }});
    setSent(false);
    onClose();
    notification.make(NextColor.DANGER, 'Joined group', `You have successfully join to ${res.body.name}`);
  }
  else {
    setSent(false);
    onClose();
    notification.make(NextColor.DANGER, 'Error', 'Could not join to group.');
  }
}