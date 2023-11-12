import {
  Button,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
  Input
} from '@nextui-org/react';
import { IconChevronDown, IconSearch } from '@tabler/icons-react';

import { titleOptions } from './GroupUsersConsts';

export default function GroupUsersTopContent({ filterValue, onClear, onSearchChange, roleFilter, setRoleFilter }) {
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
        <div className='flex w-full sm:w-min gap-3'>
          <Dropdown>
            <DropdownTrigger className='flex w-full sm:w-min justify-end sm:justify-end'>
              <Button endContent={<IconChevronDown className='text-small' />} variant='flat'>
                Title
              </Button>
            </DropdownTrigger>
            <DropdownMenu
              disallowEmptySelection
              aria-label='Table Columns'
              closeOnSelect={false}
              selectedKeys={roleFilter}
              selectionMode='multiple'
              onSelectionChange={setRoleFilter}
            >
              {titleOptions.map((role) => (
                <DropdownItem key={role.uid} className='capitalize'>
                  {role.name}
                </DropdownItem>
              ))}
            </DropdownMenu>
          </Dropdown>
        </div>
      </div>
    </div>
  )
}
