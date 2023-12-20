import { useEffect, useState } from 'react';
import { Button, Card, Checkbox, Chip, Divider, Select, SelectItem, Textarea } from '@nextui-org/react';
import { IconDeviceFloppy, IconTrash, IconX } from '@tabler/icons-react';

import './Editor.css';
import { RoleMap } from './EditorConsts';

export default function EditorDescriptor({ bbox, setBboxes, labels, examination, setExamination }) {

  const [label, setLabel] = useState(new Set());
  const [description, setDescription] = useState('');

  useEffect(() => {
    setLabel({ id: bbox?.label?.id || new Set(), color: bbox?.label?.color });
    setDescription(bbox?.description || '');
  }, [bbox]);

  return (
    <Card className='editor-descriptor'>
      <div className='flex w-full text-xs text-zinc-500'>Author</div>
      <div className='flex w-full text-small text-foreground'>
        <Chip size='sm' color={RoleMap[examination.role]} title={examination.role} variant='flat' className='mr-2'>
          {examination.role.charAt(0)}
        </Chip>
        {examination.user}
      </div>
      <Divider />
      <div className='flex w-full text-xs text-zinc-500'>Examination</div>
      <Checkbox
        value='tentative'
        size='sm'
        color='warning'
        isDisabled={!examination}
        isSelected={examination?.tentative}
        onValueChange={(e) => setExamination(prev => ({ ...prev, tentative: e }))}
      >
        Tentative
      </Checkbox>
      <Divider />
      <div className='flex w-full text-xs text-zinc-500'>BBox</div>
      <Select
        label='Label'
        items={labels}
        isDisabled={!bbox}
        selectionMode='single'
        selectedKeys={label.id}
        onSelectionChange={e => setLabel({
          id: e,
          color: e ? labels.find(label => label.id === parseInt(e.values().next().value))?.color : null
        })}
        renderValue={(items) => {
          return items.map((item) => <p key={item.key} className={item.props.className}>{item.textValue}</p>);
        }}
      >
        {labels?.map((label) => (
          <SelectItem key={label.id} value={label.id} className={`capitalize text-${label.color}-500`}>
            {label.name}
          </SelectItem>
        ))}
      </Select>
      <Textarea
        minRows={4}
        isDisabled={!bbox}
        label='Description'
        value={description}
        onChange={e => setDescription(e.target.value)}
      />
      <div className='flex justify-between'>
        <Button
          isIconOnly
          title='Delete'
          variant='light'
          className='flex'
          color='danger'
          isDisabled={!bbox}
          onPress={() => setBboxes(prev => prev.filter(bbox => !bbox.active))}
        >
          <IconTrash />
        </Button>
        <Button
          isIconOnly
          title='Save'
          color='primary'
          variant='light'
          isDisabled={!bbox}
          onPress={() => setBboxes(
            prev => prev.map(bbox => bbox.active ? {
              ...bbox,
              label,
              description,
              active: false }
            : bbox ))
          }
        >
          <IconDeviceFloppy />
        </Button>
        <Button
          isIconOnly
          title='Discard'
          color='primary'
          variant='light'
          isDisabled={!bbox}
          onPress={() => setBboxes(prev => prev.map(bbox => bbox.active ? { ...bbox, active: false } : bbox ))}
        >
          <IconX />
        </Button>
      </div>
    </Card>
  )
}
