import { put } from '../../../utils/fetch';

import { NextColor } from '../../../consts/NextColor';

export async function postSettings(settings, id, setSent, setData, notification) {
  setSent(true);
  
  const res = await put(`groups/${id}`, { name: settings.name, description: settings.description, connection_string: settings.connectionString });

  if(res.ok) {
    setData(prev => { return { ...prev, name: res.body.name, description: res.body.description, connection_string: res.body.connection_string }});
    setSent(false);
    notification.make(NextColor.SUCCESS, 'New settings', 'Settings successfully saved.');
  }
  else {
    setSent(false);
    notification.make(NextColor.DANGER, 'Error', 'Could not save settings.');
  }
}