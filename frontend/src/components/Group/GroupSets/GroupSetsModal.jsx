import { useMemo, useState } from 'react';
import {
  Button,
  Input,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Select,
  SelectItem,
  Textarea
} from '@nextui-org/react';

import { addSet, editSet } from './GroupSetsUtils';
import { typeOptions } from './GroupSetsConsts';
import { checkPackageSize } from './GroupSetsUtils';

export default function GroupSetsModal({ modal, setModal, groupId, setData, notification }) {

  const [sent, setSent] = useState(false);
  const error = useMemo(() => checkPackageSize(modal.packageSize), [modal.packageSize]);

  return (
    <Modal 
      isOpen={modal.open}
      placement='top-center'
    >
      <ModalContent>
        <ModalHeader className='flex flex-col gap-1'>
          { modal.edit ? 'Edit Set' : 'Create Set' }
        </ModalHeader>
        <ModalBody>
          <Input
            autoFocus
            label='Name'
            value={modal.name}
            isRequired={!modal.edit}
            onValueChange={e => setModal(prev => ({ ...prev, name: e }))}
          />
          <Select 
            label="Type"
            isDisabled={modal.edit}
            isRequired={!modal.edit}
            selectedKeys={modal.type}
            selectionMode='single'
            onSelectionChange={e => setModal(prev => ({ ...prev, type: e }))}
          >
            {typeOptions.map((type) => (
              <SelectItem key={type.uid} value={type.name}>
                {type.name}
              </SelectItem>
            ))}
          </Select>
          <Input
            size='sm'
            type='text'
            label='Package size'
            isDisabled={modal.edit}
            isRequired={!modal.edit}
            value={modal.packageSize}
            isInvalid={error}
            onChange={(e) => setModal(prev => ({ ...prev, packageSize: parseInt(e.target.value) || '' }))}
          />
          <Textarea
            minRows={2}
            label='Description'
            isRequired={!modal.edit}
            value={modal.description}
            onChange={e => setModal(prev => ({ ...prev, description: e.target.value }))}
          />
        </ModalBody>
        <ModalFooter>
          <Button
            onPress={() => setModal({ open: false, edit: false })}
          >
            { modal.edit ? 'Cancel' : 'Close' }
          </Button>
          <Button
            color='primary'
            isDisabled={!modal.name || modal.type?.size === 0 || error || !modal.packageSize || !modal.description}
            onClick={modal.edit
              ? () => editSet(modal, setSent, setModal, setData, groupId, notification)
              : () => addSet(modal, setSent, setModal, setData, groupId, notification)
            }
            isLoading={sent}
          >
            { modal.edit ? 'Save' : 'Create' }
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  )
}