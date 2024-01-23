# -*- coding: utf-8 -*-

import datetime
from time import sleep, time

format_duration1 = lambda x:(datetime.datetime.utcfromtimestamp(x) + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
format_duration2 = lambda x:"%02d:%02d:%02d" % (x // 3600, (x % 3600) // 60, x % 60)

def progbar(ls):
    """
    监控任务进度
    :param ls: 可遍历对象
    """
    len_ls=len(ls)
    decpla=len(str(len_ls))
    start_time=time()
    i=1
    for l in ls:
        already_use_time = time()-start_time#已使用时间
        remain_tasks=len_ls-i#剩余任务
        estimate_remain_time=already_use_time/i*remain_tasks#预估剩余时间
        if i<11:
            print("\033[92m"+
                    f'总任务数：{len_ls}，'
                    f'当前已完成任务数：{i}，'
                    f'剩余任务数：{remain_tasks}，'
                    f'进度：{round(i * 100 / len_ls, decpla)}%，'
                    f'当前时间：{format_duration1(time())}'
                  +"\033[0m")
            yield l
        else:
            print("\033[92m"+
                    f'总任务数：{len_ls}，'
                    f'当前已完成任务数：{i}，'
                    f'剩余任务数{remain_tasks}，'
                    f'进度：{round(i*100/len_ls,decpla)}%，'
                    f'已用时间：{format_duration2(already_use_time)}，'
                    f'预估剩余时间：{format_duration2(estimate_remain_time)}，'
                    f'速度：{round(i/already_use_time,2)}s/it，'
                    f'当前时间：{format_duration1(time())}，'
                    f'预估完成时间：{format_duration1(time()+estimate_remain_time)}'
                  +"\033[0m")
            yield l
        i+=1