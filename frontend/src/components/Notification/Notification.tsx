"use client"

import React from 'react'
import { Chip } from "@nextui-org/chip"
import { IconInfoCircleFilled, IconX } from '@tabler/icons-react';

import { NextColor } from '@/consts/NextColor';

import './Notification.css'

export default function Notification({ type }: { type?: NextColor }) {
  return (
    <Chip
        color={type}
        radius="md"
        variant="shadow"
        startContent={<IconInfoCircleFilled />}
        endContent={<IconX size={15} className="cursor-pointer" onClick={() => console.log("test")} />}
        className="w-96 p-2 mb-2 h-auto notification"
      >
        <h2 className="font-bold">Notification header</h2>
        <p className="whitespace-normal text-xs">Tutaj mamy treść notyfikacji</p>
      </Chip>
  )
}