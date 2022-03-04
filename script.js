let css_root = document.querySelector(':root');
let base_colr_1 = css_root.style.getPropertyValue('--base-clr-1');
let base_colr_2 = css_root.style.getPropertyValue('--base-clr-2');

function toggle_color() {
    localStorage.toggle_color ^= true;
    determine_color();
}

function determine_color() {
    if (localStorage.toggle_color === "0") {
        css_root.style.setProperty('--base-clr-1', '#fffef9');
        css_root.style.setProperty('--base-clr-2', '#0C1821');
    } else {
        css_root.style.setProperty('--base-clr-1', '#0C1821');
        css_root.style.setProperty('--base-clr-2', '#fffef9');
    }
}

determine_color();