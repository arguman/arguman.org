(function (arguman) {

    arguman.utils = {
        adder: function (a, b) {return a + b}
    };

    arguman.CollapsibleTree = Class.extend({

        init: function (options) {
            $.extend(this, options);
            this.$el = $(this.el);
        },

        setTreeWidth: function () {
            var root = this.$el.find(".root"),
                mainPremises = root.next().children(),
                mainContention = $(this.mainContention);
            var treeWidth = mainPremises.map(function (_, el) {
                return $(el).width() + 50;
            }).toArray().reduce(arguman.utils.adder);
            this.width = treeWidth;
            this.$el.width(treeWidth);
            mainContention.css({
                "margin-left": (root.position().left) - (mainContention.width() / 2)
            });

            if (this.width < window.innerWidth) {
                this.$el.css({
                    "margin-left": (window.innerWidth/2) - (this.width/2)
                });
                mainContention.css({
                    "margin-left": (window.innerWidth/2) - (mainContention.width() / 2)
                });
            }

        },

        render: function () {
            this.setTreeWidth();
        }
    });

    arguman.Zoom = Class.extend({
        canvas: '#app',
        currentSize: function(){
            return parseFloat($(this.canvas).css('zoom')) || 1
        },
        zoomOut: function(){
            var current = this.currentSize();
            $(this.canvas).css('zoom', current - 0.1);
            $('#zoomIn').show();
            $(this.canvas).css('padding-top', function(index, curValue){
                return parseInt(curValue, 10) + 40 + 'px';
            });
        },
        zoomIn: function(){
            var current = this.currentSize();
            $('#app').css('zoom', current + 0.1);
            if(parseFloat($(this.canvas).css('zoom')) >= 1){
                $('#zoomIn').hide();
            }
            $(this.canvas).css('padding-top', function(index, curValue){
                return parseInt(curValue, 10) - 40 + 'px';
            });
        },
        init: function(){
            $('#zoomIn').on('click', $.proxy(this, 'zoomIn'));
            $('#zoomOut').on('click', $.proxy(this, 'zoomOut'));
        }
    });

})(window.arguman || (window.arguman = {}));