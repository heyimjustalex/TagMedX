import { Button, Card, Slider } from '@nextui-org/react';
import { IconArrowsMove, IconFocus2, IconNewSection } from '@tabler/icons-react';

import './Editor.css';
import { Tool } from './EditorConsts';

export default function EditorTools({ tool, scale, setScale, setTranslation, setTool }) {
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
    </Card>
  )
}
