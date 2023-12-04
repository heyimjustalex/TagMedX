import { useEffect, useState } from 'react';
import { Button, Card, Select, SelectItem, Textarea } from '@nextui-org/react';
import { IconDeviceFloppy, IconTrash, IconX } from '@tabler/icons-react';

import './Editor.css';

export default function EditorDescriptor({ bbox, setBboxes, labels }) {

  const [label, setLabel] = useState(new Set());
  const [description, setDescription] = useState('');

  useEffect(() => {
    setLabel(bbox?.label || new Set());
    setDescription(bbox?.description || '');
  }, [bbox]);

  return (
    <Card className='editor-descriptor'>
      <Select
        label="Label"
        items={labels}
        isDisabled={!bbox}
        selectionMode='single'
        selectedKeys={label}
        onSelectionChange={e => setLabel(e)}
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
          isDisabled={!bbox}
          onPress={() => setBboxes(prev => prev.filter(bbox => !bbox.active))}
        >
          <IconTrash />
        </Button>
        <div className='flex'>
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
            <Button
              isIconOnly
              title='Save'
              color='primary'
              variant='light'
              isDisabled={!bbox}
              onPress={() => setBboxes(prev => prev.map(bbox => bbox.active ? { ...bbox, label, description, active: false } : bbox ))}
            >
              <IconDeviceFloppy />
            </Button>
        </div>
      </div>
    </Card>
  )
}
