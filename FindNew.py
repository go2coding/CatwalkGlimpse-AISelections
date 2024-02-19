import os
import re
from datetime import datetime, timedelta
import markdown

trending_dir = "./data/trending/"
new_dir = "./data/new/"
# 获取今天和昨天的日期并格式化为字符串
today = datetime.now().strftime("%Y-%m-%d")
year = today.split("-")[0]
month = today.split("-")[1]


project_urls = {}

if not os.path.isdir(new_dir + year + '/' + month):
    os.makedirs(new_dir + year + '/' + month)

old_files = []
# 遍历 '/data/trending' 目录及其所有子目录
for dirpath, dirnames, filenames in os.walk(trending_dir):
    # 遍历当前目录下的所有文件
    for filename in filenames:
        # 排除今天
        if today in filename:
            continue
        print(os.path.join(dirpath, filename))
        old_files.append(os.path.join(dirpath, filename))

def get_projects(filenames):


    result = {}

    for filename in filenames:
        # 使用 'with' 语句打开文件，这样可以确保文件在使用完毕后会被正确关闭
        if not os.path.exists(filename):
            continue
        with open(filename, 'r',encoding='utf-8') as file:
            text = file.read()

        # 使用正则表达式匹配类别和项目
        categories = re.split(r'#### ', text)[1:]

        print(filename)
        # 为每个类别添加项目
        for category in categories:
            lines = category.split('\n')
            category_name = lines[0].strip()
            projects = result.get(category_name,[])
            if category_name == 'python':
                print(projects)
            for line in lines[1:]:
                match = re.search(r'\* \[(.+)\]\((.+)\):(.*)', line)
                if match:
                    project_name, url, description = match.groups()
                    projects.append(project_name)
                    project_urls[project_name] = (url, description)
            result[category_name] = projects

    return result


# 读取今天和昨天的文件
year = today.split("-")[0]
month = today.split("-")[1]

today_file = trending_dir + year + '/' + month + '/' + f'{today}.md'
new_file = new_dir + year + '/' + month + '/' + f'{today}.md'

projects_today = get_projects([today_file])
projects_old = get_projects(old_files)


# 找出今天新增的项目并将其写入到新的文件中
with open(new_file, 'w',encoding='utf-8') as file:
    file.write("## " + today + "\n")
    for category, projects in projects_today.items():
        new_projects = set(projects) - set(projects_old.get(category, []))
        if new_projects:
            file.write(f'#### {category}\n')
            for project in new_projects:
                file.write(f'* [{project}]({project_urls[project][0]}):{project_urls[project][1]}\n')
