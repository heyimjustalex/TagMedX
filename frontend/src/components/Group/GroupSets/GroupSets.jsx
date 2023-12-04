'use client'

import {
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow
} from '@nextui-org/react';
import { useCallback, useMemo, useState } from 'react';
import Link from 'next/link';

import { renderCell } from './GroupSetsUtils';
import GroupSetsModal from './GroupSetsModal';
import GroupSetsTopContent from './GroupSetsTopContent';
import GroupSetsRemoveModal from './GroupSetsRemoveModal';
import GroupSetsSamplesModal from './GroupSetsSamplesModal';
import { useNotification } from '../../../hooks/useNotification';
import { adminColumns, columns, defaultModal, typeOptions } from './GroupSetsConsts';

export default function GroupSets({ data, setData }) {
  const notification = useNotification();
  const [modal, setModal] = useState(defaultModal);
  const [filterValue, setFilterValue] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');
  const [removeModal, setRemoveModal] = useState({ open: false, name: '', id: '' });
  const [samplesModal, setSamplesModal] = useState({ open: false, name: '', id: '' });
  const [sortDescriptor, setSortDescriptor] = useState({ column: 'id', direction: 'descending' });
  const hasSearchFilter = Boolean(filterValue);

  const filteredItems = useMemo(() => {
    let filteredSets = [...data.sets];

    if (hasSearchFilter) {
      filteredSets = filteredSets.filter((set) =>
        set.name.toLowerCase().includes(filterValue.toLowerCase()),
      );
    }
    if (typeFilter !== 'all' && Array.from(typeFilter).length !== typeOptions.length) {
      filteredSets = filteredSets.filter((set) => 
        Array.from(typeFilter).includes(set.type)
      );
    }

    return filteredSets;
  }, [data.sets, filterValue, typeFilter]);

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
    <GroupSetsTopContent
      filterValue={filterValue}
      onClear={onClear}
      onSearchChange={onSearchChange}
      typeFilter={typeFilter}
      setTypeFilter={setTypeFilter}
      onAddOpen={() => setModal({ ...defaultModal, open: true, edit: false })}
      isAdmin={data?.role === 'Admin'}
    />
  ,[
    filterValue,
    typeFilter,
    data.sets.length,
    onSearchChange,
    hasSearchFilter,
    setModal,
    data.role
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
        <TableHeader columns={data?.role === 'Admin' ? adminColumns : columns}>
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
          emptyContent='No sets found.'
        >
          {(item) => (
            <TableRow key={item.id} className='cursor-pointer' as={Link} href={`/groups/${data.id}?tab=packages&set=${item.id}`}>
              {(columnKey) => <TableCell>{renderCell(item, columnKey, setModal, setRemoveModal, setSamplesModal)}</TableCell>}
            </TableRow>
          )}
        </TableBody>
      </Table>
      <GroupSetsModal
        modal={modal}
        setModal={setModal}
        groupId={data.id}
        setData={setData}
        notification={notification}
      />
      <GroupSetsRemoveModal
        modal={removeModal}
        setModal={setRemoveModal}
        setData={setData}
        notification={notification}
      />
      <GroupSetsSamplesModal
        modal={samplesModal}
        setModal={setSamplesModal}
        setData={setData}
        notification={notification}
      />
    </>
  );
}