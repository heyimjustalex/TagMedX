import { put } from '../../../utils/fetch';
import { NextColor } from '../../../consts/NextColor';

export async function savePackages(packages, setPackages, oldPackages, setData, notification) {

  const res = await Promise.all(
    packages
      .filter((e, i) => e.id_user !== oldPackages[i].id_user)
      .map(e => put(`packages/${e.id}/user/${e.id_user}`))
  )

  if(res.some(e => e.ok)) {
    const changed = new Array();
    const newPackages = oldPackages.map(e => {
      const response = res.find(r => r.body.id === e.id);
      if(response?.code === 200) {
        changed.push(response.body.id)
        return response.body;
      }
      else return e
    })

    setData(prev => ({ ...prev, packages: newPackages }));
    setPackages(newPackages);
    
    if(res.length === changed.length) {
      notification.make(
        NextColor.SUCCESS,
        `${changed.length > 1 ? 'Packages' : 'Package'} saved`,
        `You have successfully saved ${changed.length > 1 ? changed.length + ' packages owners' : '#' + changed[0] + ' package owner'}.`
      );
    } else {
      notification.make(
        NextColor.WARNING,
        'Partially saved',
        `You have successfully saved ${changed.length} out of ${res.length} requested packages owners.`
      );
    }
  }
  else {
    notification.make(NextColor.DANGER, 'Error', `Could not save ${res.length > 1 ? 'package owner.' : 'packages owners.'}.`);
  }
}