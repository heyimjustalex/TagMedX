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

import { NextColor } from '../../../consts/NextColor';
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
            color={modal.color?.values()?.next()?.value}
            isRequired={!modal.edit}
            isInvalid={modal.edit && modal?.color?.size === 0}
            selectedKeys={modal.color}
            selectionMode='single'
            items={Object.values(NextColor)}
            onSelectionChange={e => setModal(prev => ({ ...prev, color: e }))}
            renderValue={(items) => {
              return items.map((item) =>
                <p key={item.key} className='capitalize'>{item.props.value}</p>
              );
            }}
          >
            {Object.values(NextColor).map((color) => (
              <SelectItem key={color} value={color} className={`capitalize text-${color}`}>
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
            isDisabled={!modal.name || modal?.color?.size === 0}
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