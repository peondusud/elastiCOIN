function _buildHTMLTemplate(projects) {
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
}

function getSpidersList(project_name) {
    var p = new Promise(function(resolve, reject) {
        var spiderlist_req = new XMLHttpRequest();

        spiderlist_req.onload = function(){
            var json = JSON.parse(this.responseText)
            json.spiders.shift();
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

getProjectsList();
