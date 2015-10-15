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
                this.currentElement.parent().parent(),
                true
            )
        },
        down: function () {
            this.select(
                this.currentElement.find("ul").find(".child-premise").first(),
                true
            )
        },
        left: function () {
            this.select(
                this.currentElement.prev(),
                true
            );
        },
        right: function () {
            this.select(
                this.currentElement.next(),
                true
            );
        },
        select: function (leaf, scroll) {
            if (leaf.is(".child-premise")) {
                this.$el.find(".premise").removeClass("focused");
                this.currentElement = leaf;
                leaf.find(".premise").first().addClass("focused");
                if (scroll) {
                    this.scrollTo(leaf);
                }
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
                    scrollTop: el.is('.main-premise') ? 0 : el.offset().top - 200,
                    scrollLeft: center - (window.innerWidth / 2)
                }, 150);
            }
        },
        setInitial: function () {
	        var selection,
                hash = window.location.hash;
            if (hash) {
                selection = $("#premise-" + hash.replace("#", ""));
            } else {
                selection = this.$el.find(".child-premise").first();
            }
            this.select(selection, hash && this.needsScroll());
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
                $(this.info).show();
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

    arguman.DraggablePage = Class.extend({
        el: '#app',
        clicked: false,
        click: {
            x: 0,
            y: 0
        },
        setScrollPosition: function (e) {
            $(window)
                .scrollLeft($(window).scrollLeft() + (this.click.x - e.pageX))
                .scrollTop($(window).scrollTop() + (this.click.y - e.pageY));
        },
        setCursor: function (cursor) {
            $('html').css('cursor', cursor);
        },
        disableUserSelect: function () {
            $('body').addClass('no-user-select');
        },
        enableUserSelect: function () {
            $('body').removeClass('no-user-select');
        },
        bindEvents: function () {
            var self = this;

            $(this.el).on({
                'mousemove': function (e) {
                    self.clicked && self.setScrollPosition(e);
                },
                'mousedown': function (e) {
                  console.log(self);
                    self.disableUserSelect();
                    self.clicked = e;
                    self.click.x = e.pageX;
                    self.click.y = e.pageY;
                    self.setCursor('move');
                },
                'mouseup': function (e) {
                    if (self.clicked) {
                        self.enableUserSelect();
                        self.clicked = false;
                        self.setCursor('auto');
                    }
                }
            });
        },
        init: function (options) {
            $.extend(this, options);
            this.bindEvents();
        }
    });

    arguman.Minimap = Class.extend({
        el: '#minimap',
        map: '#minimap .map',
        captureEl: '#app',
        width: 250,
        ratio: {
          x: null,
          y: null
        },
        navigator: '#minimap .navigator',
        setScrollPosition: function (x, y) {
          $(window)
              .scrollLeft(x)
              .scrollTop(y);
        },
        init: function (options) {
          $.extend(this, options);

          var self = this;

          this.$el = $(this.el);
          this.$map = $(this.map);
          this.$captureEl = $(this.captureEl);
          this.$navigator = $(this.navigator);

          this.capture();
          this.setDraggable();

          $(window).on('resize', function () {
              self.setDimensions();
          });
        },
        capture: function () {
          var self = this;

          html2canvas(this.$captureEl, {
            onrendered: function (canvas) {
              imageData = canvas.toDataURL();
              self.$map.css('backgroundImage', 'url(' + imageData + ')');
              self.setDimensions();
            }
          });
        },
        setDimensions: function () {
          height = Math.ceil(this.width * this.$captureEl.height() / this.$captureEl.width());

          this.$el.css({
            'height': height,
            'width': this.width
          });

          this.$navigator.css({
            height: $(window).height() * this.$map.height() / this.$captureEl.height(),
            width: $(window).width() * this.$map.width() / this.$captureEl.width()
          });

          this.ratio.x = this.$captureEl.width() / this.$map.width();
          this.ratio.y = this.$captureEl.height() / this.$map.height();
        },
        setDraggable: function () {
          var self = this;

          this.$navigator.pep({
            useCSSTranslation: true,
            constrainTo: 'parent',
            cssEaseDuration: 100,
            grid: [1, 1],
            velocityMultiplier: 1,
            allowDragEventPropagation: true,
            drag: function(e, obj) {
                var scrollX = self.$navigator.position().left * 100 / (self.$map.width() - self.$navigator.width());
                var scrollY = self.$navigator.position().top * 100 / (self.$map.height() - self.$navigator.height());

                scrollX *= self.$captureEl.width() / 100;
                scrollY *= self.$captureEl.height() / 100;

                self.setScrollPosition(scrollX, scrollY);
            }
          });
        },
        keepBound: function () {
          leftLimit = parseFloat(this.$navigator.css('left'));
          topLimit = parseFloat(this.$navigator.css('top'));

          this.$navigator.css({
            left: leftLimit <= 0 ? 1 : (leftLimit >= (this.$map.width() - this.$navigator.width()) ? (this.$map.width() - this.$navigator.width()) - 1 : leftLimit),
            top: topLimit <= 0 ? 1 : (topLimit >= (this.$map.height() - this.$navigator.height()) ? (this.$map.height() - this.$navigator.height()) - 1 : topLimit)
          });
        }
    });
    
    $(function () {
        $(".login-popup-close").on('click', function () {
            $(this).parents('.login-popup').hide();
        });
    });

})(window.arguman || (window.arguman = {}));
