        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "撤销对拍影响台账",
  "module": "撤销对拍",
  "caption": "撤销对拍影响台账",
  "detail": "每次撤销登记受牵连的节次与原签注：作废签注、待复核签注、被拦下的计算号，以及示范回退或停用结果。重复撤销按事件重放，不重复回退。",
  "path": "/revocations",
  "columns": [
    {
      "name": "id",
      "label": "撤销号"
    },
    {
      "name": "segment",
      "label": "被撤销样段"
    },
    {
      "name": "actor",
      "label": "复核员"
    },
    {
      "name": "at",
      "label": "撤销时间"
    },
    {
      "name": "impact",
      "label": "影响（节次与原签注）"
    }
  ],
  "layout": "stack",
  "view": "stack",
  "actions": []
};

        export const {title} = page;
        export const key = "revocations";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
