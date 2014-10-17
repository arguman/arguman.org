(function (arguman) {

    arguman.utils = {
        adder: function (a, b) {return a + b}
    };

    arguman.Contention = Class.extend({

        level: 0,
        maxY: 0,

        init: function (options) {
            $.extend(this, options);
            var model = options.model,
                _premiseIndex = 1;
            this.children = model.children.map(function (premise) {
                return new arguman.Premise({
                    model: premise,
                    parent: this,
                    index: _premiseIndex++,
                    level: this.level + 1,
                    contention: this
                });
            }.bind(this));
        },
        getTotalNodes: function () {
            var total = this.children
                    .map(function (child) {return child.getTotalNodes()})
                    .reduce(arguman.utils.adder);
            return total;
        },
        getWidth: function () {
            var nodesWidth = this.children
                .map(function (child) {return child.getTreeWidth()})
                .reduce(arguman.utils.adder);
            return nodesWidth;
        },
        render: function () {
            this.domElement = $("<div>", {
                "class": "main-contention"
            }).html(this.model.name)
              .width(this.getWidth());
            return this.domElement;
        },
        renderPremises: function (container) {
            var left = 0,
                top = 100 + $(this.domElement).height();
            this.children.map(function (premise) {
                premise.renderLevel(container, left, top);
                left += premise.getTreeWidth();
            }.bind(this));

            this._renderCallbacks.forEach(function (callback) {
                callback(this);
            });
        },
        renderEdges: function (context) {
            // add edge to main premises
            var firstPremise = this.children[0],
                lastPremise = this.children[this.children.length-1];
            context.moveTo(firstPremise.getCenterX(), firstPremise.y - 60);
            context.lineTo(lastPremise.getCenterX() + 4, lastPremise.y - 60);
            context.stroke();
            this.children.forEach(function (premise) {
                context.moveTo(premise.getCenterX() + 2, firstPremise.y - 60);
                context.lineTo(premise.getCenterX() + 2, lastPremise.y);
                context.stroke();
                premise.renderEdges(context);
            });
        },

        _renderCallbacks: [],
        onRender: function (callback) {
            this._renderCallbacks.push(callback);
        }
    });

    arguman.Premise = Class.extend({

        minWidth: 150,
        maxWidth: 200,

        parent: null,
        level: 0,

        init: function (options) {
            $.extend(this, options);
            var model = options.model;
            this.children = model.children.map(function (premise, index) {
                return new arguman.Premise({
                    model: premise,
                    parent: this,
                    index: index + 1,
                    level: this.level + 1,
                    contention: this.contention
                });
            }.bind(this));
        },
        getTotalNodes: function () {
            var total = 1;
            if (this.children.length) {
                total += this.children
                    .map(function (child) {return child.getTotalNodes()})
                    .reduce(arguman.utils.adder);
            }
            return total;
        },
        getWidth: function () {
            return this.maxWidth;

//            if (this.model.name.length > 50) {
//                return this.minWidth;
//            } else {
//                return this.maxWidth;
//            }
        },
        getTreeWidth: function () {
            var total;
            if (this.children.length) {
                total = this.children
                    .map(function (child) {return child.getTreeWidth()})
                    .reduce(arguman.utils.adder);
            } else {
                total = this.getWidth();
            }
            return total;
        },
        getHeight: function () {
//            return parseInt(this.model.name.length / 30)
        },

        getCenterX: function () {
            return this.x + (this.getWidth()/2)
        },

        renderPremiseContent: function () {
            return $("<div>", {
                "class": "premise-content"
            }).html(this.model.name)
        },

        render: function (columnLeft, rowTop) {
            var premise = $("<div>", {
                "class": "premise"
            }).html(this.renderPremiseContent());

            premise.css({
                "width": this.getWidth()
            });

            var centerOffset = this.getTreeWidth() / 2 - (this.getWidth()/2);

            this.x = columnLeft + centerOffset;
            this.y = rowTop;

            this.contention.maxY = Math.max(this.y, this.contention.maxY);

            premise.css({
                "margin-left": this.x + "px",
                "margin-top": this.y + "px"
            });

            return premise;
        },
        renderLevel: function (container, columnLeft, rowTop) {
            var attached = this.render(columnLeft, rowTop);
            container.append(attached);
            this.height = attached.height();
            var left = 0;
            this.children.map(function (premise) {
                premise.renderLevel(container,
                    columnLeft + left,
                    rowTop + 100 + this.height);
                left += premise.getWidth();
            }.bind(this));
        },
        renderEdges: function (context) {
            context.moveTo(this.getCenterX(), this.y + this.height);
            context.lineTo(this.getCenterX(), this.y + this.height + 40);
            context.stroke();

            if (this.children.length > 1) {
                var firstPremise = this.children[0],
                lastPremise = this.children[this.children.length-1];

                context.moveTo(firstPremise.getCenterX() -2, firstPremise.y - 60);
                context.lineTo(lastPremise.getCenterX() + 2, lastPremise.y - 60);
                context.stroke();
            }


            this.children.forEach(function (premise) {

                context.moveTo(premise.getCenterX(), premise.y - 60);
                context.lineTo(premise.getCenterX(), premise.y);
                context.stroke();
                if (premise.children.length) {
                    premise.renderEdges(context);
                }

            }.bind(this));


        }
    });

    arguman.Canvas = Class.extend({
        width: 800,
        height: 600,
        init: function (options) {
            $.extend(this, options);
        },

        render: function () {
            var canvas = document.createElement("canvas");
            canvas.width = this.width;
            canvas.height = this.height;
//            canvas.style.marginLeft = -(this.width/2) + "px";

            this.domElement = canvas;

            return canvas;
        }
    });

    arguman.Map = Class.extend({
        init: function (options) {
            $.extend(this, options);
            this.contention = new arguman.Contention({
                model: options.model
            });
            this.$container = $(this.container);
            this.contention.onRender(this.onRenderFinish.bind(this));
        },
        calculateWidth: function () {
            return this.contention.getWidth()
        },
        render: function () {
            this.canvas = new arguman.Canvas({
                width: this.contention.getWidth()
            });

            this.$container
                .append(this.canvas.render())
                .append(this.contention.render());

            this.contention.renderPremises(this.$container);

        },
        onRenderFinish: function () {
            this.canvas.domElement.height = this.contention.maxY;
            this.renderEdges();
        },
        renderEdges: function () {
            var canvas = this.canvas.domElement,
                context = canvas.getContext("2d");

            context.translate(0.5, 0.5);

            context.beginPath();

            context.arc(
                canvas.width / 2,
                $(this.contention.domElement).height() + 10,
                12,
                0,
                2 * Math.PI,
                false
            );


            context.fillStyle = 'gray';

            context.fill();
            context.beginPath();

            context.strokeStyle = "gray";
            context.lineWidth = 4;

            context.moveTo(
                (canvas.width / 2),
                $(this.contention.domElement).height() + 21
            );

            context.lineTo(
                canvas.width / 2,
                $(this.contention.domElement).height() + 40
            );

            context.stroke();

            this.contention.renderEdges(context);

        }
    });

})(window.arguman || (window.arguman = {}));