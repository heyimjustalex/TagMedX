import RouteLink from 'next/link';
import { IconEye, IconEyeExclamation, IconHealthRecognition } from '@tabler/icons-react';
import { Card, CardBody, CardFooter, CardHeader, Chip, Link, Select, SelectItem } from '@nextui-org/react';

export default function GroupPackage({ data, users, groupId, setPackages, isAdmin }) {

  const selectedKey = data?.id_user ? new Set().add(`${data.id_user}`) : new Set();

  return (
    <Card className='p-3 w-full sm:w-2-el md:w-3-el lg:w-4-el xl:w-5-el min-w-fit'>
      <CardHeader className='p-0 flex-row items-start'>
        <p className='text-xs'>Package</p>
      </CardHeader>
      <CardBody className='overflow-visible p-0'>
        <div className='flex justify-between'>
          <p className='flex text-default-800 font-bold uppercase'># {data.id}</p>
          <Chip className='flex' color={!data.id_user ? 'default' : data.is_ready ? 'success' : 'primary'} size='sm' variant='flat'>
            {!data.id_user ? 'Unassigned' : data.is_ready ? 'Ready' : 'Pending'}
          </Chip>
        </div>
        { isAdmin ?
          <Select 
            size='sm'
            className='mt-3'
            label="Assigned user"
            selectionMode='single'
            selectedKeys={selectedKey}
            onChange={e => {
              setPackages(prev => prev.map(
                pack => pack.id === data.id ? { ...data, id_user: parseInt(e.target.value) || null } : pack
              ))
            }}
          >
            {users.map((user) => (
              <SelectItem key={user.user_id} value={user.user_id}>
                {`${user.title || ''} ${user.name} ${user.surname}`}
              </SelectItem>
            ))}
          </Select>
        : null }
      </CardBody>
      <CardFooter className='p-0 pt-3'>
        { isAdmin ?
            <div className='flex justify-between w-full'>
              <Link
                isBlock
                size='sm'
                showAnchorIcon
                as={RouteLink}
                isDisabled={data.tentative === 0}
                anchorIcon={<IconEyeExclamation />}
                href={`/groups/${groupId}/sets/${data.id_set}/packages/${data.id}/editor?tentative=true`}
              >
                Uncertain
              </Link>
              <Link
                isBlock
                size='sm'
                showAnchorIcon
                as={RouteLink}
                isDisabled={data.all === 0}
                anchorIcon={<IconEye />}
                href={`/groups/${groupId}/sets/${data.id_set}/packages/${data.id}/editor`}
              >
                Browse All
              </Link>
            </div>
          : <div className='flex justify-center w-full'>
            <Link
              isBlock
              size='sm'
              showAnchorIcon
              as={RouteLink}
              isDisabled={data.all === 0}
              anchorIcon={<IconHealthRecognition />}
              href={`/groups/${groupId}/sets/${data.id_set}/packages/${data.id}/editor`}
            >
              Start Examination
            </Link>
          </div>
        }
      </CardFooter>
    </Card>
  )
}
