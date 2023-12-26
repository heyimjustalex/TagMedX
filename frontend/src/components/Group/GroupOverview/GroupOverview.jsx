import { useState } from 'react';
import { Card, Switch } from '@nextui-org/react';
import { IconAlertTriangle, IconBoxModel, IconBoxModel2, IconPackage, IconProgressCheck } from '@tabler/icons-react';

import GroupOverviewCard from './GroupOverviewCard';
import { NextColor } from '../../../consts/NextColor';

export default function GroupOverview({ data }) {

  const [userOnly, setUserOnly] = useState(false);

  return (
    <>
      <Card className='flex flex-row pl-3 pr-1 py-2 mb-4 justify-between'>
        <p className='flex w-max text-sm'>Show user stats only</p>
        <Switch className='flex' color={NextColor.SUCCESS} size='sm' onValueChange={setUserOnly}/>
        
      </Card>
      <div className='flex flex-row flex-wrap gap-4 w-full'>
        <GroupOverviewCard
          title='Detection sets'
          Icon={IconBoxModel2}
          val1={data?.detection_sets}
          val2={data?.sets}
          color={NextColor.PRIMARY}
        />
        <GroupOverviewCard
          title='Classification sets'
          Icon={IconBoxModel}
          val1={data?.classification_sets}
          val2={data?.sets}
          color={NextColor.DANGER}
        />
        <GroupOverviewCard
          title='Ready packages'
          Icon={IconPackage}
          val1={userOnly ? data?.user_ready_packages : data?.ready_packages}
          val2={userOnly ? data?.user_packages : data?.packages}
          color={NextColor.SECONDARY}
        />
        <GroupOverviewCard
          title='Total progress'
          Icon={IconProgressCheck}
          val1={userOnly ? data?.user_examinated_samples : data?.examinated_samples}
          val2={userOnly ? data?.user_samples : data?.samples}
          color={NextColor.SUCCESS}
        />
        <GroupOverviewCard
          title='Tentative examinations'
          Icon={IconAlertTriangle}
          val1={userOnly ? data?.user_tentative_examinations : data?.tentative_examinations}
          val2={userOnly ? data?.user_examinated_samples : data?.examinated_samples}
          color={NextColor.WARNING}
        />
      </div>
    </>
  )
}
