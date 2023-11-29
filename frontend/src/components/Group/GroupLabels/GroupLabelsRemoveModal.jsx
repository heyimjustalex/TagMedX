import { useState } from 'react';
import { Button, Chip, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader } from '@nextui-org/react';

import { removeLabel } from './GroupLabelsUtils';

export default function GroupLabelsRemoveModal({ modal, setModal, setData, notification }) {

  const [sent, setSent] = useState(false);

  return (
    <Modal 
      hideCloseButton
      isOpen={modal.open}
      placement='top-center'
    >
      <ModalContent>
        <ModalHeader className='flex flex-col gap-1'>Remove Label</ModalHeader>
        <ModalBody>
          Are you sure, you want to remove label: {
            <Chip className='capitalize' color={modal.color || 'default'} size='sm' variant='flat'>
              {modal.name || 'default'}
            </Chip>
          } This will cause deletion all bounding boxed marked this label.
        </ModalBody>
        <ModalFooter>
          <Button
            isDisabled={sent}
            onPress={() => setModal({ open: false, edit: false })}
          >
            Cancel
          </Button>
          <Button
            color='danger'
            onPress={() => removeLabel(modal.id, setModal, setSent, setData, notification)}
            isLoading={sent}
          >
            Remove
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  )
}
