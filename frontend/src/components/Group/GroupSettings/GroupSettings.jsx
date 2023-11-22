import { useMemo, useState } from 'react';
import { Button, ButtonGroup, Card, CardBody, Input, Textarea } from '@nextui-org/react';
import { IconCopy, IconRefresh } from '@tabler/icons-react';

import { generateRandomString } from '../../../utils/text';
import { postSettings } from './GroupSettingsUtils';
import { useNotification } from '../../../hooks/useNotification';

export default function GroupSettings({ data, setData }) {

  const notification = useNotification();
  const [sent, setSent] = useState(false);
  const [settings, setSettings] = useState({
    name: data.name,
    description: data.description,
    connectionString: data.connection_string
  });
  
  const copyBtn = useMemo(() =>
    <Button
      isIconOnly
      radius='sm'
      variant='light'
      className='min-w-min w-8 h-7 ml-1'
      onPress={() => navigator.clipboard.writeText(settings.connectionString)}
    >
      <IconCopy size={16} className='cursor-pointer' />
    </Button>
  ,[setSettings])

  const resetBtn = useMemo(() =>
    <Button
      isIconOnly
      color='danger'
      variant='light'
      radius='sm'
      className='min-w-min w-8 h-7 mx-1'
      onPress={() => setSettings({ ...settings, connectionString: generateRandomString(32) })}
    >
      <IconRefresh size={16} className='cursor-pointer' />
    </Button>
  ,[setSettings])

  const modified = useMemo(() => 
    settings.name !== data.name ||
    settings.description !== data.description ||
    settings.connectionString !== data.connection_string
  ,[settings, data])

  return (
    <Card>
      <CardBody className='gap-4'>
        <Input
          size='md'
          type='text'
          label='Name'
          labelPlacement='outside'
          className='max-w-3xl'
          value={settings.name}
          onChange={e => setSettings({ ...settings, name: e.target.value })}
        />
        <Textarea
          minRows={2}
          label='Description'
          className='max-w-3xl'
          labelPlacement='outside'
          value={settings.description}
          onChange={e => setSettings({ ...settings, description: e.target.value })}
        />
        <Input
          isReadOnly
          size='md'
          type='text'
          variant='bordered'
          classNames={{
            base: 'max-w-3xl p-0',
            inputWrapper: 'p-0',
          }}
          label='Connection string'
          labelPlacement='outside'
          value={settings.connectionString}
          startContent={copyBtn}
          endContent={resetBtn}
        />
        <ButtonGroup className='justify-start'>
          <Button
            variant='ghost'
            isDisabled={!modified}
            onPress={() => setSettings({
              name: data.name,
              description: data.description,
              connectionString: data.connection_string
            })}
          >
            Cancel
          </Button>
          <Button
            color='primary'
            isDisabled={!modified}
            isLoading={sent}
            onPress={() => postSettings(settings, data.id, setSent, setData, notification)}
          >
            Save
          </Button>
        </ButtonGroup>
      </CardBody>
    </Card>
  )
}
