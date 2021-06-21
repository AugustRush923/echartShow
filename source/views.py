from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.options import InitOpts

from .models import Data


# Create your views here.


class CustomerInitOpts(InitOpts):
    def __init__(self):
        super(CustomerInitOpts, self).__init__()
        self.opts['width'] = "1900px"
        self.opts['height'] = "900px"
        self.opts['page_title'] = "hello world"


class AllView(View):
    def get(self, request):
        hscode = request.GET.get('hscode')
        if not hscode:
            return HttpResponseNotFound("not found")
        export_type = request.GET.get('export_type')
        if not export_type:
            export_type = "volume of exports"
        datas = Data.objects.filter(is_delete=True, hscode=hscode, export_type=export_type)
        if not datas:
            return HttpResponseNotFound("暂还未拥有此类数据，敬请期待。")
        data_2019 = [("2019年" + str(data.data_months) + "月", data.export_data_2019) for data in datas]
        data_2020 = [("2020年" + str(data.data_months) + "月", data.export_data_2020) for data in datas]
        data_2021 = [("2021年" + str(data.data_months) + "月", data.export_data_2021) for data in datas]
        all_data = data_2019 + data_2020 + data_2021

        x_axis = [data[0] for data in all_data]
        y_axis = [data[1] for data in all_data]

        c = (
            Line(init_opts=CustomerInitOpts())
                .add_xaxis(x_axis)
                .add_yaxis(series_name="出口量",
                           y_axis=y_axis,
                           markpoint_opts=opts.MarkPointOpts(
                               data=[
                                   opts.MarkPointItem(type_="max", name="最大值", symbol="roundRect",
                                                      symbol_size=[80, 50]),
                                   opts.MarkPointItem(type_="min", name="最小值", symbol="roundRect",
                                                      symbol_size=[80, 50]),
                               ]
                           ),
                           markline_opts=opts.MarkLineOpts(
                               data=[opts.MarkLineItem(type_="average", name="平均值")]
                           ),
                           )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="出口走势图", subtitle=f"{hscode}-{export_type}"),

            )
        )
        return HttpResponse(c.render_embed())


class SingleView(View):
    def get(self, request, hscode, year):
        print(hscode)
        if not all([hscode, year]):
            return HttpResponseNotFound("参数有误。")
        export_type = request.GET.get('export_type')
        if not export_type:
            export_type = "volume of exports"
        datas = Data.objects.filter(is_delete=True, hscode=hscode, export_type=export_type)
        y_axis = []
        x_axis = [str(data.data_months) for data in datas]
        if year == 2019:
            y_axis = [data.export_data_2019 for data in datas]
        elif year == 2020:
            y_axis = [data.export_data_2020 for data in datas]
        elif year == 2021:
            y_axis = [data.export_data_2021 for data in datas]

        c = (
            Line(init_opts=CustomerInitOpts())
                .add_xaxis(x_axis)
                .add_yaxis(series_name="出口量",
                           y_axis=y_axis,
                           markpoint_opts=opts.MarkPointOpts(
                               data=[
                                   opts.MarkPointItem(type_="max", name="最大值", symbol="roundRect",
                                                      symbol_size=[80, 50]),
                                   opts.MarkPointItem(type_="min", name="最小值", symbol="roundRect",
                                                      symbol_size=[80, 50]),
                               ]
                           ),
                           markline_opts=opts.MarkLineOpts(
                               data=[opts.MarkLineItem(type_="average", name="平均值")]
                           ),
                           )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="出口走势图", subtitle=f"{hscode}-{export_type}"),

            )
        )
        return HttpResponse(c.render_embed())
