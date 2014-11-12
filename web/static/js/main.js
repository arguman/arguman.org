(function (arguman) {

    arguman.utils = {
        adder: function (a, b) {
            return a + b
        }
    };

    arguman.KeyboardManager = Class.extend({
        currentElement: null,
        init: function (options) {
            $.extend(this, options);
            this.$el = $(this.el);
            this.bindEvents();
            this.setInitial();
        },
        up: function () {
            this.select(
                this.currentElement.parent().parent()
            )
        },
        down: function () {
            this.select(
                this.currentElement.find("ul").find(".child-premise").first()
            )
        },
        left: function () {
            this.select(
                this.currentElement.prev()
            );
        },
        right: function () {
            this.select(
                this.currentElement.next()
            );
        },
        select: function (leaf) {
            console.log('ok')
            if (leaf.is(".child-premise")) {
                this.$el.find(".premise").removeClass("focused");
                this.currentElement = leaf;
                leaf.find(".premise").first().addClass("focused");
                this.scrollTo(leaf);
            }
        },
        needsScroll: function () {
            var maxHeight = Math.max.apply(this,
                this.$el.find(".premise")
                    .toArray()
                    .map(function (el) {
                    return $(el).offset().top + $(el).height();
            }));

            return (this.$el.width() > window.innerWidth ||
                    maxHeight > window.innerHeight)
        },
        scrollTo: function (el) {
           if (this.needsScroll()) {
               var center = el.offset().left +  (el.width()/2);
               $('html, body').animate({
                   scrollTop: el.offset().top - 200,
                   scrollLeft: center - (window.innerWidth / 2)
               }, 150);
           }
        },
        setInitial: function () {
            if (this.needsScroll()) {
                this.select(this.$el.find(".child-premise").first());
            }
        },
        bindEvents: function () {
            $(document).keydown(function(e) {
                switch(e.which) {
                    case 37:
                    this.left();
                    break;

                    case 38:
                    this.up();
                    break;

                    case 39:
                    this.right();
                    break;

                    case 40:
                    this.down();
                    break;

                    default: return; // exit this handler for other keys
                }
                e.preventDefault(); // prevent the default action (scroll / move caret)
            }.bind(this));

            if (this.needsScroll()) {
                this.$el.find(".premise-content").on('click', function (event) {
                    this.select($(event.target).parents(".child-premise").eq(0))
                }.bind(this));
                $(window).on("scroll", function () {
                    $(this.info).fadeOut(100);
                }.bind(this));

            } else {
                $(this.info).hide();
            }

        }
    });

    arguman.CollapsibleTree = Class.extend({

        premiseWidth: 260,

        init: function (options) {
            $.extend(this, options);
            this.$el = $(this.el);
        },

        setTreeWidth: function () {
            /*
             * Set full width to container, and reduce the width with
             * positions of last premise.
             * */

            if (this.$el.hasClass("empty")) {
                return;
            }

            var root = this.$el.find(".root"),
                mainContention = $(this.mainContention);
            var treeWidth = parseInt(this.$el.data("width")) * (this.premiseWidth * 2);
            this.width = treeWidth;
            this.$el.width(treeWidth);

            var mainPremises = root.next().children();

            if (mainPremises.length) {
                var premises = root.parent().find("li");

                var maxPosition = Math.max.apply(this,
                    premises.toArray().map(function (premise) {
                        return $(premise).offset().left
                    }));

                this.width = (maxPosition + this.premiseWidth + 50);
                this.$el.width(this.width);
                mainContention.css({
                    "margin-left": (root.position().left) - (mainContention.width() / 2)
                });
            }

            if (this.width < window.innerWidth) {
                this.$el.css({
                    "margin-left": (window.innerWidth / 2) - (this.width / 2)
                });
                mainContention.css({
                    "margin-left": (window.innerWidth / 2) - (mainContention.width() / 2)
                });
            }

        },

        render: function () {
            this.setTreeWidth();
            this.$el.css("visibility", "visible");
        }
    });

    arguman.Zoom = Class.extend({
        canvas: '#app',
        currentSize: function () {
            return parseFloat($(this.canvas).css('zoom')) || 1
        },
        zoomOut: function () {
            var current = this.currentSize();
            $(this.canvas).css('zoom', current - 0.1);
            $('#zoomIn').show();
            $(this.canvas).css('padding-top', function (index, curValue) {
                return parseInt(curValue, 10) + 40 + 'px';
            });
        },
        zoomIn: function () {
            var current = this.currentSize();
            $('#app').css('zoom', current + 0.1);
            if (parseFloat($(this.canvas).css('zoom')) >= 1) {
                $('#zoomIn').hide();
            }
            $(this.canvas).css('padding-top', function (index, curValue) {
                return parseInt(curValue, 10) - 40 + 'px';
            });
        },
        init: function () {
            $('#zoomIn').on('click', $.proxy(this, 'zoomIn'));
            $('#zoomOut').on('click', $.proxy(this, 'zoomOut'));
        }
    });

})(window.arguman || (window.arguman = {}));