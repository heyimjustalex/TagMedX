import { Button, Card, Progress } from '@nextui-org/react';
import { IconChevronLeft, IconChevronRight } from '@tabler/icons-react';

import './Editor.css';

export default function EditorNavigation({ pointer, setPointer, length }) {
  return (
    <Card className='editor-navigation'>
      <Button
        isIconOnly
        title='Previous'
        color='primary'
        variant='light'
        isDisabled={pointer === 0}
        onPress={() => setPointer(prev => prev - 1)}
      >
        <IconChevronLeft />
      </Button>
      <div className='flex w-24'>
        <Progress
          size='md'
          color='primary'
          value={pointer + 1}
          maxValue={length / 2}
          aria-label='progress-1/2'
          className='justify-center'
        />
      </div>
      <div className='flex text-sm text-zinc-500 items-center'>
        {pointer + 1}/{length}
      </div>
      <div className='flex w-24'>
        <Progress
          size='md'
          color='primary'
          maxValue={length / 2}
          aria-label='progress-2/2'
          className='justify-center'
          value={pointer + 1 > length / 2 ? pointer + 1 - length / 2 : 0}
        />
      </div>
      <Button
        isIconOnly
        title='Next'
        color='primary'
        variant='light'
        isDisabled={pointer + 1 === length}
        onPress={() => setPointer(prev => prev + 1)}
      >
        <IconChevronRight />
      </Button>
    </Card>
  )
}
