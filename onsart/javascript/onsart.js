let courseDict = {}
 // create an array with nodes
var nodes = new vis.DataSet([]);
// create an array with edges
var edges = new vis.DataSet([]);



color_completed = {
      border: '#ff9900',
      background: '#ffbd38',
      highlight: {
        border: '#ff9900',
        background: '#ffbd38'
      },
      hover: {
        border: '#ff9900',
        background: '#ffbd38'
      }
    }
color_selectable = {
    border: '#d4bd8e',
    background: '#f0d9aa',
    highlight: {
        border: '#d4bd8e',
        background: '#f0d9aa'
    },
    hover: {
        border: '#d4bd8e',
        background: '#f0d9aa'
    },
}
color_nonselectable = {
    border: '#9c9a94',
    background: '#bab9b6',
    highlight: {
        border: '#9c9a94',
        background: '#bab9b6'
    },
    hover: {
        border: '#9c9a94',
        background: '#bab9b6'
    },
}


class Course{
    constructor(id, semester, preqs){
        this.id = id;
        this.semester = semester;
        this.preqs = [];
        this.isSelectable = false;
        this.isCompleted = false;
        this.preqTo = [];
        nodes.update({id:this.id, level: this.semester, label:this.id, title:"course name goes here"});

        var table = document.getElementById("semester"+this.semester);
        var row = table.insertRow(1);
        row.id = this.id;
        row.onclick = function() {courseDict[this.id].toggle();};
        row.innerHTML = "<td>" + this.id + "</td><td>" + this.id + "</td><td>"+ this.semester + "</td>"

        for(var i = 0; i<preqs.length; i++){
            if (preqs[i] in courseDict){
                this.preqs.push(courseDict[preqs[i]]);
                edges.update({from: preqs[i], to: this.id, arrows: 'to'});
                courseDict[preqs[i]].preqTo.push(this);
            }
        }
        if (this.preqs.length === 0){
            this.isSelectable = true;
            this.update();
        }
        if(this.isSelectable){
            this.setColor(color_selectable);
        } else {
            this.setColor(color_nonselectable);
        }
       }

    select (){
        if (this.isSelectable){
            this.isCompleted = true;
            this.setColor(color_completed);
            for (var i = 0; i<this.preqTo.length; i++){
                this.preqTo[i].update();
            }
        }
    }

    deSelect(){
        if (this.isCompleted){
            this.isCompleted = false;
            for (var i = 0; i<this.preqTo.length; i++){
                this.preqTo[i].update();
            }
        }
        this.setColor(color_selectable);
        this.update();
    }

    update(){
        this.isSelectable = true;
        for (var i = 0; i<this.preqs.length; i++){
            if(this.preqs[i].isCompleted === false){
                this.isSelectable = false;
                if (this.isCompleted){
                    this.deSelect();
                }
            }
        }
        if (this.preqs.length === 0){
            this.isSelectable = true;
        }
        if(this.isSelectable){
            this.setColor(color_selectable);
        }else{
            this.setColor(color_nonselectable);
        }
    }

    setColor(color){
        var node = nodes.get(this.id);
        node.color = color;
        nodes.update(node);
        var row = document.getElementById(this.id);
        row.classList.remove("selectable");
        row.classList.remove("nonselectable");
        row.classList.remove("completed");
        if(color === color_selectable){
            row.classList.add("selectable");
        }
        if(color === color_nonselectable){
            row.classList.add("nonselectable");
        }
        if(color === color_completed){
            row.classList.add("completed");
        }
    }

    toggle(){
        if (this.isCompleted)
            this.deSelect();
        else
            this.select();
    }


}

courseDict["BLG1"] = new Course("BLG1", 1, []);
courseDict["BLG2"] = new Course("BLG2", 2, ["BLG1"]);
courseDict["BLG3"] = new Course("BLG3", 2, ["BLG1"]);
courseDict["BLG4"] = new Course("BLG4", 3, ["BLG2"]);
courseDict["BLG5"] = new Course("BLG5", 3, ["BLG3"]);
courseDict["BLG6"] = new Course("BLG6", 4, ["BLG5", "BLG4"]);
courseDict["BLG31"] = new Course("BLG31", 3, []);
courseDict["BLG32"] = new Course("BLG32", 4, ["BLG31"])


// create a network
var container = document.getElementById('network');
var data = {
  nodes: nodes,
  edges: edges
};
var options = {
    interaction: {
        hover:true,
        tooltipDelay: 300
    },
    height: '400px',
    edges: {
        smooth: false,
        labelHighlightBold: false,
        hoverWidth: 0,
    },
    nodes: {
        borderWidth: 4,
        borderWidthSelected: 4,
        size: 20,
        shape: 'hexagon',
        fixed: {
            x: true,
            y: true,
        },
        labelHighlightBold: false,

    },
    layout: {
        randomSeed: 1,
        improvedLayout: false,
        hierarchical: {
            enabled: true, //change to true to see the other graph
            direction: 'LR',
            nodeSpacing: 100,
            sortMethod: 'directed',
            shakeTowards: 'roots',
    }
  },
  // configure: {},
  "physics": {
  "enabled": false,
}
};
var network = new vis.Network(container, data, options);
network.on('click', function(params){
    if(params.nodes.length > 0){
        courseDict[params.nodes[0]].toggle();
    }
})
