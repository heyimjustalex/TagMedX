'use client'

import { useState } from 'react';
import RouteLink from 'next/link';
import { useSearchParams } from 'next/navigation';
import { Card, CardBody, Tab, Tabs } from '@nextui-org/react';

import GroupOverview from './GroupOverview/GroupOverview';
import GroupSettings from './GroupSettings/GroupSettings';
import GroupUsers from './GroupUsers/GroupUsers';
import GroupSets from './GroupSets/GroupSets';
import GroupPackages from './GroupPackages/GroupPackages';
import GroupLabels from './GroupLabels/GroupLabels';

export default function Group({ group }) {
  const searchParams = useSearchParams();
  const tab = searchParams.get('tab') || 'overview';
  const [data, setData] = useState(group);

  return (
    <>
      <div className='flex'>
        <h1 className='text-4xl font-medium'>{data.name}</h1>
      </div>
      <div className='flex text-xs py-1 px-1 mb-5 text-zinc-500'>{data.description}</div>
      <Tabs aria-label="Options" selectedKey={tab}>
        <Tab key="overview" title="Overview" href={`/groups/${data.id}?tab=overview`} as={RouteLink}>
          <Card>
            <CardBody className='p-4'>
              <GroupOverview data={data?.stats} />
            </CardBody>
          </Card>
        </Tab>
        <Tab key="sets" title="Sets" href={`/groups/${data.id}?tab=sets`} as={RouteLink}>
          <Card>
            <CardBody className='p-4'>
              <GroupSets data={data} setData={setData} />
            </CardBody>
          </Card>
        </Tab>
        <Tab key="packages" title="Packages" href={`/groups/${data.id}?tab=packages`} as={RouteLink}>
          <Card>
            <CardBody className='p-4'>
              <GroupPackages data={data} setData={setData} />
            </CardBody>
          </Card>
        </Tab>
        {data?.role === 'Admin' ? 
          <Tab key="labels" title="Labels" href={`/groups/${data.id}?tab=labels`} as={RouteLink}>
            <Card>
              <CardBody className='p-4'>
                <GroupLabels data={data} setData={setData} />
              </CardBody>
            </Card>
          </Tab>
        : null}
        {data?.role === 'Admin' ? 
          <Tab key="users" title="Users" href={`/groups/${data.id}?tab=users`} as={RouteLink}>
            <Card>
              <CardBody className='p-4'>
                <GroupUsers data={data} setData={setData} />
              </CardBody>
            </Card>
          </Tab>
        : null}
        {data?.role === 'Admin' ? 
          <Tab key="settings" title="Settings" href={`/groups/${data.id}?tab=settings`} as={RouteLink}>
            <Card>
              <CardBody className='p-4 gap-4'>
                <GroupSettings data={data} setData={setData} />
              </CardBody>
            </Card>
          </Tab>
        : null}
      </Tabs>
    </>
  );
}