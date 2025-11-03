#!/usr/bin/env python3
from pathlib import Path
import re
from typing import Set, List

def generate_index() -> None:
    """生成所有目录的导航页面"""
    base_dir: Path = Path('.')
    template: str = (base_dir / 'indexTemplate.html').read_text(encoding='utf-8')
    
    # 忽略的文件
    ignore_files: Set[str] = {'process_txt.py', 'generate_index.py', 'indexTemplate.html', 'template.html', 'index.html'}
    ignore_dirs: Set[str] = {'.git'}
    git_dir: Path = base_dir / '.git'
    for dirOfGit in git_dir.rglob('*'):
        if dirOfGit.is_dir():
            ignore_dirs.add(dirOfGit.name)
    def get_dir_content(directory: Path) -> str:
        """获取目录内容HTML"""
        title: str = directory.name
        html: List[str] = [f'        <div class="category">', f'            <h2>{title}</h2>', f'            <ul>']
        
        # 子目录
        for subdir in sorted([d for d in directory.iterdir() if d.is_dir()]):
            html.append(f'                <li><a href="{subdir.name}/index.html">{subdir.name}/</a></li>')
        
        # 文件
        for file in sorted([f for f in directory.iterdir() 
                          if f.is_file() and f.suffix in ['.html'] and f.name not in ignore_files]):
            html.append(f'                <li><a href="{file.name}">{file.stem}</a></li>')
        
        html.extend(['            </ul>', '        </div>'])
        return '\n'.join(html)
    
    # 为所有目录生成index.html
    directories: Set[Path] = {d for d in base_dir.rglob('*') if d.is_dir() and (d.name not in ignore_dirs)}
    print(list(d.name for d in directories))
    for directory in directories:
        content: str = get_dir_content(directory)
        html: str = re.sub(r'(<main>)(.*?)(</main>)', f'\\1\\n{content}\\n    \\3', template, flags=re.DOTALL)
        (directory / 'index.html').write_text(html, encoding='utf-8')
        print(f"生成: {directory}/index.html")

if __name__ == "__main__":
    generate_index()