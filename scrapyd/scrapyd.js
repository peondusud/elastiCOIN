function _buildHTMLTemplate(projects) {

    console.log(projects);
    var container = document.getElementById("listproject");
    var table = document.createElement("table");
    var r_header = document.createElement("tr");
    var p_header = document.createElement("th");
    var s_header = document.createElement("th");
    p_header.textContent = "Project";
    s_header.textContent = "Spiders";

    container.appendChild(table);
    table.appendChild(r_header);
    r_header.appendChild(p_header);
    r_header.appendChild(s_header);

    for (var project_name in projects) {
        var spiders = projects[project_name];

        var row = document.createElement("tr");
        var project = document.createElement("td");
        var spidersNode = document.createElement("td");

        project.textContent = project_name;
        for (var spider in spiders) {
            var tmp = document.createElement("td");
            tmp.textContent = spiders[spider];
            spidersNode.appendChild(tmp);
        }
        row.appendChild(project);
        row.appendChild(spidersNode);
        table.appendChild(row);
    }


    var s_projects = document.getElementById("s_projects");
    var s_spiders = document.getElementById("s_spiders");
    s_projects.addEventListener("change",function(evt){

        console.log("CARENTRE")
        console.log(evt.target.value)
	    console.log(projects[evt.target.value]);
        var s_spiders = document.getElementById("s_spiders");
        //remove all childs
        while (s_spiders.firstChild) {
            s_spiders.removeChild(s_spiders.firstChild);
        }
        var spiders = projects[evt.target.value];
        for (var spider_name in spiders) {
            var name = spiders[spider_name]
            var optionElem = new Option(name, name)
            //var optionElem = document.createElement("option");
            s_spiders.appendChild(optionElem);
        }
    });

    for (var project_name in projects) {
        var optionElement = new Option(project_name,project_name)
        //var optionElement = document.createElement("option");
        s_projects.appendChild(optionElement);
    }
    s_projects.firstChild.setAttribute("selected","selected");
    s_projects.selectedIndex = "0";

    var s = projects[s_projects.firstChild.value]
    console.log(s_projects.firstChild);
    for (var spider_name in s) {
        var name = s[spider_name]
        var optionElem = new Option(name,name)
        s_spiders.appendChild(optionElem);
    }
}


function getSpidersList(project_name) {
    var p = new Promise(function(resolve, reject) {
        var spiderlist_req = new XMLHttpRequest();

        spiderlist_req.onload = function(){
            var json = JSON.parse(this.responseText)
            resolve(json.spiders);
        };
        spiderlist_req.open("get", "/listspiders.json?project=" + project_name, true);
        spiderlist_req.send();
    });
    return p;
}

function getProjectsList() {
    var projectlist_req = new XMLHttpRequest();
    var projects = {};
    var promises = [];
    projectlist_req.onload = function() {
        var json = JSON.parse(this.responseText);
        projects = json.projects.reduce(function(acc, project_name) {
            var p = getSpidersList(project_name);
            p.then(function(spiders) {
                projects[project_name] = spiders;
            });
            promises.push(p);
            return acc;
        }, {});

        Promise.all(promises).then(function() {
            _buildHTMLTemplate(projects);
        });

    };

    projectlist_req.open("get", "/listprojects.json", true);
    projectlist_req.send();
}


document.getElementById("b_schedule").addEventListener("click",function(){

    var s_projects = document.getElementById("s_projects");
    var s_spiders = document.getElementById("s_spiders");
    var t_params = document.getElementById("t_params");
    console.log(s_projects.value);
    console.log(s_spiders.value);
    var data_params = new FormData();

    var param_lines = t_params.value.split("\n");
    for (var param_line in param_lines ) {
        var keyValuePair = param_lines[param_line].split('=');
        data_params.append(keyValuePair[0], keyValuePair[1]);
    }
    data_params.append("project",s_projects.value);
    data_params.append("spider",s_spiders.value);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', window.location + 'schedule.json', true);
    xhr.onload = function () {
        // do something to response
        console.log(this.responseText);
    };
    xhr.send(data_params);

});

getProjectsList();
