let courseDict = {}
let nodeList = []
let edgeList = []

class Course{
    constructor(id, semester, preqs){
        this.id = id;
        this.semester = semester;
        this.preqs = [];
        this.isSelectable = false;
        this.isCompleted = false;
        this.preqTo = [];
        nodeList.push({id:this.id, label:this.id});

        for(var i = 0; i<preqs.length; i++){
            console.log("burdayiz preq = "+ preqs);
            if (preqs[i] in courseDict){
                console.log("hacim burdayiz preq = " + preqs[i]);
                this.preqs.push(courseDict[preqs[i]]);
                edgeList.push({from: preqs[i], to: this.id});
                courseDict[preqs[i]].preqTo.push(this);
            }
        }
        if (semester === 0)
            this.isSelectable = true;
    }

    select (){
        if (this.isSelectable){
            this.isCompleted = true;
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
        if (this.semester === 0){
            this.isSelectable = true;
        }
    }


}

courseDict["BLG1"] = new Course("BLG1", 0, []);
courseDict["BLG2"] = new Course("BLG2", 2, ["BLG1"]);
