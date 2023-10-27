import { createContext, useEffect, useState } from 'react';

import Notification from '../components/Notification/Notification';
import '../components/Notification/Notification.css';

const NotificationContext = createContext();

const NotificationProvider = ({ children }) => {

    const [notifications, setNotifications] = useState({ elements: [], tops: [], closeIds: [] });

    function setHeight(id, height) {
        const n = notifications.elements.find(e => e.id === id);
        if (n != null) n.height = height
    }

    function make(type, title, text) {
        const id = `${Date.now()}${Math.random() * 100 | 0}`

        setNotifications((prev) => ({
            ...prev,
            elements: [{ id: id, title: title, text: text, type: type, height: 0 }, ...prev.elements]
        }))
    }

    function clear(id) {
        setNotifications((prev) => ({ ...prev, closeIds: [...prev.closeIds, id] }))
        setTimeout(() => {
            setNotifications((prev) => ({
            ...prev,
            elements: [...prev.elements.filter(e => (e.id !== id))],
            closeIds: [...prev.closeIds.filter(e => (e !== id))]
        }))
    }, 220)

        return false
    }

    useEffect(() => {
        setNotifications(prev => {
        let top = 0
        return ({
            ...prev,
            tops: prev.elements.map(e => {
                const value = top;
                if (!prev.closeIds.includes(e.id)) top += e.height;
                return value;
            })
        })
        })
    }, [notifications.elements])

    return (
        <NotificationContext.Provider value={{ make, clear, notifications, setNotifications }}>
            {children}
            <div className='notification-context__wrapper'>
                <div className='notification-context__wrapper--relative'>
                {notifications.elements.map((e, i) =>
                    <Notification
                    id={e.id}
                    key={e.id}
                    type={e.type}
                    title={e.title}
                    text={e.text}
                    top={notifications.tops[i]}
                    setHeight={setHeight}
                    closing={notifications.closeIds.includes(e.id)}
                    />
                )}
                </div>
            </div>
        </NotificationContext.Provider>
    )
}

export { NotificationProvider }
export default NotificationContext
