var pressed;
var numbr = 0;

function draw(canvas, radius, angle) {
    ctx = canvas.getContext("2d");
    //ctx.beginPath();
    if (angle == 60){
        numbr += 1;
    }
    rad = angle*Math.PI/180;
    var x = canvas.width / 2 + radius * Math.cos(rad);
    var y = canvas.height / 2 + radius * Math.sin(rad);
    ctx.lineTo(x, y);
    ctx.stroke();
}

function stopDraw() {
    pressed = true;
    $("canvas").css("background-color", "white");
    $("#spiral").val(numbr);
    $("#button").prop('disabled',false);
    
}

window.addEventListener('DOMContentLoaded', () => {
    var canv = document.querySelector("canvas");
    var ctx = canv.getContext("2d");
    var startTime = null;
    let r = 2;
    var angle = 0;
    ctx.lineWidth = 10;
    ctx.strokeStyle = "#0096FF"; // blue-ish color
    ctx.beginPath();
    ctx.fillText("Click Me", canv.width / 3, canv.height / 2);
    
    document.addEventListener("keyup", (e) => {
        if(e.code == "Space"){
           stopDraw();
        }
    })
    
    function animate(timestamp) {
        ctx.font = "normal 24px serif"
        ctx.fillStyle = "pink";
        ctx.fillText("click here again when ready", canv.width / 15, canv.width/10);
        if (!startTime || timestamp - startTime >= 50) {
            startTime = timestamp;
        }
        let deltaTime = (timestamp - startTime);
        if (!pressed && timestamp < 30000) {
            if (deltaTime % 20 == 0) {
                if (angle == 360){
                    angle = 0;
                }
                draw(canv, r, angle);
                angle += 30;
                r += 0.5;
            }
            requestAnimationFrame(animate);
        } else {
            stopDraw();
        }
    }    
    canv.addEventListener('click', startSpin);
    function startSpin() {
        ctx.reset();
        $("canvas").css("background-color"," black");
        requestAnimationFrame(animate);
        canv.removeEventListener('click', startSpin);
        canv.addEventListener('click', stopDraw);
    }
})

