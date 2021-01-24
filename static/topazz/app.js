
function getServices(name,field){
    let sarr = [];
    let services = document.getElementsByClassName(name);
    for(let i=0; i<services.length; i++){
        if (services[i].checked){
            sarr.push(services[i].value);
        }
    }
    area = document.getElementById(field);
    area.value = sarr;
    return area;
}