$(document).ready(function () {
  $('#form').submit(function(){
    var data = {
      url: $('#input_url').val(),
      cuils: $('#input_cuils').val().split('\n').join(','),
      emails: $('#input_emails').val().split('\n').join(','),
    }

    $.ajax({
      url: '/api/links',
      type: 'post',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function(response) {
        var links = response.links;
        $('#links').html(links.join('<br><br>'));
      }
    })
    return false;
  })
});
