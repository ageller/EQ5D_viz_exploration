document.addEventListener('DOMContentLoaded', function() {

    // for resizing by click-dragging the vertical divider
    const divider = document.getElementById('divider');
    const leftPanel = document.getElementById('survey-panel');
    const container = document.querySelector('.resizable-container');
    
    if (!divider || !leftPanel || !container) return;
    
    let isResizing = false;
    
    divider.addEventListener('mousedown', function(e) {
        isResizing = true;
        document.body.style.cursor = 'col-resize';
        e.preventDefault();
    });
    
    document.addEventListener('mousemove', function(e) {
        if (!isResizing) return;
        
        const containerRect = container.getBoundingClientRect();
        const newWidth = ((e.clientX - containerRect.left) / containerRect.width) * 100;
        
        if (newWidth > 1 && newWidth < 80) {
            leftPanel.style.flex = `0 0 ${newWidth}%`;
        }
    });
    
    document.addEventListener('mouseup', function() {
        if (isResizing) Shiny.setInputValue("redraw_trigger", Math.random(), {priority: "event"}); // triggers re-render of plots
        isResizing = false;
        document.body.style.cursor = 'default';
    });


    // hide slider until user interacts with it
    // this is somewhat hacky to wait until the slider is loaded
    // also hacky becuase it assumes only one slider in the survey
    // but since this is just a prototype, we can allow it.
    const waitForShiny = setInterval(() => {
        const survey_panel = document.getElementById('survey-panel');
        if (survey_panel) {
            // hide the slider components at first
            hide_slider();

            // add a listener on click to show components
            const el = document.getElementsByClassName('irs--shiny')[0];
            el.addEventListener('click', function() {
                // show the slider components 
                show_slider();
            });

            clearInterval(waitForShiny);
        }
    }, 500); // check every 0.5s

});

function hide_slider(index=0){
    const parentElement = document.getElementById('survey-panel');
    parentElement.querySelectorAll('.irs-handle')[index].classList.add('hidden');
    parentElement.querySelectorAll('.irs-single')[index].classList.add('hidden');
    parentElement.querySelectorAll('.irs-bar')[index].classList.add('hidden');
}
function show_slider(index=0){
    const parentElement = document.getElementById('survey-panel');
    parentElement.querySelectorAll('.irs-handle')[index].classList.remove('hidden');
    parentElement.querySelectorAll('.irs-single')[index].classList.remove('hidden');
    parentElement.querySelectorAll('.irs-bar')[index].classList.remove('hidden');
}

// I want to hide the slider when the user resets the survey
// I can't get the custom message handler to work.  The input fires, but it less elegant...
// Shiny.addCustomMessageHandler("hide_sliders", function(message) {
//     // enhancement: message could contain an index
//     // hide_slider();
//     console.log("message received", message)
// });

$(document).on('shiny:message', function(event) {
    if (event.message && event.message.inputMessages) {
        event.message.inputMessages.forEach(function(msg) {
            if (msg.id === 'js_command') {
                if (msg.message.action === 'hide_sliders') {
                    hide_slider();
                }
            }
        });
    }
});