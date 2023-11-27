import { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Button, Select, SelectItem } from '@nextui-org/react';
import { useRouter } from 'next/navigation';
import { IconDeviceFloppy, IconRestore } from '@tabler/icons-react';

import GroupPackage from './GroupPackage';

export default function GroupPackages({ data }) {

  const router = useRouter();
  const searchParams = useSearchParams();
  const [tab, setId] = [searchParams.get('tab'), searchParams.get('set')];
  const selectedKey = setId ? new Set().add(setId) : new Set();
  const [packages, setPackages] = useState(data.packages);

  return (
    <>
      <div className='flex flex-row justify-between gap-3 items-end'>
        <Select 
          size='sm'
          radius='md'
          selectionMode='single'
          selectedKeys={selectedKey}
          className='h-10 w-full sm:max-w-full'
          placeholder='Select set to display packages'
          classNames={{ inputWrapper: 'h-10', trigger: 'h-10 min-h-10' }}
          onChange={e => router.push(`/groups/${data.id}?tab=${tab}&set=${e.target.value}`)}
        >
          {data.sets.map((set) => (
            <SelectItem key={set.id} value={set.user_id}>
              {set.name}
            </SelectItem>
          ))}
        </Select>
        <Button className='min-w-fit' endContent={<IconRestore />} onPress={() => {}}>
          Discard
        </Button>
        <Button color='primary' className='min-w-fit' endContent={<IconDeviceFloppy />} onPress={() => {}}>
          Save
        </Button>
      </div>
      <div className='flex flex-row flex-wrap gap-4 w-full mt-4'>
        {packages?.map(e => <GroupPackage key={`${e.id}-${e.id_user}`} data={e} users={data.users} setPackages={setPackages} />)}
      </div>
    </>
  )
}
