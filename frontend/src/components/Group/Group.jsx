'use client'

import { useState } from 'react';
import RouteLink from 'next/link';
import { useSearchParams } from 'next/navigation';
import { Card, CardBody, Tab, Tabs } from '@nextui-org/react';

import GroupSettings from './GroupSettings/GroupSettings';
import GroupUsers from './GroupUsers/GroupUsers';

export default function Group({ data }) {
  const searchParams = useSearchParams();
  const tab = searchParams.get('tab') || 'overview';

  const [groupData, setGroupData] = useState(data);

  return (
    <>
      <div className='flex'>
        <h1 className='text-4xl font-medium'>{groupData.name}</h1>
      </div>
      <div className='flex text-sm py-3 px-1 text-gray-500'>{groupData.description}</div>
      <Tabs aria-label="Options" selectedKey={tab}>
        <Tab key="overview" title="Overview" href={`/groups/${data.id}?tab=overview`} as={RouteLink}>
          <Card>
            <CardBody>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
              incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
              exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            </CardBody>
          </Card>
        </Tab>
        {data?.role === 'Admin' ? 
          <Tab key="users" title="Users" href={`/groups/${data.id}?tab=users`} as={RouteLink}>
            <Card>
              <CardBody>
                <GroupUsers data={groupData} setData={setGroupData} />
              </CardBody>
            </Card>
          </Tab>
        : null }
        {data?.role === 'Admin' ? 
          <Tab key="settings" title="Settings" href={`/groups/${data.id}?tab=settings`} as={RouteLink}>
            <GroupSettings data={groupData} setData={setGroupData} />
          </Tab>
        : null }
      </Tabs>
    </>
  );
}