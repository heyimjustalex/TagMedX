import { Button, Select, SelectItem } from '@nextui-org/react';
import { IconTag } from '@tabler/icons-react';
import { useRouter } from 'next/navigation';

import { defaultLabelModal } from './GroupLabelsConsts';

export default function GroupLabelsTopContent({ data, setId, setModal }) {

  const router = useRouter();
  const selectedKey = setId ? new Set().add(setId) : new Set();

  return (
    <div className='flex flex-row justify-between gap-3 items-end'>
      <Select 
        size='sm'
        radius='md'
        selectionMode='single'
        aria-label='set-selector'
        selectedKeys={selectedKey}
        className='h-10 w-full'
        placeholder='Select set to display labels'
        classNames={{ inputWrapper: 'h-10', trigger: 'h-10 min-h-10' }}
        onChange={e => router.push(`/groups/${data.id}?tab=labels&set=${e.target.value}`)}
      >
        {data.sets.map((set) => (
          <SelectItem key={set.id} value={set.user_id}>
            {set.name}
          </SelectItem>
        ))}
      </Select>
      <Button
        color='primary'
        className='min-w-fit'
        endContent={<IconTag />}
        onPress={() => setModal({ ...defaultLabelModal, open: true, edit: false })}
      >
        Add Label
      </Button>
    </div>
  )
}
