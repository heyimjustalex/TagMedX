'use client'

import { useState } from 'react';
import RouteLink from 'next/link';
import { useSearchParams } from 'next/navigation';
import { Card, CardBody, Tab, Tabs } from '@nextui-org/react';

import GroupSettings from './GroupSettings/GroupSettings';
import GroupUsers from './GroupUsers/GroupUsers';
import GroupSets from './GroupSets/GroupSets';

export default function Group({ group }) {
  const searchParams = useSearchParams();
  const tab = searchParams.get('tab') || 'overview';
  const [data, setData] = useState(group);

  return (
    <>
      <div className='flex'>
        <h1 className='text-4xl font-medium'>{data.name}</h1>
      </div>
      <div className='flex text-xs py-1 px-1 mb-5 text-gray-500'>{data.description}</div>
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
        <Tab key="sets" title="Sets" href={`/groups/${data.id}?tab=sets`} as={RouteLink}>
          <Card>
            <CardBody>
              <GroupSets data={data} setData={setData} />
            </CardBody>
          </Card>
        </Tab>
        <Tab key="packages" title="Packages" href={`/groups/${data.id}?tab=packages`} as={RouteLink}>
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
                <GroupUsers data={data} setData={setData} />
              </CardBody>
            </Card>
          </Tab>
        : null }
        {data?.role === 'Admin' ? 
          <Tab key="settings" title="Settings" href={`/groups/${data.id}?tab=settings`} as={RouteLink}>
            <GroupSettings data={data} setData={setData} />
          </Tab>
        : null }
      </Tabs>
    </>
  );
}