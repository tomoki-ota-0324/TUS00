from django.views.generic import View
# from django.db.models import Q
from django.http.response import HttpResponse
# from django.core import serializers
import os

from sfacd.users.models import User
import geojson
import json
import numpy as np


class ReadLayerView(View):
    """
    large_maps.html readLayerを切り替えてデバッグ環境で使用、標準偏差と平均を出力
    """

    def get(self, request, *args, **kwargs):
        layer = request.GET['layer']
        age = request.GET['age_num']
        # path = os.path.abspath('sfacd/sfacd' + layer)
        path = os.path.abspath('sfacd' + layer)

        with open(path, encoding='utf-8') as f:
            data = geojson.load(f)

        print(data)
        l = []
        features = data["features"]
        for feature in features:
            l.append(feature.properties[age])
        while 0 in l:
            l.remove(0)
        while None in l:
            l.remove(None)
        np_arr = np.array(l)
        std_num = np.std(np_arr)
        print(std_num)
        mean_num = np.mean(np_arr)
        print(mean_num)

        data = {
            "layer": data,
            "std_num": std_num,
            "mean_num": mean_num
        }

        data = json.dumps(data)
        # print(data)
        return HttpResponse(data, content_type='application/json')
