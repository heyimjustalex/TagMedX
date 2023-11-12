import React, { useCallback, useMemo, useState } from 'react'
import { Table, TableBody, TableCell, TableColumn, TableHeader, TableRow } from '@nextui-org/react';

import { columns } from './GroupUsersConsts';
import { useNotification } from '../../../hooks/useNotification';
import { titleOptions } from './GroupUsersConsts';
import GroupUsersTopContent from './GroupUsersTopContent';
import { renderCell } from './GroupUsersUtils';

export default function GroupUsers({ data, setData }) {

  const notification = useNotification();
  const [filterValue, setFilterValue] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [sortDescriptor, setSortDescriptor] = useState({ column: 'id', direction: 'descending' });
  const hasSearchFilter = Boolean(filterValue);

  const filteredItems = useMemo(() => {
    // let filteredUsers = [];
    let filteredUsers = [...data.users];

    if (hasSearchFilter) {
      filteredUsers = filteredUsers.filter((group) =>
        group.name.toLowerCase().includes(filterValue.toLowerCase())
      );
    }

    // if (roleFilter !== 'all' && Array.from(roleFilter).length !== titleOptions.length) {
    //   filteredUsers = filteredUsers.filter((user) => 
    //     Array.from(roleFilter).includes(user.role.toLowerCase())
    //   );
    // }

    return filteredUsers;
  }, [data.users, filterValue]);

  const sortedItems = useMemo(() => {
    return [...filteredItems].sort((a, b) => {
      const first = a[sortDescriptor.column];
      const second = b[sortDescriptor.column];
      const cmp = first < second ? -1 : first > second ? 1 : 0;

      return sortDescriptor.direction === 'descending' ? -cmp : cmp;
    });
  }, [sortDescriptor, filteredItems]);

  const onSearchChange = useCallback((value) => {
    if (value) setFilterValue(value);
    else setFilterValue('');
  }, []);

  const onClear = useCallback(()=>{
    setFilterValue('')
  },[])

  const topContent = useMemo(() =>
    <GroupUsersTopContent
      filterValue={filterValue}
      onClear={onClear}
      onSearchChange={onSearchChange}
      roleFilter={roleFilter}
      setRoleFilter={setRoleFilter}
    />
  ,[
    filterValue,
    roleFilter,
    data.users.length,
    onSearchChange,
    hasSearchFilter
  ]);

  return (
    <Table
      aria-label='Table with users'
      isHeaderSticky
      bottomContentPlacement='outside'
      classNames={{ wrapper: 'max-h-full' }}
      selectionMode='single'
      showSelectionCheckboxes={false}
      sortDescriptor={sortDescriptor}
      topContent={topContent}
      topContentPlacement='outside'
      onSortChange={setSortDescriptor}
    >
      <TableHeader columns={columns}>
        {(column) => (
          <TableColumn
            key={column.uid}
            allowsSorting={column.sortable}
          >
            {column.name}
          </TableColumn>
        )}
      </TableHeader>
      <TableBody
        items={sortedItems}
        emptyContent={data.ready ? 'No users found' : true}
      >
        {(item) => (
          <TableRow key={item.user_id} className='cursor-pointer'>
            {(columnKey) => <TableCell>{renderCell(item, columnKey)}</TableCell>}
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}
