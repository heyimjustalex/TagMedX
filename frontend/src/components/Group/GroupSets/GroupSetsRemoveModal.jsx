import { useState } from 'react';
import { Button, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader } from '@nextui-org/react';

import { removeSet } from './GroupSetsUtils';

export default function GroupSetsRemoveModal({ modal, setModal, setData, notification }) {

  const [sent, setSent] = useState(false);

  return (
    <Modal 
      isOpen={modal.open}
      placement='top-center'
    >
      <ModalContent>
        {(onClose) => (
          <>
            <ModalHeader className='flex flex-col gap-1'>Remove Set</ModalHeader>
            <ModalBody>
              {`Are you sure, you want to remove ${modal?.name}? This will also remove all packages, samples and examinations belonging to this set!`}
            </ModalBody>
            <ModalFooter>
              <Button
                isDisabled={sent}
                onPress={() => setModal(prev => ({ ...prev, open: false }))}
              >
                Close
              </Button>
              <Button
                color='danger'
                onPress={onClose}
                onClick={() => removeSet(modal.id, setModal, setSent, setData, notification)}
                isLoading={sent}
              >
                Remove
              </Button>
            </ModalFooter>
          </>
        )}
      </ModalContent>
    </Modal>
  )
}
