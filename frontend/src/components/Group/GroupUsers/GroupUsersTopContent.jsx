import { Input } from '@nextui-org/react';
import { IconSearch } from '@tabler/icons-react';

export default function GroupUsersTopContent({ filterValue, onClear, onSearchChange }) {
  return (
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
  )
}
