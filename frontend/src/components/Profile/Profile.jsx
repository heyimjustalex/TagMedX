'use client'
import { useMemo, useState } from 'react';
import { Avatar, Button, Card, CardBody, CardFooter, CardHeader, Divider, Input, Select, SelectItem } from '@nextui-org/react';

import { titles } from '../../consts/Titles';
import { NextColorMap } from '../../consts/NextColorMap';
import { checkEmail } from '../SignupForm/SignupFormUtils';
import { useNotification } from '../../hooks/useNotification';
import { specializations } from '../../consts/Specializations';
import { checkInitYear, compareChanges, handleSaveUser } from './ProfileUtils';

export default function Profile ({ data }) {

  const notification = useNotification();
  const [user, setUser] = useState(data);
  const [newUser, setNewUser] = useState(data);
  const [sent, setSent] = useState(false);

  const error = useMemo(() => {
    return {
      name: newUser.name === '',
      surname: newUser.surname === '',
      email: !checkEmail(newUser.e_mail),
      year: checkInitYear(newUser.practice_start_year)
    };
  }, [newUser]);

  return (
    <Card className='w-full max-w-xl min-w-0 h-fit'>
      <CardHeader className='flex flex-col gap-5 justify-center'>
        <Avatar
          className='sm:w-28 w-20 sm:h-28 h-20 sm:text-5xl text-2xl mt-2'
          fallback={`${newUser.name[0] || ''}${newUser.surname[0] || ''}`}
          color={NextColorMap[(((newUser.name.codePointAt(0) || 0) + (newUser.surname.codePointAt(0) || 0)) || -1) % 5 + 1]}
        />
        <div className='text-center'>
          <h1 className='text-xl'>{`${newUser.title || ''} ${newUser.name || ''} ${newUser.surname || ''}`}</h1>
          <p className='text-sm text-zinc-400'>{newUser.e_mail}</p>
        </div>
      </CardHeader>
      <Divider/>
      <CardBody className='flex gap-3'>
        <div className='flex flex-row gap-2'>
          <Select 
            size='sm'
            label='Title'
            selectionMode='single'
            selectedKeys={newUser.title ? new Set([newUser.title]) : new Set([])}
            onChange={e => setNewUser(prev => ({ ...prev, title: e.target.value || null }))}
            className='sm:max-w-[150px] max-w-[100px]'
          >
            {titles.map((t) => (
              <SelectItem key={t} value={t}>{t}</SelectItem>
            ))}
          </Select>
          <Input
            type='text'
            size='sm'
            label='Name'
            isInvalid={error.name}
            value={newUser.name}
            onChange={e => setNewUser(prev => { return { ...prev, name: e.target.value }})}
          />
        </div>
        <Input
          type='text'
          size='sm'
          label='Surname'
          isInvalid={error.surname}
          value={newUser.surname}
          onChange={e => setNewUser(prev => { return { ...prev, surname: e.target.value }})}
        />
        <div className='flex flex-row gap-2'>
          <Input
            type='text'
            size='sm'
            label='Initiation year'
            className='sm:max-w-[200px] max-w-[150px]'
            value={newUser.practice_start_year || ''}
            isInvalid={error.year}
            onChange={(e) => setNewUser(prev => ({ ...prev, practice_start_year: parseInt(e.target.value) || null }))}
          />
          <Select 
            size='sm'
            label='Specialization'
            selectionMode='single'
            selectedKeys={newUser.specialization ? new Set([newUser.specialization]) : new Set([])}
            onChange={e => setNewUser(prev => ({ ...prev, specialization: e.target.value || null }))}
          >
            {specializations.map((t) => (
              <SelectItem key={t} value={t}>{t}</SelectItem>
            ))}
          </Select>
        </div>
        <Input
          type='email'
          size='sm'
          label='Email'
          isInvalid={error.email}
          value={newUser.e_mail}
          onChange={e => setNewUser(prev => { return { ...prev, e_mail: e.target.value }})}
        />
      </CardBody>
      <Divider/>
      <CardFooter className='justify-around'>
        <Button
          className='flex'
          variant='light'
          color='primary'
          isDisabled={compareChanges(user, newUser)}
          onPress={() => setNewUser({ ...user })}
        >
          Discard
        </Button>
        <Button
          className='flex'
          variant='solid'
          color='primary'
          isDisabled={compareChanges(user, newUser) || (error.name || error.surname || error.email || error.year)}
          onPress={() => handleSaveUser(newUser, setSent, setUser, notification)}
          isLoading={sent}
        >
          Save
        </Button>
      </CardFooter>
    </Card>
  )
}