import { Card, CardBody, CardHeader, Chip, Select, SelectItem } from '@nextui-org/react';

export default function GroupPackage({ data, users, setPackages }) {

  const selectedKey = data?.id_user ? new Set().add(`${data.id_user}`) : new Set();

  return (
    <Card className='p-3 w-full sm:w-2-el md:w-3-el lg:w-4-el xl:w-5-el min-w-fit'>
      <CardHeader className='p-0 flex-row items-start'>
        <p className='text-xs'>Package</p>
      </CardHeader>
      <CardBody className='overflow-visible p-0'>
        <div className='flex justify-between'>
          <p className='flex text-default-800 font-bold uppercase'># {data.id}</p>
          <Chip className='flex' color={data.is_ready ? 'success' : 'primary'} size='sm' variant='flat'>
            {data.is_ready ? 'Ready' : 'Pending'}
          </Chip>
        </div>
        <Select 
          size='sm'
          className='mt-3'
          label="Assigned user"
          selectionMode='single'
          selectedKeys={selectedKey}
          onChange={e => {
            setPackages(prev => prev.map(
              pack => pack.id === data.id ? { ...data, id_user: parseInt(e.target.value) } : pack
            ))
          }}
        >
          {users.map((user) => (
            <SelectItem key={user.user_id} value={user.user_id}>
              {`${user.title} ${user.name} ${user.surname}`}
            </SelectItem>
          ))}
        </Select>
      </CardBody>
    </Card>
  )
}
