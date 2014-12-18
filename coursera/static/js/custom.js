/*function get_courses(obj){
    document.forms["course_form"].submit();
    data = {cat : obj};
        $.get("/courses/", data);
};
*/
$('input[type="checkbox"]').bind('change', function() {
    $('input[type="checkbox"]').each(function(index, value) {
      if (this.checked) {
            alert('hello');
            document.getElementById(this.id).checked = true;
            var datalist = [];
            $(":checked").each(function() {
              datalist.push($(this).val());
            });
            alert(datalist);
            $.ajax({
                type:'POST',
                url:'/new_courses/',
                data: {'cat' : datalist},
                success: function(data){
                    $('#myResponse').html(data);
                    alert('success');
                },
                error: function (request, status, error) {
                    alert(request.responseText);
                }
            });
        }
    });
});
/*when a user selects interest in an addtional service, add this to the additionalServices div
$('input[type="checkbox"]').bind('change', function() {
    var alsoInterested = '';
     $('input[type="checkbox"]').each(function(index, value) {
          if (this.checked) {

               alsoInterested += ($('label[for="'+this.id+'"]').html() + ', ');
          }
     });
     if (alsoInterested.length > 0) {
          alsoInterested = alsoInterested.substring(0,alsoInterested.length-2);
     } else {
          alsoInterested = 'All Categories';
     }

     $('#additionalServices').html(alsoInterested);
       //  alert($('#additionalServices').html());

    var myDivObj = document.getElementById("additionalServices").innerHTML ;

     //get_courses(myDivObj);
     setTimeout(get_courses(myDivObj), 100000);
});*/