canvas = document.getElementById('canvas');
ctx = canvas.getContext('2d');
ctx.lineWidth = 5;

function getPos(element) {
    let rect = element.getBoundingClientRect();
    return {y:rect.y, x:rect.x}
}

function getNormalizedPos(element) {
    let rect = element.getBoundingClientRect();
    rect.y = rect.y - getPos(canvas).y;
    rect.x = rect.x - getPos(canvas).x;
    return {y:rect.y, x:rect.x, height:rect.height, width:rect.width}

}

function getCenterPos(element) {
    let rect = element.getBoundingClientRect();
    let y = rect.y - getPos(canvas).y + rect.height/2;
    let x = rect.x - getPos(canvas).x + rect.width/2;
    return {x, y}
}

function start(lecture_id, color){
    ctx.beginPath();
    ctx.strokeStyle = color;

    let lecture = document.getElementById(lecture_id);
    let lecture_rect = getNormalizedPos(lecture);

    ctx.moveTo((lecture_rect.x + lecture_rect.width),(lecture_rect.y + lecture_rect.height/2));
    console.log('moved pencil to ', (lecture_rect.x + lecture_rect.width),(lecture_rect.y + lecture_rect.height/2))
}

function connect(node_id) {
    let node = document.getElementById(node_id);
    let nodePos = getCenterPos(node);

    ctx.lineTo((nodePos.x), nodePos.y)
}

function end(lecture_id) {

    let lecture = document.getElementById(lecture_id);
    let lecture_rect = getNormalizedPos(lecture);

    ctx.lineTo((lecture_rect.x), (lecture_rect.y + lecture_rect.height/2))
    ctx.stroke();
}