from django.db import models

# Create your models here.

# months = ((str(i) + '月' for i in range(1, 13)), (i for i in range(1, 13)))


class Data(models.Model):
    MONTHS_CHOICES = (zip((i for i in range(1, 13)),(str(i) + '月' for i in range(1, 13))))
    TYPES_CHOICES = (
        ("volume of exports", "出口量"),
        ("value of exports", "出口额")
    )
    STATUS_CHOICES = (
        (True, '正常'),
        (False, '删除'),
    )
    data_months = models.PositiveSmallIntegerField(choices=MONTHS_CHOICES, verbose_name="月份")
    hscode = models.CharField(max_length=20, verbose_name='HsCode')
    export_data_2019 = models.PositiveIntegerField(verbose_name="2019年数据", null=True, blank=True)
    export_data_2020 = models.PositiveIntegerField(verbose_name="2020年数据", null=True, blank=True)
    export_data_2021 = models.PositiveIntegerField(verbose_name="2021年数据", null=True, blank=True)
    product_name = models.CharField(max_length=128, verbose_name="产品名", null=True, blank=True)
    export_type = models.CharField(max_length=128, choices=TYPES_CHOICES, verbose_name="出口类型")
    unit = models.CharField(max_length=20, verbose_name="单位")

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    is_delete = models.BooleanField(verbose_name='状态', default=False, choices=STATUS_CHOICES)

    class Meta:
        db_table = "source_data"
        verbose_name_plural = verbose_name = "出口数据总量"

    def __str__(self):
        return self.product_name + self.export_type
