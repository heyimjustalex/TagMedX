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

import { addSet } from './GroupSetsUtils';
import { typeOptions } from './GroupSetsConsts';
import { checkPackageSize } from './GroupSetsUtils';

export default function GroupSetsAddModal({ groupId, isOpen, onOpenChange, setData, notification }) {

  const [values, setValues] = useState({ name: '', type: new Set(), description: '', packageSize: '' });
  const [sent, setSent] = useState(false);
  const error = useMemo(() => checkPackageSize(values.packageSize), [values.packageSize]);

  return (
    <Modal 
      isOpen={isOpen}
      onOpenChange={() => { onOpenChange(); setValues({ name: '', type: new Set(), description: '', packageSize: '' })}}
      placement='top-center'
    >
      <ModalContent>
        {(onClose) => (
          <>
            <ModalHeader className='flex flex-col gap-1'>Create Set</ModalHeader>
            <ModalBody>
              <Input
                autoFocus
                isRequired
                label='Name'
                variant='bordered'
                value={values.name}
                onValueChange={e => setValues(prev => ({ ...prev, name: e }))}
              />
              <Select 
                isRequired
                label="Type" 
                selectedKeys={values.type}
                selectionMode='single'
                onSelectionChange={e => setValues(prev => ({ ...prev, type: e }))}
              >
                {typeOptions.map((type) => (
                  <SelectItem key={type.uid} value={type.name}>
                    {type.name}
                  </SelectItem>
                ))}
              </Select>
              <Input
                size='sm'
                isRequired
                type='text'
                label='Package size'
                value={values.packageSize}
                isInvalid={error}
                onChange={(e) => setValues(prev => ({ ...prev, packageSize: parseInt(e.target.value) || '' }))}
              />
              <Textarea
                isRequired
                minRows={2}
                label='Description'
                value={values.description}
                onChange={e => setValues(prev => ({ ...prev, description: e.target.value }))}
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
                isDisabled={!values.name || values.type?.size === 0 || error || !values.packageSize || !values.description}
                onClick={() => addSet(values, setSent, onClose, setData, groupId, notification)}
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