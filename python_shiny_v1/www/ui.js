document.addEventListener('DOMContentLoaded', function() {
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
        
        if (newWidth > 20 && newWidth < 80) {
            leftPanel.style.flex = `0 0 ${newWidth}%`;
        }
    });
    
    document.addEventListener('mouseup', function() {
        isResizing = false;
        document.body.style.cursor = 'default';
    });
});