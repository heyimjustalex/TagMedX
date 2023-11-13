import { Input } from '@nextui-org/react';
import { IconSearch } from '@tabler/icons-react';

export default function GroupUsersTopContent({ filterValue, onClear, onSearchChange }) {
  return (
    <div className='flex flex-col gap-4'>
      <div className='flex flex-col sm:flex-row justify-between gap-3 items-end'>
        <Input
          isClearable
          radius='md'
          className='h-10 w-full sm:max-w-full'
          classNames={{ inputWrapper: 'h-10' }}
          placeholder='Search by name...'
          startContent={<IconSearch />}
          value={filterValue}
          onClear={() => onClear()}
          onValueChange={onSearchChange}
        />
      </div>
    </div>
  )
}
