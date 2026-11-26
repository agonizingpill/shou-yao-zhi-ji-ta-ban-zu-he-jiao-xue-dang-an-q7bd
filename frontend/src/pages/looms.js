        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "从织架开始校核脚位",
  "module": "织架与踏板对照",
  "caption": "织架与踏板对照",
  "detail": "机型的踏板布局由技师核实。跨织架替换讲义时，目标织架也须有签过的对照图。",
  "path": "/looms",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "machine",
      "label": "机型"
    },
    {
      "name": "pedal_count",
      "label": "踏板数"
    },
    {
      "name": "mapping_signed",
      "label": "脚位映射已签"
    }
  ],
  "layout": "flip",
  "view": "grid",
  "actions": [
    {
      "name": "sign_mapping",
      "label": "签认脚位对照",
      "path": "/looms/sign-mapping",
      "fields": [
        {
          "name": "loom",
          "label": "织架号",
          "kind": "text",
          "initial": "LM-WEST"
        },
        {
          "name": "mapping_note",
          "label": "脚位校核凭据",
          "kind": "text",
          "initial": "脚位图 A-219 双签"
        }
      ],
      "help": "填写带双签的纸本脚位图规格。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "looms";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
