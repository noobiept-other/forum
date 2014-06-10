window.onload = function()
{
var rows = document.querySelectorAll( '.clickableRow' );

for (var a = 0 ; a < rows.length ; a++)
    {
    rows[ a ].onclick = function()
        {
        window.location = this.getAttribute( 'href' );
        };
    }
};