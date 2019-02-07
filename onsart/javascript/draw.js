canvas = document.getElementById('canvas');
ctx = canvas.getContext('2d');
ctx.lineWidth = 3;
let offset = 5;
let lines = [];
let colors = [];
color_picker = [];


class Point {
    constructor(y, x){
        this.y = y;
        this.x = x;
    }

    get pos(){
        return {y:this.y, x:this.x}
    }

    move(y, x){
        this.y += y;
        this.x += x;
    }
}

class Line{
    constructor(y0, x0, y1, x1){
        let start = new Point(y0, x0);
        let end = new Point(y1, x1);
        this.startPoint = start;
        this.endPoint = end;
        // let conflict = false;
        let i = 0;
        while (i < lines.length){
            if(lines[i].startPoint.y === this.startPoint.y && lines[i].endPoint.y === this.endPoint.y){
                this.move(offset, 0);
                i = 0;
            }
            if(lines[i].startPoint.x === this.startPoint.x && lines[i].endPoint.x === this.endPoint.x){
                this.move(offset, 0);
                i = 0;
            }
            i++;
        }
        lines.push(this);
    }
    get getStart(){
        return {y:this.startPoint.y, x:this.startPoint.x}
    }
    get getEnd(){
        return {y:this.endPoint.y, x:this.endPoint.x}
    }
    move(y, x){
        this.startPoint.move(y, x);
        this.endPoint.move(y, x);
    }

    draw(){
        console.log('drawing wohoo');
    }
}

function getPos(element) {
    let rect = element.getBoundingClientRect();
    return {y:rect.y, x:rect.x}
}

function getCenterPos(element) {
    let rect = element.getBoundingClientRect();
    let y = rect.y - getPos(canvas).y + rect.height/2;
    let x = rect.x - getPos(canvas).x + rect.width/2;
    return {y, x}
}

function getElement(y, x) {
    let element_id = y + '_' + x;
    return document.getElementById(element_id);
}



    // script = f'connect({preq_y}, {preq_x}, {lect_y}, {lect_x});'
function connect(preq_y, preq_x, lect_y, lect_x) {



}



















/*

old python code


def connect(preq_y, preq_x, lect_y, lect_x):
    script = ''

    # start('0_0');connect('0_1');connect('1_1');connect('1_5');connect('0_5');end('0_6') // on same line
    # start('0_0');end('0_2') // side by side
    if preq_y == lect_y:

        if lect_x - preq_x == 2:
            script += f"start('{preq_y}_{preq_x}');"
            script += f"end('{lect_y}_{lect_x}');\n"

        else:
            script += f"start('{preq_y}_{preq_x}');"
            script += f"connect('{preq_y}_{preq_x + 1}');"
            script += f"connect('{preq_y + 1}_{preq_x + 1}');"
            script += f"connect('{lect_y + 1}_{lect_x - 1}');"
            script += f"connect('{lect_y}_{lect_x - 1}');"
            script += f"end('{lect_y}_{lect_x}');\n"

    # start('14_0');connect('14_preqx+1');connect('lecty+1_preqx+1');connect('1_13');connect('0_13');end('0_14');
    # // going up
    elif preq_y > lect_y:

        script += f"start('{preq_y}_{preq_x}');"
        script += f"connect('{preq_y}_{preq_x + 1}');"
        script += f"connect('{lect_y + 1}_{preq_x + 1}');"
        script += f"connect('{lect_y + 1}_{lect_x - 1}');"
        script += f"connect('{lect_y}_{lect_x - 1}');"
        script += f"end('{lect_y}_{lect_x}');\n"

    # start('0_0');connect('0_1');connect('5_1');connect('5_5');connect('6_5');end('6_6'); // going down
    elif preq_y < lect_y:

        script += f"start('{preq_y}_{preq_x}');"
        script += f"connect('{preq_y}_{preq_x + 1}');"
        script += f"connect('{lect_y - 1}_{preq_x + 1}');"
        script += f"connect('{lect_y - 1}_{lect_x - 1}');"
        script += f"connect('{lect_y}_{lect_x - 1}');"
        script += f"end('{lect_y}_{lect_x}');\n"
 */
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








// old javascript code

// function start(lecture_id){
//     ctx.beginPath();
//     ctx.strokeStyle = '#00ff00';
//
//     let lecture = document.getElementById(lecture_id);
//     let lecture_rect = getNormalizedPos(lecture);
//
//     ctx.moveTo((lecture_rect.x + lecture_rect.width),(lecture_rect.y + lecture_rect.height/2));
//     console.log('moved pencil to ', (lecture_rect.x + lecture_rect.width),(lecture_rect.y + lecture_rect.height/2))
// }
//
// function connect(node_id) {
//     let node = document.getElementById(node_id);
//     let nodePos = getCenterPos(node);
//
//     ctx.lineTo((nodePos.x), nodePos.y)
// }
//
// function end(lecture_id) {
//
//     let lecture = document.getElementById(lecture_id);
//     let lecture_rect = getNormalizedPos(lecture);
//
//     ctx.lineTo((lecture_rect.x), (lecture_rect.y + lecture_rect.height/2))
//     ctx.stroke();
// }