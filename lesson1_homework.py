import requests
import re
import numpy as np
import json

import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

r = requests.get('http://map.amap.com/service/subway?_1469083453978&srhdata=1100_drw_beijing.json')
#r.text
string1 = json.loads(r.text)   #loads:把json转换为dict
print(string1 )


#得到路线信息
def get_lines_stations_info(string1):
    lines_info = {}
    stations_info = {}

    for line in string1['l']:
        line_name = line['kn']
        lines_info[line_name] = [i['n'] for i in line['st']]
        for i in line['st']:
            x_y = re.findall("(\d+.\d+),(\d+.\d+)", i['sl'])[0]
            stations_info[i['n']] = tuple(map(float, x_y))

    return lines_info, stations_info


lines_info, stations_info = get_lines_stations_info(string1)


# 根据线路信息，建立站点邻接表dict

def get_neighbor_info(lines_info):
    neighbor_info = {}

    for sta in lines_info.values():  # 路线的站点循环
        for k, v in enumerate(sta):
            tmp_list = []

            if k == 0:
                if v in neighbor_info:
                    tmp_list = neighbor_info[v]
                    tmp_list.append(sta[k + 1])
                else:
                    tmp_list.append(sta[k + 1])

                neighbor_info[v] = tmp_list

            elif k == len(sta) - 1:
                if v in neighbor_info:
                    tmp_list = neighbor_info[v]
                    tmp_list.append(sta[k - 1])
                else:
                    tmp_list.append(sta[k - 1])

                neighbor_info[v] = tmp_list

            else:
                if v in neighbor_info:
                    tmp_list = neighbor_info[v]
                    tmp_list.append(sta[k + 1])
                    tmp_list.append(sta[k - 1])

                else:
                    tmp_list.append(sta[k + 1])
                    tmp_list.append(sta[k - 1])
                    neighbor_info[v] = tmp_list

    return neighbor_info

#如果汉字无法显示，请参照
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'

plt.figure(figsize=(40,30))



def get_path_BFS(lines_info, neighbor_info, from_station, to_station):
    pathes = [[from_station]]
    visited = set()

    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]

        if froniter in visited: continue

        sucesssors = neighbor_info[froniter]

        for sta in sucesssors:
            if sta in path: continue  # 检查是否已经遍历过

            new_path = path + [sta]

            pathes.append(new_path)  # bfs

            if sta == to_station:
                return new_path
        visited.add(froniter)

neighbor_info = get_neighbor_info(lines_info)
station_graph = nx.Graph(neighbor_info)
nx.draw(station_graph, stations_info,with_labels=True)
plt.show

print(get_path_BFS(lines_info,neighbor_info,'望京','大井'))
