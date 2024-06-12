window.onload = function() {
    const canvas = document.getElementById('gridCanvas');
    const context = canvas.getContext('2d');
    const gridSize = 20;
    let isDrawing = false;
    let startX, startY;
    let rectangles = [];
    let currentDrawingId = null;

    // Draw the grid
    function drawGrid() {
        context.strokeStyle = '#ddd';
        for (let x = 0; x <= canvas.width; x += gridSize) {
            context.moveTo(x, 0);
            context.lineTo(x, canvas.height);
        }
        for (let y = 0; y <= canvas.height; y += gridSize) {
            context.moveTo(0, y);
            context.lineTo(canvas.width, y);
        }
        context.stroke();
    }

    // Draw all rectangles
    function drawRectangles() {
        rectangles.forEach(rect => {
            context.fillStyle = 'rgba(0, 0, 0, 0.5)';
            context.fillRect(rect.startX, rect.startY, rect.width, rect.height);
        });
    }

    // Main drawing function
    function draw() {
        // Clear the canvas
        context.clearRect(0, 0, canvas.width, canvas.height);
        drawGrid();
        drawRectangles();
    }

    canvas.addEventListener('mousedown', (event) => {
        isDrawing = true;
        startX = event.offsetX - (event.offsetX % gridSize);
        startY = event.offsetY - (event.offsetY % gridSize);
    });

    canvas.addEventListener('mouseup', (event) => {
        if (!isDrawing) return;
        isDrawing = false;
        const endX = event.offsetX - (event.offsetX % gridSize);
        const endY = event.offsetY - (event.offsetY % gridSize);

        const width = endX - startX + gridSize;
        const height = endY - startY + gridSize;

        rectangles.push({ startX, startY, width, height });
        draw();
    });

    canvas.addEventListener('mousemove', (event) => {
        if (!isDrawing) return;

        const currentX = event.offsetX - (event.offsetX % gridSize);
        const currentY = event.offsetY - (event.offsetY % gridSize);

        // Clear the canvas
        context.clearRect(0, 0, canvas.width, canvas.height);
        drawGrid();
        drawRectangles();

        // Draw the current rectangle
        context.fillStyle = 'rgba(0, 0, 0, 0.5)';
        context.fillRect(startX, startY, currentX - startX + gridSize, currentY - startY + gridSize);
    });

    // Save drawing to server
    document.getElementById('saveBtn').addEventListener('click', () => {
        fetch('/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rectangles: rectangles })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    currentDrawingId = data.id;
                    alert('Drawing saved successfully!');
                }
            });
    });

    // Load drawing from server
    document.getElementById('loadBtn').addEventListener('click', () => {
        fetch('/load')
            .then(response => response.json())
            .then(data => {
                const drawing = data.find(d => d.id === currentDrawingId);
                if (drawing) {
                    rectangles = drawing.rectangles;
                    draw();
                } else {
                    alert('No drawing found!');
                }
            });
    });

    draw();
};
