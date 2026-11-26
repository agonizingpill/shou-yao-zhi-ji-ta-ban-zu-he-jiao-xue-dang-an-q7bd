from domain.looms_api import router as looms
from domain.segments_api import router as segments
from domain.axes_api import router as axes
from domain.lesson_demos_api import router as lesson_demos

routers = (looms, segments, axes, lesson_demos,)
