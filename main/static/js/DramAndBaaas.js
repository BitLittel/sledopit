// made by vladis
// this uneversal code
// class_name_for_all = class name dragable list
// class_name_parent_all = parent class name 'class_name_for_all'
var class_name_for_all = 'participantContainer',
    class_name_parent_all = 'main_place_photo',
    class_name_for_place_div = 'place';
var all = document.getElementsByClassName(class_name_for_all),
    parent_all = document.getElementById(class_name_parent_all);
// get coord html element
function getCoords(elem) {
  var box = elem.getBoundingClientRect();
  return {
    top: box.top + pageYOffset,
    left: box.left + pageXOffset
  };
}
// main func Drag'n'Drop
function DrugDrop() {
  for(var i = 0; i<all.length; i++) {
    (function(i){
      var cur = all[i],
          place_div = document.createElement('div');
      cur.onmousedown = function(e) {
        // calc coord
        var coords = getCoords(cur);
        var shiftX = e.pageX - coords.left;
        var shiftY = e.pageY - coords.top;
        // begin remove
        cur.style.position = 'absolute';
        cur.style.zIndex = 9999;
        moveAt(e);
        // begin insert place_div
        place_div.className = class_name_for_place_div;
        place_div.style.height = cur.clientHeight + 'px';
        parent_all.insertBefore(place_div, all[i+1]);
        // func remove 'moveAt'
        function moveAt(e) {
          //cur.style.left = coords.left + 'px';
          cur.style.top = e.pageY - shiftY + 'px';
          cur.style.left = e.pageX - shiftX + 'px';
        }
        document.onmousemove = function(e) {
          moveAt(e);
          for (var j = 0; j<all.length; j++) {
            if (parseInt(all[j].offsetTop) == e.pageY) {
              if (j+1 == all.length) {
                parent_all.appendChild(place_div);
              } else {
                parent_all.insertBefore(place_div, all[j+1]);
              }
            }
            if (parseInt(all[j].offsetTop)+all[j].offsetHeight == e.pageY) {
              parent_all.insertBefore(place_div, all[j]);
            }
          }
        };
        cur.onmouseup = function() {
          cur.style.position = '';
          cur.style.zIndex = '';
          cur.style.left = '';
          cur.style.top = '';
          parent_all.replaceChild(cur, place_div);
          document.onmousemove = null;
          cur.onmouseup = null;
          all = document.getElementsByClassName(class_name_for_all);
          DrugDrop();
          // ajax
          // place your code, if you can
        };
      }
    })(i);
  }
}
DrugDrop();
