import {
  Button,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
  Input
} from '@nextui-org/react';
import { IconChevronDown, IconPlus, IconSearch } from '@tabler/icons-react';

import { roleOptions } from './GroupsTableConsts';

export default function GroupsTableTopContent({ filterValue, onClear, onSearchChange, statusFilter, setStatusFilter }) {
  return (
    <div className='flex flex-col gap-4'>
        <div className='flex justify-between gap-3 items-end'>
          <Input
            isClearable
            className='w-full sm:max-w-full'
            placeholder='Search by name...'
            startContent={<IconSearch />}
            value={filterValue}
            onClear={() => onClear()}
            onValueChange={onSearchChange}
          />
          <div className='flex gap-3'>
            <Dropdown>
              <DropdownTrigger className='hidden sm:flex'>
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
            <Button color='primary' endContent={<IconPlus />}>
              Add New
            </Button>
          </div>
        </div>
      </div>
  )
}
