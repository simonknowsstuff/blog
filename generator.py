import os
import shutil
import markdown
from bs4 import BeautifulSoup
import datetime as dt

def read_template(filetype):
    if filetype == "index":
        with open('template/index.html') as f:
            return f.read()
    elif filetype == "post":
        with open('template/post.html') as f:
            return f.read()
    else: raise ValueError('filetype must be index or post')

def determine_post_class(item_index):
    if (item_index % 2) == 0: return str(1)
    else: return str(2)

def return_p_date(elem): return dt.datetime.strptime(elem.p.string, '%d-%m-%Y')

def generate_index():
    item_index = 0
    soup = BeautifulSoup(read_template('index'), "html.parser")
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
                
                new_div = soup.new_tag("div", **{'class':'post'})
                new_div_str = "<h3><a href=\"posts/{name}.html\">{title}</a></h3><p class=\"post_date\">{date}</p><p>{summ}</p>"
                new_div_str = new_div_str.format(name=item.name[:-3], title=post_title, date=post_date, summ=post_summary)
                new_div.append(BeautifulSoup(new_div_str, 'html.parser'))
                posts_tag.append(new_div)
                item_index += 1

    posts_date: list = soup.findAll('div', {'class': 'post'})
    posts_date.sort(key=lambda a: dt.datetime.strptime(a.p.string, '%d-%m-%Y'), reverse=True)
    posts_tag.clear()
    for post in posts_date:
        posts_tag.append(post)

    if not os.path.isdir("output"):
        os.mkdir('output')
    with open('output/index.html', 'w') as f:
        f.write(str(soup.prettify()))
    return

def generate_template_files():
    for file in os.scandir('template'):
        if file.is_file() and file.name != "index.html" and file.name != "post.html":
            shutil.copy2(file.path, 'output')
    return

def generate_posts():
    if not os.path.isdir('output/posts'):
        os.mkdir('output/posts')    
    for file in os.scandir('content'):
        if file.is_file() and file.path.lower().endswith('.md'):
            with open(file.path) as f:
                soup = BeautifulSoup(read_template('post'), 'html.parser')
                post_container = soup.find('div', {'id': 'post-container'})
                md = markdown.Markdown(extensions=['meta'])
                html = md.convert(f.read())

                # Replace post container tags with content
                post_title_tag = soup.find('h1', {'id': 'post-heading'})
                post_date_tag = soup.find('p', {'id': 'post-date'})
                post_title_tag.append(md.Meta['title'][0])
                post_date_tag.append(md.Meta['date'][0])
                # Change css reference to parent directory
                soup.find('link', {'rel': 'stylesheet', 'href': 'style.css'})['href'] = '../style.css'

                post_container.append(BeautifulSoup(html, 'html.parser'))
                with open("output/posts/{}.html".format(file.name[:-3]), 'w') as p:
                    p.write(str(soup.prettify()))


generate_index()
generate_template_files()
generate_posts()