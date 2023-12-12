let css_root = document.querySelector(':root');
let base_colr_1 = css_root.style.getPropertyValue('--base-clr-1');
let base_colr_2 = css_root.style.getPropertyValue('--base-clr-2');
const LIGHT = '#fffef9';
const DARK = '#0C1821';

function toggle_color() {
    localStorage.toggle_color ^= true;
    determine_color();
}

function determine_color() {
    if (localStorage.toggle_color === "0") {
        css_root.style.setProperty('--base-clr-1', DARK);
        css_root.style.setProperty('--base-clr-2', LIGHT);
    } else {
        css_root.style.setProperty('--base-clr-1', LIGHT);
        css_root.style.setProperty('--base-clr-2', DARK);
    }
}

function color_index() {
    const posts = document.getElementsByClassName('post');
    let post_index = 0;
    for (post of posts) {
        if (post_index % 2 == 0) {
            post.classList.add('post-1');
        } else {
            post.classList.add('post-2');
        }
        post_index += 1;
    }
}

determine_color();