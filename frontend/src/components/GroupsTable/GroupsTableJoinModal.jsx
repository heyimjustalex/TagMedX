import { useState } from 'react';
import { Button, Input, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader } from '@nextui-org/react';

import { joinGroup } from './GroupsTableUtils';

export default function GroupsTableJoinModal({ isOpen, onOpenChange, setData, notification }) {

  const [value, setValue] = useState('');
  const [sent, setSent] = useState(false);

  return (
    <Modal
      hideCloseButton
      isOpen={isOpen}
      onOpenChange={() => { onOpenChange(); setValue('')}}
      placement='top-center'
    >
      <ModalContent>
        {(onClose) => (
          <>
            <ModalHeader className='flex flex-col gap-1'>Join Group</ModalHeader>
            <ModalBody>
              <Input
                autoFocus
                label='Connection string'
                variant='bordered'
                value={value}
                onValueChange={setValue}
              />
            </ModalBody>
            <ModalFooter>
              <Button
                onPress={onClose}
              >
                Cancel
              </Button>
              <Button
                color='primary'
                onPress={onClose}
                isDisabled={!value}
                onClick={() => joinGroup(value, setSent, onClose, setData, notification)}
                isLoading={sent}
              >
                Join
              </Button>
            </ModalFooter>
          </>
        )}
      </ModalContent>
    </Modal>
  )
}