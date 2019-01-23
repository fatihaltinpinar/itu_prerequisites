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
/*
var colorArray = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
		  '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
		  '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
		  '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
		  '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
		  '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
		  '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
		  '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
		  '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
		  '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];
 */
function start(lecture_id){
    ctx.beginPath();
    ctx.strokeStyle = '#ff0000';

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