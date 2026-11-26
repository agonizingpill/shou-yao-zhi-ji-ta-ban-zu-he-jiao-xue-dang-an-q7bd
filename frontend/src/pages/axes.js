        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "不同纹样的判别轴",
  "module": "判别纠混签注",
  "caption": "判别纠混签注",
  "detail": "同台织架的已对拍样段沿监督判别轴布局。每组保留样段作验证。",
  "path": "/axes",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "segment",
      "label": "待辨动作"
    },
    {
      "name": "suggestion",
      "label": "判别纹样"
    },
    {
      "name": "confidence",
      "label": "模型概率"
    },
    {
      "name": "holdout",
      "label": "留出正确率"
    },
    {
      "name": "token",
      "label": "计算号"
    },
    {
      "name": "state",
      "label": "状态"
    }
  ],
  "layout": "split",
  "view": "grid",
  "actions": [
    {
      "name": "fit_axes",
      "label": "计算踏板判别轴",
      "path": "/axes/fit-axes",
      "fields": [
        {
          "name": "segment",
          "label": "样段号",
          "kind": "text",
          "initial": "SEG-A"
        }
      ],
      "help": "计算只使用同一台织架的三类已核对参考。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "record_axis",
      "label": "签注判别纠混",
      "path": "/axes/record-axis",
      "fields": [
        {
          "name": "code",
          "label": "签注号",
          "kind": "text",
          "initial": "AXIS-02"
        },
        {
          "name": "token",
          "label": "计算编号",
          "kind": "token",
          "initial": ""
        }
      ],
      "help": "置信和留出均合格才生成签注。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "axes";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
