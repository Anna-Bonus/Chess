function update_squares(x, y, img)
{
    if (img == false)
        img = 'Empty_Image'
    $('td[data-x=' + x + '][data-y=' + y + '] img').attr('src', '/static/images/' + img +'.png')
}


var first_choosing_was_done = false;
var first_coordinates = [];


$(document).ready(function()
{
    $('img').click(function()
    {
        var x = $(this).parent().data('x');
        var y = $(this).parent().data('y');
        console.log(x);
        console.log(y);
        if (first_choosing_was_done)
        {
            if (first_coordinates[0] != x || first_coordinates[1] != y)
            {
                $.post('/move', {'source_x':first_coordinates[0],'source_y':first_coordinates[1], 'destination_x':x, 'destination_y':y}, function(data)
                {
                     console.log(data.status);
                     if (data.status == 'Ok')
                     {
                        for (i = 0; i < 8; i++)
                            for (j = 0; j < 8; j++)
                                update_squares(i, j, data.board[i][j])
                        $('.whose-turn').text(data.turn+' turn')
                     }
                     else alert(data.message)
                },
                 'json');
            }
            first_choosing_was_done = false;
            $('img').removeClass('selected');
        }
        else
        {
            first_choosing_was_done = true;
            first_coordinates = [x, y];
            // $(this).css("border", "1px solid green");
            $(this).addClass('selected');
        }
    });
});

