'use client'

import {
  Spinner,
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow
} from '@nextui-org/react';
import { useCallback, useEffect, useMemo, useState } from 'react';

import { useNotification } from '../../hooks/useNotification';
import { columns, roleOptions } from './GroupsTableConsts';
import GroupsTableTopContent from './GroupsTableTopContent';
import { getGroups, renderCell } from './GroupsTableUtils';

export default function GroupsTable() {
  const [filterValue, setFilterValue] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [data, setData] = useState({ elements: [], ready: false })
  const [sortDescriptor, setSortDescriptor] = useState({ column: 'id', direction: 'descending' });
  const hasSearchFilter = Boolean(filterValue);
  const notification = useNotification();

  useEffect(() => {
    getGroups(setData, notification)
  }, [])

  const filteredItems = useMemo(() => {
    let filteredUsers = [...data.elements];

    if (hasSearchFilter) {
      filteredUsers = filteredUsers.filter((group) =>
        group.name.toLowerCase().includes(filterValue.toLowerCase()),
      );
    }
    if (statusFilter !== 'all' && Array.from(statusFilter).length !== roleOptions.length) {
      filteredUsers = filteredUsers.filter((user) =>
        Array.from(statusFilter).includes(user.status),
      );
    }

    return filteredUsers;
  }, [data.elements, filterValue, statusFilter]);

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
    <GroupsTableTopContent
      filterValue={filterValue}
      onClear={onClear}
      onSearchChange={onClear}
      statusFilter={statusFilter}
      setStatusFilter={setStatusFilter}
    />
  ,[
    filterValue,
    statusFilter,
    data.elements.length,
    onSearchChange,
    hasSearchFilter,
  ]);

  return (
    <Table
      aria-label='Table with groups'
      isHeaderSticky
      bottomContentPlacement='outside'
      classNames={{ wrapper: 'max-h-full' }}
      selectionMode='single'
      showSelectionCheckboxes={false}
      sortDescriptor={sortDescriptor}
      topContent={topContent}
      topContentPlacement='outside'
      onSortChange={setSortDescriptor}
      onRowAction={(e) => console.log(e)}
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
        emptyContent={data.ready ? 'No groups found' : true}
        isLoading={!data.ready}
        loadingContent={<Spinner className='mt-10' label='Loading groups...' />}
      >
        {(item) => (
          <TableRow key={item.id} className='cursor-pointer'>
            {(columnKey) => <TableCell>{renderCell(item, columnKey)}</TableCell>}
          </TableRow>
        )}
      </TableBody>
    </Table>
  );
}