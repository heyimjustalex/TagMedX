import { Button, Card, Progress } from '@nextui-org/react';
import { IconChevronLeft, IconChevronRight } from '@tabler/icons-react';

import './Editor.css';

export default function EditorNavigation() {
  return (
    <Card className='editor-navigation'>
      <Button
        isIconOnly
        title='Previous'
        color='primary'
        onPress={() => {}}
        variant='light'
      >
        <IconChevronLeft />
      </Button>
      <div className='flex w-24'>
        <Progress
          size='md'
          value={1}
          maxValue={5}
          color='primary'
          // label='6/10'
          className='justify-center'
        />
      </div>
      <div className='flex text-sm text-zinc-500 items-center'>6/10</div>
      <div className='flex w-24'>
        <Progress
          size='md'
          value={0}
          maxValue={5}
          color='primary'
          // label='6/10'
          className='justify-center'
        />
      </div>
      <Button
        isIconOnly
        title='Next'
        color='primary'
        onPress={() => {}}
        variant='light'
      >
        <IconChevronRight />
      </Button>
    </Card>
  )
}
