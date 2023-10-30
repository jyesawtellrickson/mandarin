function colourGrades(grade) {

    var colour_map = {
        0: 'white',
        1: 'violet',
        2: 'blue',
        3: 'green',
        4: 'yellow',
        5: 'orange',
        6: 'red',
    }
    grade = 2
    var x = document.querySelectorAll('[data-grade="' + grade + '"]');
    var i;
    for (i = 0; i < x.length; i++) {
      x[i].style.color = colour_map.2
    }

}
