window.onload = function() {
    const canvas = document.getElementById('gridCanvas');
    const context = canvas.getContext('2d');
    const gridSize = 20;
    let isDrawing = false;
    let startX, startY;
    let rectangles = [];
    let currentColor = '#000000';
    let image = new Image();
    let imgSrc = '';
    const templateNameInput = document.getElementById('templateName');
    const loadSelect = document.getElementById('loadSelect');

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
        context.clearRect(0,0,canvas.width,canvas.height)
        if (image.src) {
            context.drawImage(image, 0, 0, canvas.width, canvas.height); }
        drawGrid(context, canvas.width, canvas.height)
        rectangles.forEach(rect => {
            context.fillStyle = rect.color;
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

        rectangles.push({ startX, startY, width, height, color: currentColor });
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
        context.fillStyle = currentColor;
        context.fillRect(startX, startY, currentX - startX + gridSize, currentY - startY + gridSize);
    });

    // Save drawing to server
    document.getElementById('saveBtn').addEventListener('click', function()  {
        const templateName = templateNameInput.value.trim();
        if (templateName === '') {
            alert('Please enter a template name.');
            return;
        }
        fetch('/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: templateName, rectangles: rectangles, imageSource: imgSrc})
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Drawing saved successfully!');
                    loadTemplates();
                }
                else{
                    alert("Something went wrong.")
                }
            });
    });

    // Load drawing from server
    document.getElementById('loadBtn').addEventListener('click', () => {
        const selectedTemplate = loadSelect.value;
        if (selectedTemplate === '') {
            alert('Please select a template to load.');
            return;
        }
        fetch(`/load/${selectedTemplate}`)
            .then(response => response.json())
            .then(data => {
                rectangles = data.rectangles;
                imgSrc = data.imageSource;
                image.src = data.imageSource;

                if (imgSrc) {
                    const fileInput = document.getElementById('imageInput');


                    fileInput.addEventListener('change', function(event) {
                        const file = event.target.files[0];
                        if (file) {
                            const reader = new FileReader();
                            reader.onload = function(e) {
                                image.onload = function() {
                                    drawRectangles();
                                };
                                image.src = e.target.result;
                                imgSrc = file.name;
                            };
                            reader.readAsDataURL(file);
                        }
                    });
                } else {
                    drawRectangles();
                }
            });
    });
    // Handle color change
    document.querySelectorAll('.color-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            currentColor = event.target.getAttribute('data-color');
        });
    });

    // Load templates into the select element
    function loadTemplates() {
        fetch('/templates')
            .then(response => response.json())
            .then(data => {
                loadSelect.innerHTML = '<option value="">Select a template to load</option>';
                data.templates.forEach(template => {
                    const option = document.createElement('option');
                    option.value = template.name;
                    option.textContent = template.name;
                    loadSelect.appendChild(option);
                });
            });
    }


    imageInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                image.onload = function() {
                    drawRectangles();
                };
                image.src = e.target.result;
                imgSrc= file.name;
            };
            reader.readAsDataURL(file);
        }
    });



    draw();
    loadTemplates();
};
