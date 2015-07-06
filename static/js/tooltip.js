function Tooltip( referenceElement, text )
{
var _this = this;

var element = document.createElement( 'div' );
element.className = 'tooltip';
element.innerHTML = text;

referenceElement.onmouseover = function()
    {
    _this.show();
    };

referenceElement.onmouseout = function()
    {
    _this.hide();
    };

referenceElement.onmousemove = function( event )
    {
    var windowWidth = window.innerWidth;
    var windowHeight = window.innerHeight;
    var width = element.offsetWidth;
    var height = element.offsetHeight;

    var nextX = event.clientX + 20;
    var nextY = event.clientY + 20;

    if ( nextX + width > windowWidth )
        {
        nextX = windowWidth - width;
        }

    if ( nextY + height > windowHeight )
        {
        nextY = windowHeight - height;
        }

    _this.moveTo( nextX, nextY );
    };


this.element = element;
}


Tooltip.prototype.show = function()
{
document.body.appendChild( this.element );
};


Tooltip.prototype.hide = function()
{
document.body.removeChild( this.element );
};


Tooltip.prototype.moveTo = function( x, y )
{
this.element.style.left = x + 'px';
this.element.style.top = y + 'px';
};
