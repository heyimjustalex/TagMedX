import {
  Button,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
  Input
} from '@nextui-org/react';
import { IconChevronDown, IconPlus, IconSearch } from '@tabler/icons-react';

import { typeOptions } from './GroupSetsConsts';

export default function GroupSetsTopContent({ filterValue, onClear, onSearchChange, typeFilter, setTypeFilter, onAddOpen }) {
  return (
    <div className='flex flex-col gap-4'>
      <div className='flex flex-row justify-between gap-3 items-end'>
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
        <Dropdown>
          <DropdownTrigger>
            <Button endContent={<IconChevronDown className='text-small' />} variant='flat' className='min-w-fit'>
              Type
            </Button>
          </DropdownTrigger>
          <DropdownMenu
            disallowEmptySelection
            aria-label='Table Columns'
            closeOnSelect={false}
            selectedKeys={typeFilter}
            selectionMode='multiple'
            onSelectionChange={setTypeFilter}
          >
            {typeOptions.map((type) => (
              <DropdownItem key={type} className='capitalize'>
                {type}
              </DropdownItem>
            ))}
          </DropdownMenu>
        </Dropdown>
        <Button color='primary' className='min-w-fit' endContent={<IconPlus />} onPress={onAddOpen}>
          Add New
        </Button>
      </div>
    </div>
  )
}
