(function (arguman) {

    arguman.utils = {
        adder: function (a, b) {
            return a + b
        }
    };

    arguman.Navigator = Class.extend({
        currentElement: null,
        init: function (options) {
            $.extend(this, options);
            this.$el = $(this.el);
        },
        up: function () {
            this.select(
                this.currentElement.parent().closest(".tree-branch"),
                true
            )
        },
        down: function () {
            this.select(
                this.currentElement
                    .find(".tree-branch")
                    .first(),
                true
            )
        },
        left: function () {
            this.select(
                this.currentElement
                    .prevAll(".tree-branch")
                    .first(),
                true
            );
        },
        right: function () {
            this.select(
                this.currentElement
                    .nextAll(".tree-branch")
                    .first(),
                true
            );
        },
        select: function (leaf, scroll) {
            if (leaf.is(".tree-branch")) {
                if (leaf.closest(".collapsed").length) {
                    this.expandNode(leaf);
                }
                this.$el.find(".tree-node").removeClass("focused");
                leaf.find(".tree-node").first().addClass("focused");
                this.currentElement = leaf;
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
            var mainPremise = (".tree-container > .tree > " +
                               ".tree-branch > .tree-node");
            var node = el.find("> .tree-node");
            if (this.needsScroll()) {
                var center = node.offset().left +  (node.width()/2);
                $('html, body').animate({
                    scrollTop: node.is(mainPremise)? 0: node.offset().top - 200,
                    scrollLeft: center - (window.innerWidth / 2)
                }, 150);
            }
        },
        expandNode: function (node) {
            var branch = node.closest(".tree-branch.collapsed");
            if (branch.length) {
                this.treeView.expandBranch(branch);
            }
        },
        getHashOrPath: function () {
            var hash = window.location.hash,
                path = window.location.pathname;

            var parts = path.split("/");

            if (parts.length > 2) {
                return parts[parts.length - 1];
            } else {
                return hash.replace("#", "");
            }
        },
        setInitial: function () {
	        var hash = this.getHashOrPath(),
                selection = this.$el.find(".tree-branch").first();
            
            if (hash) {
                var targetPremise = $("#premise-" + hash);
                if (targetPremise.length) {
                    selection = targetPremise;
                    this.expandNode(selection);
                }
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

                    default: return;
                }
                e.preventDefault();
            }.bind(this));

            if (this.needsScroll()) {
                $(this.info).show();
            } else {
                $(this.info).hide();
            }
        },

        render: function () {
            this.bindEvents();
            this.setInitial();
            setTimeout(function () {
                $(this.info).fadeOut('slow');
            }.bind(this), 3000);
            this.$el
                .find(".tree-node")
                .on('click', function (event) {
                    this.select(
                        $(event.target)
                        .parents(".tree-branch")
                        .first()
                    )
                }.bind(this));
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
        render: function (options) {
            $.extend(this, options);
            this.bindEvents();
        }
    });

    arguman.Tree = Class.extend({

        treeWidth: 0,

        branchWidth: function (i, branch) {
            var width = 1;
            $(branch).find("> .tree").each(function (i, el) {
                var tree = $(el);
                var max = tree
                            .find("> .tree-branch")
                            .not(".collapsed")
                            .map(this.branchWidth.bind(this))
                            .toArray()
                            .reduce(arguman.utils.adder, 0);
                
                if (max > width) {
                    width = max;
                }

            }.bind(this));
            return width;
        },

        renderSubTree: function (branch, top, left, level) {
            var subTree = branch.find("> .tree"),
                isSingleBranch = subTree.find("> .tree-branch").length === 1;
            
            if (subTree.length) {
                if (isSingleBranch) {
                    var extraHeight = 50;
                } else {
                    var extraHeight = 100;
                }

                this.renderTree(
                    subTree, 
                    top + extraHeight,
                    left,
                    level
                );
            }
        },

        renderBranchConnector: function (branch, top, left) {
            var branchConnector = branch.find("> .branch-connector");
            if (branchConnector.length) {
                branchConnector.css({
                    left: left,
                    top: top
                });
            }
        },

        renderChildConnector: function (branch, top, left) {
            var childConnector = branch.find("> .child-connector");
            if (childConnector.length) {
                childConnector.css({
                    left: left,
                    top: top
                });
            }
        },

        renderTreeConnector: function (tree, width, top, left, branchSize, level) {
            var connector = tree.find("> .tree-connector"),
                hasCollapsed = tree.find("> .collapsed").length > 0,
                hasCollapsible = tree.find("> .collapsible").length > 0,
                visible = branchSize > 1; 

            if (connector.length) {
                connector.css({
                    width: width,
                    marginLeft: 125,
                    left: left,
                    top: top,
                    display: visible ? "block": "none"
                });
            }

            if (hasCollapsed) {
                var collapsiblePreview = connector.hide().next();
                collapsiblePreview.css({
                    display: "block",
                    top: top - 30,
                    left: left
                })
                .off('click')
                .one('click', function () {
                    this.resetTreeWidth();
                    this.expandTree(tree);
                }.bind(this))
            }

            if (hasCollapsible && !hasCollapsed) {
                var collapseButton = connector.nextAll(".collapse-button");
                    
                collapseButton.css({
                    display: "block",
                    top: top - 30,
                    left: left + width
                })
                .off('click')
                .one('click', function () {
                    this.resetTreeWidth();
                    this.collapseTree(tree.parents(".tree").first());
                    this.renderTree(this.getRoot());
                }.bind(this)); 
                
            }

        },
        
        renderBranch: function (el, treeTop, treeLeft, level) {
            var branch = $(el);
            var node = branch.find("> .tree-node");
            var left = branch
                        .prevAll()
                        .map(this.branchWidth.bind(this))
                        .toArray()
                        .reduce(arguman.utils.adder, 0)
                         * (node.width() + 20);

            node.css({
                left: left + treeLeft,
                top: treeTop
            });

            if (!branch.is(".collapsed")) {
                branch.show();
            }

            this.renderSubTree(
                branch,
                treeTop + node.height(), 
                left + treeLeft,
                level + 1
            );

            this.renderBranchConnector(
                branch,
                treeTop,
                left + treeLeft
            );
            
            this.renderChildConnector(
                branch,
                treeTop + node.height(),
                left + treeLeft
            );

            return left;
        },

        renderTree: function (tree, treeTop, treeLeft, level) {
            var branches = tree.find("> .tree-branch");
            
            treeTop = treeTop || 40;
            treeLeft = treeLeft || 0;
            level = level || 0;

            var maxWidth = 0,
                branchSize = branches.length;
            
            branches.each(function (index, el) {
                var width = this.renderBranch(
                    el,
                    treeTop,
                    treeLeft,
                    level
                );
                if (width > maxWidth) {
                    maxWidth = width;
                }
            }.bind(this));

            this.renderTreeConnector(
                tree,
                maxWidth,
                treeTop,
                treeLeft,
                branchSize,
                level
            );
            
            if (maxWidth > this.treeWidth) {
                this.treeWidth = maxWidth;
            }

            if (level === 0) {
                this.setCenter(maxWidth);
                if (branches.length === 1) {
                    this.viewSingleBranch();
                } else if (branches.length === 0) {
                    this.viewEmptyTree();
                }
            }

            this.setAppHeight();
        },

        resetTreeWidth: function () {
            this.treeWidth = null;
        },

        viewSingleBranch: function () {
            this.getRoot().css({
                marginTop: -50
            });
        },

        viewEmptyTree: function () {
            $(".tree-contention-actions").hide()
            $(".root-connector").addClass("empty");
            $(".empty-state").show();
        },

        setCenter: function (maxWidth) {
            var left;
            if (maxWidth + 300 < window.innerWidth) {
                var width = maxWidth + 254;
                left = (window.innerWidth / 2 - width / 2);
            } else {
                left = 30;
            }
            $(".tree-container").css({
                marginLeft: left
            });
        },

        setAppHeight: function () {
            var premises = $(".tree-node"),
                deepestPosition = 0,
                deepestPremise = null;
            premises.each(function () {
                var premise = $(this),
                    position = premise.position().top;
                if (position > deepestPosition) {
                    deepestPosition = position;
                    deepestPremise = premise
                }
            });

            if (deepestPremise) {
                $("#app").height(
                    deepestPosition + 
                    deepestPremise.height() +
                    $(".tree-contention").height() +
                    300
                );
            } 
        },

        expandTree: function (tree, renderTree) {
            renderTree = renderTree || true;

            tree.find("> .collapsed").removeClass("collapsed");
            tree.find('> .collapsible-preview').hide();

            if (renderTree) {
                this.renderTree(this.getRoot())
            }
        },

        expandBranch: function (branch) {
            branch.parents('.tree').each(function (i, el) {
                this.expandTree($(el));
            }.bind(this));

            this.renderTree(this.getRoot());
        },

        collapseTree: function (tree) {
            var subTrees = tree.find(".tree");
            subTrees.each(function (i, el) {
                var subTree = $(el);

                var isFallacy = subTree.prev().hasClass('too-many-fallacy');
                var score = parseInt(subTree.prev().data('weight'));
                
                if (parseInt(subTree.data("level")) < 3
                        && !isFallacy
                        && score > 0) {
                    return;
                }
                
                subTree
                    .find("> .tree-branch")
                    .first()
                    .nextAll(".tree-branch")
                    .addClass("collapsible")
                    .addClass("collapsed");

                subTree
                    .find(".collapse-button")
                    .add(".collapsed")
                    .hide();

            }.bind(this));
        },

        getRoot: function () {
            return $(".tree-container > .tree");
        },

        renderContentionHeader: function () {
            var viewport = window.innerWidth,
                rootPoint = $(".root"),
                actions = $(".tree-contention-actions");

            var center = viewport / 2 - rootPoint.width() / 2;

            rootPoint.css({
                marginLeft: center
            });
            actions.css({
                marginLeft: center + 40
            })
        },

        showApp: function () {
            $("#app").css({
                visibility: "visible"
            });
            $("#loading").hide();
        },

        loadPartials: function (callback) {

            var promises = [],
                partials = $('[data-load-partial]');

            if (!partials.length) {
                return callback();
            }

            partials.each(function () {
                var partialNode = $(this);
                var url = partialNode.data('load-partial');
                var promise = $.get(url);

                promise.done(function (response) {
                    partialNode.replaceWith(response)
                });

                promises.push(promise)
            });

            $.when.apply($, promises).then(function () {
                callback()
            })

        },

        render: function () {
            this.loadPartials(function () {
                var tree = this.getRoot();
                this.renderContentionHeader();
                this.collapseTree(tree);
                this.renderTree(tree);
                this.onRender();
                this.showApp();
            }.bind(this));
        },

        init: function (options) {
            $.extend(this, options);
        }
        
    });

    arguman.NounLoader = Class.extend({
        el: ".tree-contention h3 a",
        currentNoun: null,

        init: function (options) {
            $.extend(this, options);
            this.$el = $(this.el);
            this.$tooltip = $("<div>", {
                'class': 'noun-tooltip'
            }).css({
                'display': 'none'
            }).append(
                $("<div />").addClass('noun-tooltip-content')
            );
        },

        placeTooltip: function ($target) {
            var position = $target.position();
            this.$tooltip.css({
                'left': position.left,
                'top': position.top + $target.height()
            });
            this.timeout = setTimeout(
                this.loadContent.bind(this, $target),
                300
            );
        },

        loadContent: function ($target) {
            var url = $target.attr('href');
            if (this.currentNoun != url) {
                this.$tooltip
                    .find('.noun-tooltip-content')
                    .html('Loading');
            }
            $.get(url, {
                'partial': true,
                'source': arguman.contention.id
            }, function (response) {
                this.currentNoun = url;
                if ($(response).find('.relation').length > 0) {
                    this.$tooltip
                        .find('.noun-tooltip-content')
                        .html(response)
                        .end().show();
                }
            }.bind(this));
        },

        render: function () {
            $('body').append(this.$tooltip);

            this.$el.on('mouseover', function (event) {
                var $target = $(event.target);
                if (this.timeout) {
                    clearTimeout(this.timeout);
                }
                this.placeTooltip($target);
            }.bind(this));

            var hideTooltip = true;

            this.$el.on('mouseleave', function (event) {
                var target = $(event.relatedTarget);
                if (!target.is(this.$tooltip) &&
                    !target.is('.noun-tooltip-content')) {
                    this.hideTooltip();
                }
            }.bind(this));

            this.$tooltip.on('mouseleave', function (event) {
                if (!$(event.relatedTarget).is(this.el)) {
                    this.hideTooltip();
                }
            }.bind(this));
        },

        hideTooltip: function () {
            this.$tooltip.hide();
            clearTimeout(this.timeout);
        }
    });

    arguman.Timeline = Class.extend({
        el: "#timeline",
        premises: ".tree-node",

        init: function (options) {
            $.extend(this, options);

            this.$el = $(this.el);
            this.$premises = $(this.premises);
        },

        getPremiseId: function (node) {
            return parseInt($(node).data('id'));
        },

        sortPremises: function () {
            var premises = this.$premises;
            premises.sort(function (a, b) {
                return (this.getPremiseId(a) -
                        this.getPremiseId(b));
            }.bind(this));
            return premises;
        },

        selectNode: function (target) {
            this.navigator.select(
                $(target).closest('.tree-branch'),
                true
            );
        },

        render: function () {
            var premises = this.sortPremises();
            var barWidth = Math.max(
                $('.tree-contention h3 span').width() + 10,
                620
            );

            $('#tree-overview')
                .show()
                .css({width: barWidth,
                      marginLeft: -barWidth/2});

            this.$el.css({
                width: barWidth,
                marginLeft: -barWidth/2
            });

            var width = barWidth / this.$premises.length;

            $(premises).each(function (i, el) {
                var premise = $(el);
                this.$el.append(
                    $("<a />")
                        .addClass("entry")
                        .addClass(premise.data('type'))
                        .attr({
                            'href': '#'
                        })
                        .css({
                            width: width
                        }).
                        on('click', function (event) {
                            this.selectNode(premise);
                            event.preventDefault();
                        }.bind(this))
                );
            }.bind(this));
        }
    });

    $(function () {
        $(".login-popup-close").on('click', function () {
            $(this).parents('.login-popup').hide();
        });

        var hideToolTips = function () {
            $('.tooltip').hide();
        };

        $('.tooltip .close').on('click', hideToolTips);
        $(window).on('scroll', hideToolTips);

        $('.search').on('click', function(){
            $('#keyword').trigger('focus');
        });


        $('.recommendation-sidebar')
            .on('click', function () {
                $(this).addClass('opened');
            })
            .on('mouseleave', function () {
                $(this).removeClass('opened');
            });

        $("form.support").submit(function(event) {
          event.preventDefault();
          var $this = $(this);
          var csrfToken = $this.find('[name=csrfmiddlewaretoken]').val();
          var contentionPk = $this.attr('data-contention-pk');
          var premisePk = $this.attr('data-premise-pk');
          var action = $this.attr('data-action');
          var labelSupport = $this.attr('data-label-support');
          var labelUndo = $this.attr('data-label-undo');
          $.ajax($this.attr('action'),
            {
              type: action,
              headers: {
                'X-CSRFToken': csrfToken
              },
              success: function () {
                if(action === 'POST') {
                  $this.attr('data-action', 'DELETE');
                  $this.find('input[type=submit]').val(labelUndo);
                } else {
                  $this.attr('data-action', 'POST');
                  $this.find('input[type=submit]').val(labelSupport);
                }
              }
            });
        });
    });

})(window.arguman || (window.arguman = {}));
