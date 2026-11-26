        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "讲义的示范版本",
  "module": "课堂示范册",
  "caption": "课堂示范册",
  "detail": "替换旧示范会同步更改两张签条。跨织架脚位未签时整次替换被拒绝。",
  "path": "/lesson_demos",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "axis",
      "label": "判别依据"
    },
    {
      "name": "loom",
      "label": "示范织架"
    },
    {
      "name": "lesson",
      "label": "节次"
    },
    {
      "name": "state",
      "label": "状态"
    }
  ],
  "layout": "stack",
  "view": "stack",
  "actions": [
    {
      "name": "replace_demo",
      "label": "替换示范动作",
      "path": "/lesson_demos/replace-demo",
      "fields": [
        {
          "name": "code",
          "label": "新示范编号",
          "kind": "text",
          "initial": "LESSON-02"
        },
        {
          "name": "axis",
          "label": "签注号",
          "kind": "text",
          "initial": "AXIS-02"
        },
        {
          "name": "loom",
          "label": "目标织架",
          "kind": "text",
          "initial": "LM-WEST"
        },
        {
          "name": "lesson",
          "label": "节次",
          "kind": "text",
          "initial": "上午平纹练习"
        },
        {
          "name": "previous",
          "label": "替换的旧示范",
          "kind": "text",
          "initial": "LESSON-01"
        }
      ],
      "help": "当前讲义节次与旧示范必须属于同一课。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "restore_demo",
      "label": "退回此前的示范",
      "path": "/lesson_demos/restore-demo",
      "fields": [
        {
          "name": "demo",
          "label": "当前示范",
          "kind": "text",
          "initial": "LESSON-02"
        },
        {
          "name": "older",
          "label": "回退的示范",
          "kind": "text",
          "initial": "LESSON-01"
        }
      ],
      "help": "旧示范复用训练场次保持不变。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "lesson_demos";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
