var current_chapter_index;
var current_page_index = 1;
var current_chapter = document.head.childNodes[5].data;
var image_locations = JSON.parse(document.head.childNodes[7].data);
for (let i = 0; i < image_locations.length; i++) {
    if (image_locations[i][0] === current_chapter) {
        current_chapter_index = i;
        break;
    }
}
function nextChapter() {
    current_chapter_index++;
    if (current_chapter_index >= image_locations.length) {
        current_chapter_index--;
        return true;
    }
    current_page_index = 1;
    current_chapter = image_locations[current_chapter_index][0];
    return false;
}
function previousChapterEnd() {
    current_chapter_index--;
    if (current_chapter_index < 0) {
        current_chapter_index++;
        return true;
    }
    current_page_index = image_locations[current_chapter_index].length - 1;
    current_chapter = image_locations[current_chapter_index][0];
    return false;
}
function previousChapterBeginning() {
    current_chapter_index--;
    if (current_chapter_index < 0) {
        current_chapter_index++;
        return true;
    }
    current_page_index = 1;
    current_chapter = image_locations[current_chapter_index][0];
    return false;
}
function nextPage() {
    current_page_index++;
    if (current_page_index >= image_locations[current_chapter_index].length) {
        if (nextChapter()) {
            current_page_index--;
        }
    }
}
function previousPage() {
    current_page_index--;
    if (current_page_index <= 0) {
        if (previousChapterEnd()) {
            current_page_index++;
        }
    }
}
function updatePage() {
    document.getElementById("image")
        .setAttribute("src", image_locations[current_chapter_index][current_page_index]);
    document.getElementById("chapter").innerText = current_chapter;
    document.getElementById("page").innerText = current_page_index;
    document.getElementById("numpages").innerText = image_locations[current_chapter_index].length - 1;
}
updatePage();
window.addEventListener('keydown', (key) => {
    switch (key.keyCode) {
        // left
        case 37:
            previousPage();
            updatePage();
            break;
        // up
        case 38:
            nextChapter();
            updatePage();
            break;
        // right
        case 39:
            nextPage();
            updatePage();
            break;
        // down
        case 40:
            previousChapterBeginning();
            updatePage();
            break;
    }
})
