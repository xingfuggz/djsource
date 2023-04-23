#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :pushdata.py
@说明    :导入演示数据命令
@时间    :2023/04/23 14:52:45
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from . import _create

class Command(BaseCommand):
    
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "type", nargs="?", help="The path or URL to load the template from."
        )
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        # 添加商品分类
        print(options)
        if options.get("type") == "cates":
            _create.create_cates()
            self.stdout.write(self.style.SUCCESS(f'菜单演示数据添加成功！'))
        
        if options.get("type") == "spec":
            _create.create_specs()
            self.stdout.write(self.style.SUCCESS(f'规格数据添加成功！'))
            
        if options.get("type") == "spu":
            _create.create_spu()
            self.stdout.write(self.style.SUCCESS(f'spu添加成功！'))