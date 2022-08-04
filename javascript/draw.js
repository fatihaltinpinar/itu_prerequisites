let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");

let lines = [];
let lastLect = null;
let color_picker = 0;

// You can change these values.
// Line thickness
ctx.lineWidth = 3;

// Space between line centers
let offset = 4;

// Colors that lines will have. Changes for every lecture that has prerequisites.
let colors = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
		  '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
		  '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
		  '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
		  '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
		  '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
		  '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
		  '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
		  '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
		  '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];

let offsets = [];
for (let i = 1; i*offset < 70; i++){
    if(i % 2 === 0){
        offsets.push(offset * i * (-1));
    }else{
        offsets.push(offset * i );
    }
}



class Point {
    constructor (y, x) {
        this.y = y;
        this.x = x;
    }

    get pos(){
        return {y:this.y, x:this.x}
    }

    get getY(){
        return this.y;
    }

    get getX(){
        return this.x;
    }
    move(y, x){
        this.y += y;
        this.x += x;
    }

    set setLineAfter (line) {
        this.lineAfter = line;
    }

    set setLineBefore (line) {
        this.lineBefore = line;
    }

    get getLineAfter () {
        return this.lineAfter;
    }

    get getLineBefore () {
        return this.lineBefore;
    }
}


function isConflictV(line1, line2) {
    if (line2.getStartPoint.getY < line1.getStartPoint.getY &&
        line2.getStartPoint.getY < line1.getEndPoint.getY &&
        line2.getEndPoint.getY < line1.getEndPoint.getY &&
        line2.getEndPoint.getY < line1.getStartPoint.getY){
        return false;
    }else if (line2.getStartPoint.getY > line1.getStartPoint.getY &&
        line2.getStartPoint.getY > line1.getEndPoint.getY &&
        line2.getEndPoint.getY > line1.getEndPoint.getY &&
        line2.getEndPoint.getY > line1.getStartPoint.getY){
        return false;
    }
    return true
}

function isConflictH(line1, line2) {
    if (line2.getStartPoint.getX < line1.getStartPoint.getX &&
        line2.getStartPoint.getX < line1.getEndPoint.getX &&
        line2.getEndPoint.getX < line1.getEndPoint.getX &&
        line2.getEndPoint.getX < line1.getStartPoint.getX){
        return false;
    }else if (line2.getStartPoint.getX > line1.getStartPoint.getX &&
        line2.getStartPoint.getX > line1.getEndPoint.getX &&
        line2.getEndPoint.getX > line1.getEndPoint.getX &&
        line2.getEndPoint.getX > line1.getStartPoint.getX){
        return false;
    }
    return true
}



class Line {
    constructor (startPoint, endPoint) {

        this.color = colors[color_picker];
        this.startPoint = startPoint;
        this.endPoint = endPoint;
        this.startPoint.setLineAfter = this;
        this.endPoint.setLineBefore = this;

        let k = 0;
        let conflict = true;

        // TODO:
        //  Write an function that returns if there is a conflict between two lines or not.
        //  Our problem is while lines are being drawn on a column lets say they move to side even if they dont collide
        //  at all.
        while (k < offsets.length && conflict) {
            conflict = false;
            let i = 0;
            while (i < lines.length) {
                if(lines[i].getColor !== this.color) {
                    if (lines[i].isVertical && this.isVertical &&
                        lines[i].startPoint.getX === this.startPoint.getX &&
                        isConflictV(lines[i], this)){
                            this.move(0, offsets[k]);
                            i = 0;
                            k++;
                            conflict = true;
                    }

                    if (lines[i].isHorizontal && this.isHorizontal &&
                        lines[i].startPoint.getY === this.startPoint.getY &&
                        isConflictH(lines[i], this)) {
                            this.move(offsets[k], 0);
                            i = 0;
                            k++;
                            conflict = true;
                    }
                }
                i++;
            }
        }
        if(conflict){
            console.log("Could not draw a line: ", this.getStartPoint.y, ',',
                        this.getStartPoint.x, ' - ',
                        this.getEndPoint.y, ',',
                        this.getEndPoint.x);
        }
        if(k === lines.length){
            console.log("Add more offsets plx!")
        }
        console.log("ses");
        lines.push(this);
    }


    get getStartPoint() {
        return this.startPoint;
    }
    get getEndPoint() {
        return this.endPoint;
    }

    get isVertical(){
        return this.startPoint.getX === this.endPoint.getX;
    }
    get isHorizontal(){
        return this.startPoint.getY === this.endPoint.getY;
    }
    get getColor(){
        return this.color;
    }
    move(y, x){
        this.startPoint.move(y, x);
        this.endPoint.move(y, x);
    }

    draw() {
        console.log("drawing line");
        ctx.beginPath();
        ctx.strokeStyle = this.color;
        ctx.moveTo(this.startPoint.x, this.startPoint.y);
        console.log('moved to ',this.startPoint.x,',', this.startPoint.y);
        ctx.lineTo(this.endPoint.x, this.endPoint.y);
        console.log('line to ',this.endPoint.x,',', this.endPoint.y);
        ctx.stroke();
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

function getElementSide(element, side) {
    // side = 1 means right
    let rect = element.getBoundingClientRect();
    let y = rect.y - getPos(canvas).y + rect.height / 2;
    let x = rect.x - getPos(canvas).x;
    if(side === 1){
        return {y:y, x:x + rect.width};
    }else {
        return {y:y, x:x};
    }
}

function createPoint(y, x) {
    let elem = getElement(y, x);
    let elemPos = getCenterPos(elem);
    return new Point(elemPos.y, elemPos.x);
}

    // script = f'connect({preq_y}, {preq_x}, {lect_y}, {lect_x});'
function connect(preq_y, preq_x, lect_y, lect_x) {

    if(lastLect === null){
        lastLect = {y:lect_y, x:lect_x}
    }else if(lastLect.y !== lect_y || lastLect.x !== lect_x){
        color_picker++;
        lastLect = {y:lect_y, x:lect_x};
    }



    let path = [];
    let path_lines = [];

    let preq = getElement(preq_y, preq_x);
    let start = new Point(getElementSide(preq, 1).y, getElementSide(preq, 1).x);
    path.push(start);

    if(lect_y === preq_y && (lect_x - preq_x) !== 2){
            path.push(createPoint(preq_y, preq_x + 1));
            path.push(createPoint(preq_y + 1, preq_x + 1));
            path.push(createPoint(lect_y + 1, lect_x - 1));
            path.push(createPoint(lect_y, lect_x - 1));
    }else if (preq_y > lect_y) {

        path.push(createPoint(preq_y, preq_x + 1));
        path.push(createPoint(lect_y + 1, preq_x + 1));
        path.push(createPoint(lect_y + 1, lect_x - 1));
        path.push(createPoint(lect_y, lect_x - 1));

    }else if(preq_y < lect_y){

        path.push(createPoint(preq_y, preq_x + 1));
        path.push(createPoint(lect_y - 1, preq_x + 1));
        path.push(createPoint(lect_y - 1, lect_x - 1));
        path.push(createPoint(lect_y, lect_x - 1));
    }

    let lect = getElement(lect_y, lect_x);
    let end = new Point(getElementSide(lect, -1).y, getElementSide(lect, -1).x);
    path.push(end);

    for(let i = 0; i < path.length - 1; i++){
        path_lines.push(new Line(path[i], path[i+1]));
    }

    for(let i = 0; i < path_lines.length; i++){
        path_lines[i].draw();
    }

}
