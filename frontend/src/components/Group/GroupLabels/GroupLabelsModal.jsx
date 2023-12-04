import { useState } from 'react';
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

import { NextCommonColor } from '../../../consts/NextCommonColor';
import { addLabel, editLabel } from './GroupLabelsUtils';

export default function GroupLabelsModal({ modal, setModal, setId, setData, notification }) {

  const [sent, setSent] = useState(false);

  return (
    <Modal
      hideCloseButton
      isOpen={modal.open}
      placement='top-center'
    >
      <ModalContent>
        <ModalHeader className='flex flex-col gap-1'>
          { modal.edit ? 'Edit Label' : 'Add Label' }
        </ModalHeader>
        <ModalBody>
          <Input
            autoFocus
            label='Name'
            value={modal.name}
            isRequired={!modal.edit}
            isInvalid={modal.edit && !modal.name}
            onValueChange={e => setModal(prev => ({ ...prev, name: e }))}
          />
          <Select 
            label="Color"
            isRequired={!modal.edit}
            selectedKeys={modal.color}
            selectionMode='single'
            items={Object.values(NextCommonColor)}
            onSelectionChange={e => setModal(prev => ({ ...prev, color: e }))}
            renderValue={(items) => {
              return items.map((item) =>
                <p key={item.key} className={item.props.className}>{item.props.value}</p>
              );
            }}
          >
            {Object.values(NextCommonColor).map((color) => (
              <SelectItem key={color} value={color} className={`capitalize text-${color}-500`}>
                {color}
              </SelectItem>
            ))}
          </Select>
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
            isDisabled={sent}
          >
            Cancel
          </Button>
          <Button
            color='primary'
            isDisabled={!modal.name}
            onClick={modal.edit
              ? () => editLabel(modal, setSent, setModal, setData, notification)
              : () => addLabel(modal, setSent, setModal, setData, setId, notification)
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