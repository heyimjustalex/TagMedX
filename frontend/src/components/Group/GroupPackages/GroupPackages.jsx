import { useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useSearchParams } from 'next/navigation';
import { Button, Select, SelectItem } from '@nextui-org/react';
import { IconDeviceFloppy, IconEditOff } from '@tabler/icons-react';

import GroupPackage from './GroupPackage';
import { savePackages } from './GroupPackagesUtils';
import { useNotification } from '../../../hooks/useNotification';

export default function GroupPackages({ data, setData }) {

  const router = useRouter();
  const searchParams = useSearchParams();
  const notification = useNotification();
  const [tab, setId] = [searchParams.get('tab'), searchParams.get('set')];
  const selectedKey = setId ? new Set().add(setId) : new Set();
  const [packages, setPackages] = useState(data.packages);

  const isModified = useMemo(() => {
    return packages?.some((e, i) => e.id_user !== data.packages[i].id_user) || false
  }, [packages, data.packages])

  return (
    <>
      <div className='flex flex-row justify-between gap-3 items-end'>
        <Select 
          size='sm'
          radius='md'
          selectionMode='single'
          aria-label='set-selector'
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
        <Button
          className='min-w-fit'
          endContent={<IconEditOff />}
          onPress={() => setPackages(data.packages)}
          isDisabled={!isModified}
        >
          Discard
        </Button>
        <Button
          color='primary'
          className='min-w-fit'
          endContent={<IconDeviceFloppy />}
          onPress={() => savePackages(packages, setPackages, data.packages, setData, notification)}
          isDisabled={!isModified}
        >
          Save
        </Button>
      </div>
      {
        packages?.length > 0
        ? <div className='flex flex-row flex-wrap gap-4 w-full mt-4'>
          {packages?.map(e => <GroupPackage key={`${e.id}-${e.id_user}`} data={e} users={data.users} setPackages={setPackages} />)}
        </div>
        : <div className='flex text-foreground-400 items-center justify-center h-40'>
          {data.role === 'Admin' && data?.sets?.length === 0 ? 'No packages found, create set first.' : 'No packages found.'}
        </div>
      }
    </>
  )
}
