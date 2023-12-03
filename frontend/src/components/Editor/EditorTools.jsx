import { Button, Card, Slider } from '@nextui-org/react';
import { IconArrowsMove, IconNewSection } from '@tabler/icons-react';

import './Editor.css';
import { Tool } from './EditorConsts';

export default function EditorTools({ scale, setScale, tool, setTool }) {
  return (
    <Card className='editor-tools'>
      <Button
        isIconOnly
        color='primary'
        onPress={() => setTool(Tool.PAN)}
        variant={tool === Tool.PAN ? 'flat' : 'light'}
      >
        <IconArrowsMove />
      </Button>
      <Button
        isIconOnly
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
    </Card>
  )
}
