import {
  IconAlertTriangleFilled,
  IconCircleArrowDownRightFilled,
  IconCircleCheckFilled,
  IconForbidFilled,
  IconHelpHexagonFilled,
  IconInfoCircleFilled
} from '@tabler/icons-react';

import { NextColor } from '../../consts/NextColor';

export function getIcon(type) {
  switch(type) {
    case NextColor.DANGER: return <IconForbidFilled />;
    case NextColor.PRIMARY: return <IconInfoCircleFilled />;
    case NextColor.SECONDARY: return <IconHelpHexagonFilled />;
    case NextColor.SUCCESS: return <IconCircleCheckFilled />;
    case NextColor.WARNING: return <IconAlertTriangleFilled />;
    default: return <IconCircleArrowDownRightFilled />;
  }
}