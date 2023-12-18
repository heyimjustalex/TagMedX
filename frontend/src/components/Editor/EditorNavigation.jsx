import { Button, Card } from '@nextui-org/react';
import { IconChevronLeft, IconChevronRight } from '@tabler/icons-react';

import './Editor.css';

export default function EditorNavigation({ pointer, setPointer, length, setStatus }) {
  return (
    <Card className='editor-navigation'>
      <Button
        isIconOnly
        title='Previous'
        color='primary'
        variant='light'
        isDisabled={pointer === 0}
        onPress={() => { setStatus({ ready: false, error: false }); setPointer(prev => prev - 1) }}
      >
        <IconChevronLeft />
      </Button>
      <div className='flex text-sm text-zinc-500 items-center px-2'>
        {pointer + 1}/{length}
      </div>
      <Button
        isIconOnly
        title='Next'
        color='primary'
        variant='light'
        isDisabled={pointer + 1 === length}
        onPress={() => { setStatus({ ready: false, error: false }); setPointer(prev => prev + 1)} }
      >
        <IconChevronRight />
      </Button>
    </Card>
  )
}
