import { useState } from 'react';
import { Button, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader } from '@nextui-org/react';

import { removeUser } from './GroupUsersUtils';

export default function GroupUsersModal({ modal, setModal, groupId, groupName, setData, notification }) {

  const [sent, setSent] = useState(false);

  return (
    <Modal
      hideCloseButton
      isOpen={modal.open}
      placement='top-center'
    >
      <ModalContent>
        {(onClose) => (
          <>
            <ModalHeader className='flex flex-col gap-1'>Remove User</ModalHeader>
            <ModalBody>
              {`Are you sure, you want to remove ${modal?.user?.name} ${modal?.user?.surname} from ${groupName}?`}
            </ModalBody>
            <ModalFooter>
              <Button
                isDisabled={sent}
                onPress={() => setModal(prev => { return { ...prev, open: false }})}
              >
                Cancel
              </Button>
              <Button
                color='danger'
                onPress={onClose}
                onClick={() => removeUser(modal.user, groupId, setModal, setSent, setData, notification)}
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
