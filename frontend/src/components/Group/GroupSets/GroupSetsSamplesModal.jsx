import { useEffect, useRef, useState } from 'react';
import { IconX } from '@tabler/icons-react';
import {
  Button,
  Card,
  CardBody,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow,
} from '@nextui-org/react';

import './GroupSets.css';

export default function GroupSetsSamplesModal({ modal, setModal, notification }) {

  const [sent, setSent] = useState(false);
  const [files, setFiles] = useState([]);

  const input = useRef(null);

  const handleChange = event => {
    if (event.target.files) {
      setFiles(prev => [...prev, ...event.target.files])
      // const i = event.target.files[0];
      // const body = new FormData();
      // body.append('image', i);
    }
  };

  useEffect(() => {
    if(modal.open) setFiles([])
  }, [modal.open])

  console.log(files)

  return (
    <>
      <Modal 
        size='lg'
        hideCloseButton
        isOpen={modal.open}
        placement='top-center'
        className='group-sets-samples'
        classNames={{
          footer: 'justify-between overflow-hidden',
        }}
      >
        <ModalContent>
          <ModalHeader className='flex flex-col gap-1'>
            Upload Samples
          </ModalHeader>
          <ModalBody>
            {
              files.length === 0
              ? <Card isPressable shadow='sm' onPress={() => input.current.click()}>
                <CardBody className='p-4 text-center text-default-500'>
                  No files selected
                </CardBody>
              </Card>
              : <Table
                removeWrapper
                selectionMode='single'
                aria-label='files-table'
                classNames={{
                  base: 'max-h-screen-base overflow-scroll',
                  table: 'min-h-screen-table',
                }}
              >
              <TableHeader className='hidden'>
                <TableColumn className='hidden'/>
                <TableColumn className='hidden'/>
              </TableHeader>
                  <TableBody className='p-0'>
                    {files.map((e, i) =>
                      <TableRow key={i}>
                        <TableCell>
                          {e.name}
                        </TableCell>
                        <TableCell className='flex justify-end'>
                          <IconX
                            className='cursor-pointer'
                            size={20}
                            onClick={() => setFiles(prev => prev.filter((_, j) => i !== j))}
                          />
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
            }
          </ModalBody>
          <ModalFooter>
            <div className='flex items-center text-default-500 text-xs'>
              {files.length > 0 ? files.length === 1 ? '1 file' : `${files.length} files` : null}
            </div>
            <div className='flex gap-2'>
              <Button
                onPress={() => setModal(prev => ({ ...prev, open: false }))}
              >
                Cancel
              </Button>
              <Button
                color='primary'
                variant='flat'
                onClick={() => input.current.click()}
                isLoading={sent}
              >
                Add files
              </Button>
              <Button
                color='primary'
                isDisabled={files.length === 0}
                onClick={() => {}}
                isLoading={sent}
              >
                Upload
              </Button>
            </div>
          </ModalFooter>
        </ModalContent>
      </Modal>
      <input
        multiple
        type='file'
        ref={input}
        onChange={handleChange}
        accept='image/*'
        className='hidden'
      />
    </>
  )
}