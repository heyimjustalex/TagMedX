export const columns = [
  {name: 'NAME', uid: 'name', sortable: true},
  {name: 'TYPE', uid: 'type', sortable: true},
  {name: 'DESCRIPTION', uid: 'description', sortable: false},
  {name: 'ACTIONS', uid: 'actions', sortable: false}
];

export const typeOptions = [
  {name: 'Classification 	', uid: 'classification'},
  {name: 'Detection', uid: 'detection'}
];

export const defaultModal = { open: false, edit: false, name: '', type: new Set(), description: '', packageSize: ''};
