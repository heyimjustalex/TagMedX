import { useState } from 'react';
import { Card, Switch } from '@nextui-org/react';
import { IconAlertTriangle, IconBoxModel, IconBoxModel2, IconPackage, IconProgressCheck } from '@tabler/icons-react';

import { NextColor } from '../../../consts/NextColor';
import GroupOverviewCard from './GroupOverviewCard';

export default function GroupOverview() {

  const [userOnly, setUserOnly] = useState(false);

  return (
    <>
      <Card className='flex flex-row pl-3 pr-1 py-2 mb-4 justify-between'>
        <p className='flex w-max text-sm'>Show user stats only</p>
        <Switch className='flex' color={NextColor.SUCCESS} size='sm' onValueChange={setUserOnly}/>
        
      </Card>
      <div className='flex flex-row flex-wrap gap-4 w-full'>
      <GroupOverviewCard title='Detection sets' Icon={IconBoxModel2} val1={1} val2={2} color={NextColor.PRIMARY} />
        <GroupOverviewCard title='Classification sets' Icon={IconBoxModel} val1={1} val2={2} color={NextColor.DANGER} />
        <GroupOverviewCard title='Ready packages' Icon={IconPackage} val1={userOnly ? 2 : 3} val2={userOnly ? 5 : 10} color={NextColor.SECONDARY} />
        <GroupOverviewCard title='Total progress' Icon={IconProgressCheck} val1={userOnly ? 59 : 123} val2={userOnly ? 109 : 432} color={NextColor.SUCCESS} />
        <GroupOverviewCard title='Tentative examinations' Icon={IconAlertTriangle} val1={userOnly ? 4 : 12} val2={userOnly ? 109 : 432} color={NextColor.WARNING} />
      </div>
    </>
  )
}
