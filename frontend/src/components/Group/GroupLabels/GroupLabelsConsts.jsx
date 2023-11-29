export const columns = [
  {name: 'NAME', uid: 'name', sortable: true},
  {name: 'COLOR', uid: 'color', sortable: true},
  {name: 'DESCRIPTION', uid: 'description', sortable: false},
  {name: 'ACTIONS', uid: 'actions', sortable: false}
];

export const defaultLabelModal = {
  open: false,
  edit: false,
  name: '',
  color: new Set(),
  description: '',
}