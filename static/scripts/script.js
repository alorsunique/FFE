console.log('Hello World');




function initialize_image_list(){
    image_set = document.querySelectorAll(".thumbnail");
    return image_set
}


function add_image_listener(image_set){
    image_set.forEach(element => {
        // console.log(element)
        element.addEventListener('click',console.log('Hey'))
    });
}

function startup(){
    image_set = initialize_image_list();
    // console.log(image_set)
    add_image_listener(image_set);
}






document.addEventListener('DOMContentLoaded', () => {
    const fileBoxes = document.querySelectorAll('.selectable');

    fileBoxes.forEach(box => {
        box.addEventListener('click', () => {
            box.classList.toggle('selected');
        });
    });
});






document.addEventListener('DOMContentLoaded', () => {
    const videoThumbnails = document.querySelectorAll('video.thumbnail');

    videoThumbnails.forEach(video => {
        video.addEventListener('mouseenter', () => {
            video.currentTime = 0; // Start from beginning
            video.play();
        });

        video.addEventListener('mouseleave', () => {
            video.pause();
            video.currentTime = 0; // Reset to first frame
        });
    });
});




// Key for localStorage
const STORAGE_KEY = 'selectedFiles';

// Utility to load selection from storage
function loadSelection() {
    return new Set(JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]"));
}

// Utility to save selection to storage
function saveSelection(set) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...set]));
    console.log("Currently selected files:", [...set]);
}

// Initialize selection set
let selectedSet = loadSelection();

// Mark previously selected items on page load
window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.item_box.selectable').forEach(box => {
        const filePath = box.dataset.filePath;
        if (selectedSet.has(filePath)) {
            box.classList.add('selected');
        }

        // Click handler for selection toggle
        box.addEventListener('click', () => {
            if (selectedSet.has(filePath)) {
                selectedSet.delete(filePath);
                box.classList.remove('selected');
            } else {
                selectedSet.add(filePath);
                box.classList.add('selected');
            }
            saveSelection(selectedSet);
        });
    });
});


window.onload = function () {

    document.getElementById('export-button').addEventListener('click', () => {

        console.log("GETS")

        const selectedFiles = [...loadSelection()];

        fetch('/export_selection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selected: selectedFiles })
        })
        .then(response => {
            if (response.ok) {
                console.log("✅ Exported to server successfully.");
            } else {
                console.error("❌ Export failed.");
            }
        })
        .catch(error => console.error("Error:", error));
    });
};