(function(window)
{
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
    _this.moveTo( event.clientX + 20, event.clientY + 20 );
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


window.Tooltip = Tooltip;

}(window));