#!/usr/bin/env python3
from pathlib import Path
import re

def process_txt_files():
    # 读取模板文件
    work_dir = Path('.')
    template_path = Path('./template.html')
    template_content = template_path.read_text(encoding='utf-8')
    # 递归遍历所有txt文件
    for txt_file in work_dir.glob('**/*.txt'):
        print(f"处理文件: {txt_file}")
        
        # 读取txt内容
        txt_content = txt_file.read_text(encoding='utf-8')
        
        # 使用正则表达式替换模板中的content区域
        # 匹配 <div id="content"> 到 </div> 之间的内容
        pattern = r'(<div id="content">)(.*?)(</div>)'
        replacement = f'\\1{txt_content}\\3'
        
        # 执行替换
        html_content = re.sub(pattern, replacement, template_content, flags=re.DOTALL)
        
        # 生成html文件路径（同目录下，同名但扩展名为.html）
        html_file = txt_file.with_suffix('.html')
        
        # 写入html文件（覆盖模式）
        html_file.write_text(html_content, encoding='utf-8')
        print(f"生成文件: {html_file}")

if __name__ == "__main__":
    process_txt_files()