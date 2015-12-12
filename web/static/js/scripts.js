function update_squares(x, y, img)
{
    if (img == false)
        img = 'Empty_Image'
    $('td[data-x=' + x + '][data-y=' + y + '] img').attr('src', '/static/images/' + img +'.png')
}

function what_about_check(value)
{
    if (value == 1)
        return('Check for Black player')
    if (value == 2)
        return('Check for White player')
    return('No check')
}

function what_about_mate(value)
{
    if (value == 0)
        return('No mate')
    else
        return('Congratulations!')
}

var first_choosing_was_done = false;
var first_coordinates = [];
var not_game_begin = false


$(document).ready(function()
{

//    $.getJSON()
    $.get('/get_status', function(data)
    {
        if (data.game_has_begun)
        {
            $('.whose-turn').text(data.turn+' turn');
            $('.game-info form').hide();
        }
        else
        {
            $('table').hide();
            $('.create_new_game').hide()
            console.log('Game hasn\'t begun');
        }
    }
     , 'json')


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
                        $('.is-check').text(what_about_check(data.is_check))
                        $('.is-mate').text(what_about_mate(data.is_mate))
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
            not_game_begin = true
            first_choosing_was_done = true;
            first_coordinates = [x, y];
            // $(this).css("border", "1px solid green");
            $(this).addClass('selected');

        }
    });

    $('.new_game_button').click(function(e)
    {
        e.preventDefault();
        $.post('/start_new_game', function(data){
            console.log(data)
            if (data.status == 'Ok')
            {
                console.log('new_game = true')

                new_game = true
            }
            else new_game = False
            if (new_game)
            {
                for (i = 0; i < 8; i++)
                    for (j = 0; j < 8; j++)
                        update_squares(i, j, data.board[i][j])
                $('.whose-turn').text('White turn')
            }

        }, 'json')

    })

    $('.send_names_button').click(function (e){
        e.preventDefault();
        var form = $(this).parents('form')[0];
        var form_data = $(form).serialize();

        $.post('/set_names', form_data, function(data){
            console.log(data);
            if (data.status == 'Ok')
            {
                $('.game-info form').hide();
                $('.white_player').text(data.white_player);
                $('.black_player').text(data.black_player);
                $('.whose-turn').text('White turn');
                $('.create_new_game').show();
                $('table').show()
            }
            else alert(data.message)
        }, 'json');
    });
});

