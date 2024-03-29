import os
import shutil
import markdown
import sys
from bs4 import BeautifulSoup as bsoup
import datetime as dt

BUILD_DRAFT = False
CURRENT_TEMPLATE_PATH = 'templates/default/'

def read_template(filetype):
    if filetype == 'index':
        with open(f'{CURRENT_TEMPLATE_PATH}index.html') as f:
            return f.read()
    elif filetype == 'post':
        with open(f'{CURRENT_TEMPLATE_PATH}post.html') as f:
            return f.read()
    raise ValueError('filetype must be index or post')

def return_p_date(elem):
    return dt.datetime.strptime(elem.p.string, '%d-%m-%Y')

def generate_index():
    soup = bsoup(read_template('index'), 'html.parser')
    posts_tag = soup.find('div', {'id': 'posts'})
    content_dir_scan = os.scandir('content')
    # Setting up references in the index
    for item in content_dir_scan:
        if item.is_file():
            with open(item.path) as f:
                md = markdown.Markdown(extensions = ['meta'])
                md.convert(f.read())
                # md.Meta to access metadata
                # [0] to only access the first string
                post_title = md.Meta["title"][0]
                post_summary = md.Meta["summary"][0]
                post_date = md.Meta["date"][0]
                is_draft = eval(md.Meta["draft"][0])
                if is_draft and not BUILD_DRAFT:
                    continue                
                new_div = soup.new_tag("div", **{'class':'post'})
                new_div_str = "<h3><a href=\"posts/{name}.html\">{title}</a></h3><p class=\"post_date\">{date}</p><p>{summ}</p>"
                new_div_str = new_div_str.format(name=item.name[:-3], title=post_title, date=post_date, summ=post_summary)
                new_div.append(bsoup(new_div_str, 'html.parser'))
                posts_tag.append(new_div)

    posts_date: list = soup.findAll('div', {'class': 'post'})
    posts_date.sort(key=lambda a: dt.datetime.strptime(a.p.string, '%d-%m-%Y'), reverse=True)
    posts_tag.clear()
    for post in posts_date:
        posts_tag.append(post)
    with open('output/index.html', 'w') as f:
        f.write(str(soup.prettify()))
    return

def generate_template_files():
    for file in os.scandir(CURRENT_TEMPLATE_PATH):
        if file.is_file() and file.name not in ["index.html","post.html"]:
            shutil.copy2(file.path, 'output')
    return

def generate_static_content():
    if not os.path.isdir('output/static'):
        os.mkdir('output/static')
    for file in os.scandir('static'):
        shutil.copy2(file.path, 'output/static')
    return

def generate_posts():
    for file in os.scandir('content'):
        if file.is_file() and file.path.lower().endswith('.md'):
            with open(file.path) as f:
                soup = bsoup(read_template('post'), 'html.parser') # Template soup
                post_container = soup.find('div', {'id': 'post-container'})
                md = markdown.Markdown(extensions = ['meta'])
                html = md.convert(f.read())
                is_draft = eval(md.Meta["draft"][0]) # Check if post is a draft
                if is_draft and not BUILD_DRAFT:
                    continue

                # Replace post container tags with content
                post_heading_tag = soup.find('h1', {'id': 'post-heading'})
                post_date_tag = soup.find('p', {'id': 'post-date'})
                post_title_tag = soup.find('title')
                post_heading_tag.append(md.Meta['title'][0])
                post_date_tag.append('Published on: ' + md.Meta['date'][0])
                if md.Meta.get('edited') is not None:
                    post_date_tag.append(' | Edited on: ' + md.Meta.get('edited', [''])[0])
                post_title_tag.append(md.Meta['title'][0])
                # Change css reference to parent directory
                soup.find('link', {'rel': 'stylesheet', 'href': 'style.css'})['href'] = '../style.css'
                psoup = bsoup(html, 'html.parser')

                ''''
                Note:
                For now, the program only expects image tags and files in their respective files / folders.
                But I may update it in the future to check for other files like audio or video.
                The code below just redirects the sources of the tags to the static directory.
                '''         
                img_sources = []

                for img in psoup.find_all('img'):
                    if img['src'] not in img_sources and img['src'].startswith('static/'):
                        img_sources.append(img['src'])
                for link in img_sources:
                    count = 0
                    for img in psoup.find_all('img', {'src': link}):
                        img_path = img['src']
                        img['id'] = img_path[len('static/'):] + str(count)
                        img['src'] = '../' + img_path
                        if img.parent.name != 'div': # Change parent to an image container
                            img.parent.name = 'div'
                            img.parent['class'] = 'img-container'
                        count += 1

                # Open all links in new tab
                for anchor in psoup.find_all('a'):
                    if not anchor['href'].startswith('../'): # Avoid links to the website itself
                        anchor['target'] = '_blank'
                
                post_container.append(psoup)
                with open("output/posts/{}.html".format(file.name[:-3]), 'w') as p:
                    # Used to use prettify() over here, but it seems to be interfering with the whitespace of code tags
                    p.write(str(soup))
    return


def main():
    arg_index = 0
    for raw_arg in sys.argv:
        if raw_arg.startswith('--'):
            arg = raw_arg[2:]
            match arg:
                case 'build-draft':
                    global BUILD_DRAFT 
                    BUILD_DRAFT = True
                case 'clean-output':
                    if os.path.isdir('output'):
                        shutil.rmtree('output')
                case 'template':
                    template = sys.argv[arg_index + 1]
                    # Check if template exists in directory:
                    if os.path.isdir('templates/' + template):
                        global CURRENT_TEMPLATE_PATH
                        CURRENT_TEMPLATE_PATH = 'templates/{}/'.format(template)
                    print(CURRENT_TEMPLATE_PATH)
        arg_index += 1

    if not os.path.isdir('output'):
        os.mkdir('output')
        os.mkdir('output/posts')
    generate_index()
    generate_template_files()
    generate_static_content()
    generate_posts()
    return

main()