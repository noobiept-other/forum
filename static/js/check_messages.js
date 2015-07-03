var CheckMessages = (function()
{
function C()
{

}

C.init = function()
{
setClickableRows();
setContentPreview();
};


function setClickableRows()
{
var rows = document.querySelectorAll( '.clickableRow' );

for (var a = 0 ; a < rows.length ; a++)
    {
    rows[ a ].onclick = function()
        {
        window.location = this.getAttribute( 'data-url' );
        };
    }
}


function setContentPreview()
{
var setupTooltip = function( referenceElement, content )
    {
    referenceElement.tooltip = new Tooltip( referenceElement, content );
    };

var elements = document.querySelectorAll( '.contentPreview' );

for (var a = 0 ; a < elements.length ; a++)
    {
    var element = elements[ a ];
    var content = element.getAttribute( 'data-content' );

    setupTooltip( element, content );
    }
}


return C;

}());


window.addEventListener( 'load', CheckMessages.init, false );

