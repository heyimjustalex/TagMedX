import { Card, CardBody, CardFooter, CardHeader, CircularProgress } from '@nextui-org/react';

export default function GroupOverviewCard({ title, Icon, val1, val2, color }) {
  return (
    <Card className='p-3 w-full sm:w-2-el md:w-3-el lg:w-4-el xl:w-5-el min-w-fit'>
      <CardHeader className='p-0 flex-row justify-between'>
        <p className='text-xs flex'>{title}</p>
        <Icon size={20} className='flex' />
      </CardHeader>
      <CardBody className='overflow-visible p-0 py-4 items-center'>
      <CircularProgress
          classNames={{
            svg: 'w-36 h-36 drop-shadow-md',
            value: 'text-3xl font-semibold',
          }}
          value={val2 ? Math.floor(val1 / val2 * 100) : 0}
          strokeWidth={4}
          showValueLabel={true}
          color={color}
          aria-label='stat'
        />
      </CardBody>
      <CardFooter className='p-0 justify-center'>
        <p className='flex'>{val1} out of {val2}</p>
      </CardFooter>
    </Card>
  )
}
