import { useMemo, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import {
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow
} from '@nextui-org/react';

import { columns, defaultLabelModal } from './GroupLabelsConsts';
import { renderCell } from './GroupLabelsUtils';
import GroupLabelsTopContent from './GroupLabelsTopContent';
import GroupLabelsModal from './GroupLabelsModal';
import GroupLabelsRemoveModal from './GroupLabelsRemoveModal';
import { useNotification } from '../../../hooks/useNotification';

export default function GroupLabels({ data, setData }) {

  const searchParams = useSearchParams();
  const setId = searchParams.get('set');
  const setIdNum = parseInt(setId);
  const notification = useNotification();
  const [modal, setModal] = useState(defaultLabelModal);
  const [removeModal, setRemoveModal] = useState(defaultLabelModal);
  const [sortDescriptor, setSortDescriptor] = useState({ column: 'id', direction: 'descending' });

  const filteredItems = useMemo(() => {
    return data.labels.filter(e => e.id_set === setIdNum);
  }, [data.labels, setId]);

  const sortedItems = useMemo(() => {
    return [...filteredItems].sort((a, b) => {
      const first = a[sortDescriptor.column];
      const second = b[sortDescriptor.column];
      const cmp = first < second ? -1 : first > second ? 1 : 0;
      return sortDescriptor.direction === 'descending' ? -cmp : cmp;
    });
  }, [sortDescriptor, filteredItems]);

  const topContent = useMemo(() =>
    <GroupLabelsTopContent
      data={data}
      setId={setId}
      setModal={setModal}
    />
  ,[data, setId, setModal]);

  return (
    <>
      <Table
        aria-label='labels-table'
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
          emptyContent='No labels found.'
        >
          {(item) => (
            <TableRow key={item.id}>
              {(columnKey) => <TableCell>{renderCell(item, columnKey, setModal, setRemoveModal)}</TableCell>}
            </TableRow>
          )}
        </TableBody>
      </Table>
      <GroupLabelsModal
        modal={modal}
        setModal={setModal}
        setId={setId}
        setData={setData}
        notification={notification}
      />
      <GroupLabelsRemoveModal
        modal={removeModal}
        setModal={setRemoveModal}
        setId={setId}
        setData={setData}
        notification={notification}
      />
    </>
  )
}
