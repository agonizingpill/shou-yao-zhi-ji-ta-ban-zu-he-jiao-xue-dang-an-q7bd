        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "踏板动作样段",
  "module": "动作样段",
  "caption": "动作样段",
  "detail": "教研员记录一次完整循环的左右脚频次和停顿。复核比对节拍后进入训练参考。",
  "path": "/segments",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "loom",
      "label": "织架"
    },
    {
      "name": "pattern",
      "label": "物料纹样"
    },
    {
      "name": "right_rate",
      "label": "右脚频次"
    },
    {
      "name": "left_rate",
      "label": "左脚频次"
    },
    {
      "name": "pause",
      "label": "踏间停顿 s"
    },
    {
      "name": "checked",
      "label": "已对拍"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "record_segment",
      "label": "登记课上样段",
      "path": "/segments/record-segment",
      "fields": [
        {
          "name": "code",
          "label": "样段编号",
          "kind": "text",
          "initial": "SEG-A"
        },
        {
          "name": "loom",
          "label": "织架号",
          "kind": "text",
          "initial": "LM-EAST"
        },
        {
          "name": "pattern",
          "label": "纹样",
          "kind": "text",
          "initial": "斜纹"
        },
        {
          "name": "right_rate",
          "label": "右脚频次",
          "kind": "float",
          "initial": 1.88
        },
        {
          "name": "left_rate",
          "label": "左脚频次",
          "kind": "float",
          "initial": 2.64
        },
        {
          "name": "pause",
          "label": "踏间停顿 s",
          "kind": "float",
          "initial": 0.62
        }
      ],
      "help": "样段编号可对应课上短片。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "verify_segment",
      "label": "复核样段对拍",
      "path": "/segments/verify-segment",
      "fields": [
        {
          "name": "segment",
          "label": "样段号",
          "kind": "text",
          "initial": "SEG-A"
        }
      ],
      "help": "复核员先核对短片手记，再确认记录。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "segments";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
