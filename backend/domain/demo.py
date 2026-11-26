from domain.looms_model import looms
from domain.segments_model import segments
from domain.axes_model import axes
from domain.lesson_demos_model import lesson_demos


def _segment(code, loom, pattern, right, left, pause):
    return {'code': code, 'loom': loom, 'pattern': pattern, 'right_rate': right,
            'left_rate': left, 'pause': pause, 'checked': True, 'revoked': False}


FIXTURES = [
    (looms, [{'code': 'LM-EAST', 'machine': '红木二框', 'pedal_count': 4, 'mapping_signed': True},
 {'code': 'LM-WEST', 'machine': '松木四框', 'pedal_count': 6, 'mapping_signed': False}]),
    (segments, [_segment('SEG-00', 'LM-EAST', '平纹', 1.2, 3.2, .5),
 _segment('SEG-01', 'LM-EAST', '斜纹', 1.93, 2.67, .613),
 _segment('SEG-02', 'LM-EAST', '缎纹', 2.66, 2.14, .726),
 _segment('SEG-03', 'LM-EAST', '平纹', 1.29, 3.35, .539),
 _segment('SEG-04', 'LM-EAST', '斜纹', 1.9, 2.82, .652),
 _segment('SEG-05', 'LM-EAST', '缎纹', 2.63, 2.04, .765),
 _segment('SEG-06', 'LM-EAST', '平纹', 1.26, 3.25, .578),
 _segment('SEG-07', 'LM-EAST', '斜纹', 1.99, 2.72, .6),
 _segment('SEG-08', 'LM-EAST', '缎纹', 2.6, 2.19, .713),
 _segment('SEG-09', 'LM-EAST', '平纹', 1.23, 3.4, .526),
 _segment('SEG-10', 'LM-EAST', '斜纹', 1.96, 2.62, .639),
 _segment('SEG-11', 'LM-EAST', '缎纹', 2.69, 2.09, .752),
 _segment('SEG-12', 'LM-EAST', '平纹', 1.2, 3.3, .565),
 _segment('SEG-13', 'LM-EAST', '斜纹', 1.93, 2.77, .678),
 _segment('SEG-14', 'LM-EAST', '缎纹', 2.66, 2.24, .7),
 _segment('SEG-15', 'LM-EAST', '平纹', 1.29, 3.2, .513),
 _segment('SEG-16', 'LM-EAST', '斜纹', 1.9, 2.67, .626),
 _segment('SEG-17', 'LM-EAST', '缎纹', 2.63, 2.14, .739),
 _segment('SEG-18', 'LM-EAST', '平纹', 1.26, 3.35, .552),
 _segment('SEG-19', 'LM-EAST', '斜纹', 1.99, 2.82, .665),
 _segment('SEG-20', 'LM-EAST', '缎纹', 2.6, 2.04, .778),
 _segment('SEG-21', 'LM-EAST', '平纹', 1.23, 3.25, .5),
 _segment('SEG-22', 'LM-EAST', '斜纹', 1.96, 2.72, .613),
 _segment('SEG-23', 'LM-EAST', '缎纹', 2.69, 2.19, .726)]),
    (axes, [{'code': 'AXIS-01', 'segment': 'SEG-03', 'suggestion': '平纹',
  'confidence': 0.99, 'holdout': 0.93, 'token': 'AXIS-SEED-01', 'state': '有效'},
 {'code': 'AXIS-02', 'segment': 'SEG-09', 'suggestion': '平纹',
  'confidence': 0.97, 'holdout': 0.91, 'token': 'AXIS-SEED-02', 'state': '有效'}]),
    (lesson_demos, [{'code': 'LESSON-01', 'axis': 'AXIS-01', 'loom': 'LM-EAST',
  'lesson': '上午平纹练习', 'state': '已被替换', 'replaced_from': None},
 {'code': 'LESSON-02', 'axis': 'AXIS-02', 'loom': 'LM-EAST',
  'lesson': '上午平纹练习', 'state': '当前示范', 'replaced_from': 'LESSON-01'}]),
]
