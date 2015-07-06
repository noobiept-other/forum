var CheckMessages;
(function(CheckMessages) {

CheckMessages.init = function()
{
setClickableRows();
setContentPreview();
};


/**
 * When clicking on a row, change to the location specified in a 'data-url' attribute.
 */
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


/**
 * When the mouse is over the element, show a tooltip next to the mouse, with some text (for example show the text of a thread, without having to open it).
 */
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

})(CheckMessages || (CheckMessages = {}));


window.addEventListener( 'load', CheckMessages.init, false );

