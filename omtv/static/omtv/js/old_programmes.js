



function getCollapsedDivs(isCollapsed) {
    var collapseElements = document.querySelectorAll("div[my_type='collapsable']");
    var divs = [];
    for (var i = 0; i < collapseElements.length; i++) {
        var element = collapseElements[i];
        var isElementCollapsed = element.classList.contains('collapse') && !element.classList.contains('show');                                
        if ((isCollapsed && isElementCollapsed) || (!isCollapsed && !isElementCollapsed)) {
            divs.push(element);
        }
    }            
    return divs;
}


function toggle_divs() {
    var divs_opened = getCollapsedDivs(false);
    var divs_closed = getCollapsedDivs(true);            
    var divs = divs_opened.length > 0 ? divs_opened : divs_closed;
    divs.forEach(function(element) {
        var bsCollapse = new bootstrap.Collapse(element, {toggle: true});
    })
}