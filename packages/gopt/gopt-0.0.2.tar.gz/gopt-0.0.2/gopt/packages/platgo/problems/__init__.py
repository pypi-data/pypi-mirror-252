from .multi_objective.Real_world_MOPs.Sparse_SR import Sparse_SR  # noqa: F401
from .multi_objective.Real_world_MOPs.Sparse_CD import Sparse_CD  # noqa: F401
from .multi_objective.selfDefineProblem1 import selfDefineProblem1
from .multi_objective.selfDefineProblem2 import selfDefineProblem2  # 无角度
from .multi_objective.selfDefineProblem3 import selfDefineProblem3  # 有角度
from .multi_objective.selfDefineProblem4 import selfDefineProblem4  # 折线
from .multi_objective.daily_planning import Daily_Planning  # 每日规划问题[一个时间窗]
from .multi_objective.daily_planning_strategy import Daily_Planning_Strategy  # 每日规划问题加修复策略[一个时间窗]
from .multi_objective.daily_planning2_strategy import Daily_Planning2_Strategy  # 每日规划问题贪心的解作为初始化解
from .multi_objective.daily_planning3_strategy import Daily_Planning3_Strategy  # 每日规划问题优化数据集的顺序
