import os
import shutil
import markdown
import sys
import yaml
import importlib.util
from timeit import default_timer as timer

BUILD_DRAFT = False
CURRENT_TEMPLATE = 'default'
CONTENT_DIR_PATH = 'content/'

def __init__():
    time_start = timer()
    global BUILD_DRAFT
    global CURRENT_TEMPLATE
    global CONTENT_DIR_PATH
    CONFIG_PATH = 'config.yml'
    # Read arguments:
    for raw_arg in sys.argv:
        if raw_arg.startswith('--'):
            arg = raw_arg[2:]
            match arg:
                case 'config-path':
                    CONFIG_PATH = arg.split('=')[1]
                case 'clean-output':
                    if os.path.isdir('output'):
                        shutil.rmtree('output')
    # Load config:
    if os.path.exists(CONFIG_PATH):
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file)
            for key in config:
                match key:
                    case 'build-draft':
                        BUILD_DRAFT = config[key]
                    case 'template':
                        CURRENT_TEMPLATE = config[key]
                    case 'content-dir':
                        CONTENT_DIR_PATH = config[key]
    # Create output directory if it does not exist:
    if not os.path.isdir('output'):
        os.mkdir('output')
        os.mkdir('output/posts')
    generate_posts(CURRENT_TEMPLATE, BUILD_DRAFT, CONTENT_DIR_PATH)
    time_end = timer()
    print('Done! Elapsed time: ', round(time_end - time_start, 4), 's', sep='')
    return

def generate_posts(current_template="default", build_draft=False, content_path="content/"):
    index_dict = {}
    index_arr = []
    file_iter = 0
    content_dir_scan = os.scandir(content_path)
    for file in content_dir_scan:
        # Check if valid file and file type:
        if file.is_file() and file.path.lower().endswith('.md'):
            with open(file.path, 'r') as f:
                md = markdown.Markdown(extensions=['meta'])
                html = md.convert(f.read())
                post_title = md.Meta["title"][0]
                post_summary = md.Meta["summary"][0]
                post_date = md.Meta["date"][0]
                post_edited = None
                if md.Meta.get('edited') is not None: # Check if post is edited:
                    post_edited = md.Meta.get('edited')[0]
                try: # Check if post is a draft:
                    is_draft = eval(md.Meta["draft"][0])
                    if is_draft and not build_draft:
                        continue
                except:
                    pass
                # Add to index dict:
                index_arr.append({
                        'title': post_title,
                        'date': post_date,
                        'edited': post_edited,
                        'summary': post_summary,
                        'html': html,
                        'filename': file.name.split('.')[0],
                        'path': file.path
                })
                file_iter += 1
    print('Read', file_iter, 'posts.')
    index_dict['posts'] = index_arr
    # Load builder from current template as a module:
    spec = importlib.util.spec_from_file_location('template', f'templates/{current_template}/builder.py')
    template = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(template)
    template.build(index_dict) # The template builder must have a mandatory build function.
    return

__init__()