import random
import copy
import numpy as np
from gopt.packages.platgo.Problem import Problem
from gopt.packages.platgo import Population


class Daily_Planning3_Strategy(Problem):
    """
    type = {"n_obj": "single", "encoding": "real"}
    """

    def __init__(self, in_optimization_problem, debug=True) -> None:
        optimization_problem = {
            "mode": 0,
            "encoding": "permutation",
            "n_obj": 3,
        }
        optimization_problem.update(in_optimization_problem)
        self.date_time = optimization_problem["date_time"]
        super(Daily_Planning3_Strategy, self).__init__(
            optimization_problem, debug=debug
        )

    def init_pop(self, N: int = None):
        if N is None:
            N = self.pop_size
        data = self.data[0]
        list1 = [_ for _ in range(len(data["scheduling_task"]))]
        decs = []
        for i in range(int(N * 0.4)):
            decs.append(random.sample(range(self.n_var), self.n_var))
        for j in range(int(N * 0.6)):
            decs += [list1]
        decs = np.array(decs)
        return Population(decs=decs)

    # def fix_decs(self, pop: Population):
    #     # 进行修复, 将开始时间早的往前排
    #     for i in range(len(pop)):
    #         pop.decs[i] = self.bubble_sort(pop.decs[i], self.task_start_time, self.index_task)
    #     return pop

    def compute(self, pop) -> None:
        objv = np.zeros((pop.decs.shape[0], self.n_obj))
        finalresult = np.empty((pop.decs.shape[0], 1), dtype=np.object)
        for i, x in enumerate(pop.decs):
            objv[i], finalresult[i] = self.main(x)

        pop.objv = objv
        pop.finalresult = finalresult
        pop.cv = np.zeros((pop.pop_size, self.n_constr))

    def main(self, x):
        data1 = self.data[0]
        data = copy.deepcopy(data1)
        # x = [9, 8, 12, 15, 13, 6, 3, 2, 4, 16, 7, 0, 5, 14, 11, 1, 17, 10]
        data["scheduling_task"] = [data["scheduling_task"][i] for i in x]
        next_times = 0
        task_info = dict()  # 记录每个任务的信息
        time_window_dict = dict()  # 记录每个任务的时间窗
        task_main_action = dict()  # 记录每个任务做的主动作的个数
        task_start_time = dict()
        index_task = dict()
        gantt_dict = dict()
        for i in range(0, len(data["scheduling_task"])):
            task_id = data["scheduling_task"][i]["task_id"]
            for _ in [k for k in range(i * 30 + 1, (i + 1) * 30 + 1)]:
                index_task[_] = task_id
        index_list = [i for i in range(1, len(data["scheduling_task"]) * 30 + 1, 30)]
        time_window_dict2 = dict()
        index1 = 1
        task_index_dict = dict()
        task_index1_dict = dict()
        for i in range(len(data["scheduling_task"])):
            task_index_dict[data["scheduling_task"][i]["task_id"]] = i + 1
            for t_v in data["scheduling_task"][i]["time_window"]:
                time_window_dict2[index1] = t_v
                task_index1_dict[index1] = data["scheduling_task"][i]["task_id"]
                index1 += 1
            time_window_dict[data["scheduling_task"][i]["task_id"]] = data["scheduling_task"][i]["time_window"]
            task_info[data["scheduling_task"][i]["task_id"]] = {
                "main_action_num": data["scheduling_task"][i]["main_action_num"],
                "main_action_time": data["scheduling_task"][i]["main_action_time"],
                "end_action": data["scheduling_task"][i]["end_action"],
                "next_action": data["scheduling_task"][i]["next_action"]
            }
            task_main_action[data["scheduling_task"][i]["task_id"]] = 0
        time_window_dict2 = dict(sorted(time_window_dict2.items(), key=lambda x: (x[1][0])))  # 按开始时间进行排序
        time_window_list2 = list()
        for key in time_window_dict2.keys():
            if task_index1_dict[key] not in time_window_list2:
                time_window_list2.append(task_index1_dict[key])
        index_list2 = [int(task_index_dict[i]) - 1 for i in time_window_list2]
        # sorted_tuples = sorted(zip(index_list2, index_list), key=lambda x: x[0])
        # 提取排序后的元素
        index_list = [index_list[i] for i in index_list2]
        index_list_dict = dict(zip(time_window_list2, index_list))
        index_list_dict2 = copy.deepcopy(index_list_dict)
        # index_list = np.array(index_list)[index_list2].tolist()
        start_time = list(time_window_dict2.values())[0][0]
        pre_task = list(time_window_dict2.keys())[0]
        for key, value in time_window_dict2.items():
            main_action_time = task_info[task_index1_dict[key]]["main_action_time"]  # 获取该任务的主动作时长
            end_action = task_info[task_index1_dict[key]]["end_action"]  # 获取该任务的后处理动作时长
            temp_time = float()
            temp = float()
            flag2 = False
            flag3 = True
            if task_index1_dict[pre_task] != task_index1_dict[key]:  # 发生切换
                next_action = task_info[task_index1_dict[pre_task]]["next_action"]  # 获取该任务的切换动作时长集合
                temp_time = max(task_info[task_index1_dict[pre_task]]["end_action"],
                                next_action[task_index_dict[task_index1_dict[key]] - 1])  # 上一个任务切换到该任务的时长
                start_time -= task_info[task_index1_dict[pre_task]]["end_action"]  # 先退回到上一个任务执行主动作完毕
                start_time += temp_time  # 当前任务的开始时间
                if start_time < value[0]:  # 开始时间在该任务时间窗之前
                    temp = value[0] - start_time
                    start_time = value[0]
                    if start_time + main_action_time > value[1]:
                        start_time -= temp
                        start_time -= temp_time
                        start_time += task_info[task_index1_dict[pre_task]]["end_action"]
                        continue  # 切换到当前任务失败，直接跳过该任务
                    else:
                        flag2 = True
                        next_times += 1  # 切换成功，次数加1
                elif value[0] <= start_time <= value[1]:  # 开始时间在窗口集合中间
                    if start_time + main_action_time > value[1]:
                        start_time -= temp_time
                        start_time += task_info[task_index1_dict[pre_task]]["end_action"]
                        continue  # 切换到当前任务失败，直接跳过该任务
                    else:
                        next_times += 1  # 切换成功，次数加1
                elif start_time > value[1]:  # 这里也是切换失败
                    start_time -= temp_time
                    start_time += task_info[task_index1_dict[pre_task]]["end_action"]
                    continue

            else:  # 没有发生切换【可能进行第一次】
                # if start_time < value[0]:
                #     if start_time + main_action_time > value[1]:
                #         continue
                #     start_time = value[0]
                #     flag3 = False
                if start_time + main_action_time < value[0] or start_time < value[0]:
                    if start_time + main_action_time > value[1]:
                        continue
                    start_time = value[0]
                    flag3 = False
                    print("=======================")
            if index_list_dict[task_index1_dict[key]] - index_list_dict2[task_index1_dict[key]] >= 30:  # 该窗口对应的任务全部做完
                # index_list_dict[task_index1_dict[key]] = index_list_dict2[task_index1_dict[key]]+29
                if flag2:
                    start_time -= temp
                if flag3:
                    start_time -= temp_time
                    next_times -= 1
                    start_time += task_info[task_index1_dict[pre_task]]["end_action"]
                continue

            while value[0] <= start_time + main_action_time <= value[1]:  # 初始时间加上主动作时长仍然在该任务的窗口内
                task_start_time[index_list_dict[task_index1_dict[key]]] = [start_time]
                task_main_action[task_index1_dict[key]] += 1  # 该任务的主动作次数加1
                start_time += main_action_time  # 加上该任务的主动作时长
                task_start_time[index_list_dict[task_index1_dict[key]]] += [start_time]
                start_time += end_action  # 加上该任务的后处理动作时长
                index_list_dict[task_index1_dict[key]] += 1
                if index_list_dict[task_index1_dict[key]] - index_list_dict2[
                    task_index1_dict[key]] >= 30:  # 该窗口对应的任务全部做完
                    break
            pre_task = key  # 存储为上一个任务
        for key, value in task_start_time.items():
            if key in index_task:
                gantt_dict.setdefault(index_task[key], []).append(
                    value
                )
        # info = self.check_overlap(gantt_dict, time_window_dict)
        obj1 = self.n_var * 30 - len(task_start_time)  # 统计总的主动作[最大化]
        obj2 = 1 - len(task_start_time) / 30 / len(gantt_dict)  # 每个任务的完成度之和的平均值[最大化]
        obj3 = next_times * 40  # 总的切换时长[最小化]
        return np.array([obj1, obj2, obj3]), f'{task_start_time}'

    def check_overlap(self, gantt_dict, time_window_dict):
        """
        检查优化后的时间窗是否与原时间窗的完全重叠
        :param gantt_dict:
        :param time_window_dict:
        :return:
        """
        info = dict()
        k = 0
        for key, value in gantt_dict.items():
            time_window = time_window_dict[key]
            for i in range(len(value)):
                v_s = value[i][0]  # 优化出的开始时间
                v_e = value[i][1]  # 优化出的结束时间
                for j in range(len(time_window)):
                    t_s = time_window[j][0]  # 原来的开始时间
                    t_e = time_window[j][1]  # 原来的结束时间
                    if (v_s < t_s < v_e and t_s < v_e < t_e) or (t_s < v_s < t_e and v_s < t_e < v_e) or (
                            v_s < t_s and v_e > t_e):
                        info[key] = [v_s, v_e, t_s, t_e]
                    k += 1
        return info
