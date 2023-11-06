'use client'

import {
  Spinner,
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow,
  useDisclosure
} from '@nextui-org/react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import Link from 'next/link';

import { useNotification } from '../../hooks/useNotification';
import { columns, roleOptions } from './GroupsTableConsts';
import GroupsTableTopContent from './GroupsTableTopContent';
import { getGroups, renderCell } from './GroupsTableUtils';
import GroupsTableAddModal from './GroupsTableAddModal';
import GroupsTableJoinModal from './GroupsTableJoinModal';

export default function GroupsTable() {
  const addModal = useDisclosure();
  const joinModal = useDisclosure();
  const notification = useNotification();
  const [filterValue, setFilterValue] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [data, setData] = useState({ elements: [], ready: false });
  const [sortDescriptor, setSortDescriptor] = useState({ column: 'id', direction: 'descending' });
  const hasSearchFilter = Boolean(filterValue);

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
    if (roleFilter !== 'all' && Array.from(roleFilter).length !== roleOptions.length) {
      filteredUsers = filteredUsers.filter((user) => 
        Array.from(roleFilter).includes(user.role.toLowerCase())
      );
    }

    return filteredUsers;
  }, [data.elements, filterValue, roleFilter]);

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
      onSearchChange={onSearchChange}
      roleFilter={roleFilter}
      setRoleFilter={setRoleFilter}
      onAddOpen={addModal.onOpen}
      onJoinOpen={joinModal.onOpen}
    />
  ,[
    filterValue,
    roleFilter,
    data.elements.length,
    onSearchChange,
    hasSearchFilter,
    addModal.onOpen,
    joinModal.onOpen
  ]);

  return (
    <>
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
            <TableRow key={item.id} className='cursor-pointer' as={Link} href={`groups/${item.id}`}>
              {(columnKey) => <TableCell>{renderCell(item, columnKey)}</TableCell>}
            </TableRow>
          )}
        </TableBody>
      </Table>
      <GroupsTableAddModal
        isOpen={addModal.isOpen}
        onOpenChange={addModal.onOpenChange}
        setData={setData}
        notification={notification}
      />
      <GroupsTableJoinModal
        isOpen={joinModal.isOpen}
        onOpenChange={joinModal.onOpenChange}
        setData={setData}
        notification={notification}
      />
    </>
  );
}