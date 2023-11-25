import { useState } from 'react';
import { Button, Input, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader } from '@nextui-org/react';

import { addGroup } from './GroupsTableUtils';

export default function GroupsTableAddModal({ isOpen, onOpenChange, setData, notification }) {

  const [value, setValue] = useState('');
  const [sent, setSent] = useState(false);

  return (
    <Modal 
      isOpen={isOpen}
      onOpenChange={() => { onOpenChange(); setValue('')}}
      placement='top-center'
    >
      <ModalContent>
        {(onClose) => (
          <>
            <ModalHeader className='flex flex-col gap-1'>Create Group</ModalHeader>
            <ModalBody>
              <Input
                autoFocus
                label='Name'
                variant='bordered'
                value={value}
                onValueChange={setValue}
              />
            </ModalBody>
            <ModalFooter>
              <Button
                onPress={onClose}
              >
                Close
              </Button>
              <Button
                color='primary'
                isDisabled={!value}
                onClick={() => addGroup(value, setSent, onClose, setData, notification)}
                isLoading={sent}
              >
                Create
              </Button>
            </ModalFooter>
          </>
        )}
      </ModalContent>
    </Modal>
  )
}