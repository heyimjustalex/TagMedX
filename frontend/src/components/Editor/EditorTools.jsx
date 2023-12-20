import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button, Card, Divider, Slider } from '@nextui-org/react';
import { IconArrowsMove, IconDeviceFloppy, IconFocus2, IconLogout2, IconNewSection, IconX } from '@tabler/icons-react';

import './Editor.css';
import { Tool } from './EditorConsts';

export default function EditorTools({ tool, scale, setScale, setTranslation, setTool, changed }) {
  const path = usePathname().split('/');
  return (
    <Card className='editor-tools'>
      <Button
        isIconOnly
        title='Move'
        color='primary'
        onPress={() => setTool(Tool.PAN)}
        variant={tool === Tool.PAN ? 'flat' : 'light'}
      >
        <IconArrowsMove />
      </Button>
      <Button
        isIconOnly
        title='Select'
        color='primary'
        onPress={() => setTool(Tool.SELECT)}
        variant={tool === Tool.SELECT ? 'flat' : 'light'} 
      >
        <IconNewSection />
      </Button>
      <Slider   
        size="md"
        step={0.5}
        maxValue={3}
        minValue={0.5}
        showSteps={true}
        value={scale}
        onChange={setScale}
        orientation="vertical"
        aria-label="scale"
        className='h-[180px] my-2'
      />
      <Button
        isIconOnly
        title='Center'
        color='primary'
        onPress={() => setTranslation({ x: 0, y: 0 })}
        variant='light' 
      >
        <IconFocus2 />
      </Button>
      <Divider />
      <Button
        isIconOnly
        title='Save'
        color='primary'
        variant='light'
        onPress={() => {}}
        isDisabled={!changed}
      >
        <IconDeviceFloppy />
      </Button>
      <Button
        isIconOnly
        title='Discard'
        color='primary'
        variant='light'
        onPress={() => {}}
        isDisabled={!changed}
      >
        <IconX />
      </Button>
      <Button
        as={Link}
        isIconOnly
        title='Exit'
        variant='light'
        href={`/groups/${path[2]}?tab=packages&set=${path[4]}`}
      >
        <IconLogout2 />
      </Button>
    </Card>
  )
}
