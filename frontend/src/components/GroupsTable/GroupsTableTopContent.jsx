import {
  Button,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
  Input
} from '@nextui-org/react';
import { IconChevronDown, IconPlus, IconSearch, IconUsersGroup } from '@tabler/icons-react';

import { roleOptions } from './GroupsTableConsts';

export default function GroupsTableTopContent({ filterValue, onClear, onSearchChange, statusFilter, setStatusFilter }) {
  return (
    <div className='flex flex-col gap-4'>
      <div className='flex flex-col sm:flex-row justify-between gap-3 items-end'>
        <Input
          isClearable
          className='w-full sm:max-w-full'
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
                Status
              </Button>
            </DropdownTrigger>
            <DropdownMenu
              disallowEmptySelection
              aria-label='Table Columns'
              closeOnSelect={false}
              selectedKeys={statusFilter}
              selectionMode='multiple'
              onSelectionChange={setStatusFilter}
            >
              {roleOptions.map((status) => (
                <DropdownItem key={status.uid} className='capitalize'>
                  {status.name}
                </DropdownItem>
              ))}
            </DropdownMenu>
          </Dropdown>
          <Button className='min-w-fit' color='primary' variant='flat' endContent={<IconPlus />}>
            Add New
          </Button>
          <Button className='min-w-fit' color='primary' endContent={<IconUsersGroup />}>
            Join Group
          </Button>
        </div>
      </div>
    </div>
  )
}
