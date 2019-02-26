"use strict";
function _classCallCheck(t, e) {
    if (!(t instanceof e))
        throw new TypeError("Cannot call a class as a function")
}
function make_tmpl_data(t) {
    var e = [];
    /btime/.test(location.href) && !/localhost/.test(location.host) && location.host.match(/([^\.]+)\.btime/)[1];
    return t.forEach(function(t) {
        var a = {
            module: t.module || "",
            m_type: t.type || "",
            url: location.origin + "/item/router?gid=" + t.gid,
            title: t.data.title || "",
            summary: t.data.summary || "",
            pdate: $webFunc.elapse(t.data.pdate) || "",
            duration: t.data.duration || "",
            source: t.data.source || "",
            num: "",
            covers: t.data.covers[0] || "",
            comments: "",
            status: t.data.live_stats || "",
            gid: t.gid || "",
            tag: []
        };
        t.data.watches && 0 != t.data.watches && a.tag.push({
            name: (t.data.watches < 1e4 ? t.data.watches : parseInt(t.data.watches / 1e4) + "\u4e07") + "\u9605\u8bfb",
            str_color: "#999"
        }),
        t.is_stick && a.tag.push({
            name: "\u7f6e\u9876",
            str_color: "#ff3644"
        }),
        e.push(a)
    }),
    e
}
var _createClass = function() {
    function t(t, e) {
        for (var a = 0; a < e.length; a++) {
            var n = e[a];
            n.enumerable = n.enumerable || !1,
            n.configurable = !0,
            "value"in n && (n.writable = !0),
            Object.defineProperty(t, n.key, n)
        }
    }
    return function(e, a, n) {
        return a && t(e.prototype, a),
        n && t(e, n),
        e
    }
}();
!function() {
    var t = function() {
        function t() {
            _classCallCheck(this, t),
            this.init(),
            this.bindEvent()
        }
        return _createClass(t, [{
            key: "init",
            value: function() {
                this.cid = $webFunc.getParam("cid"),
                this.cid && this.renderList()
            }
        }, {
            key: "renderList",
            value: function() {
                var t = this
                  , e = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 1
                  , a = arguments[1]
                  , n = "";
                this.reqestList(e).then(function(e) {
                    e && t.hideLoading(),
                    make_tmpl_data(e.data).forEach(function(t, e) {
                        n += window.mbtime.tmpl[t.module].render(t)
                    }),
                    $(".news-list").append(n),
                    a && a(e)
                })
            }
        }, {
            key: "reqestList",
            value: function() {
                var t = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 1
                  , e = "https:" === location.protocol ? "https:" : "http:"
                  , a = e + "//h5.btime.com/news/getSubjectNews"
                  , n = {
                    cid: this.cid,
                    refresh_total: t
                };
                return new Promise(function(t, e) {
                    $.ajax({
                        url: a,
                        type: "get",
                        dataType: "jsonp",
                        data: n,
                        success: function(e) {
                            if (e && 0 == e.errno) {
                                var a = e.data && e.data.uinfo || [];
                                t(a)
                            }
                        },
                        error: function(t) {
                            return e(t)
                        }
                    })
                }
                )
            }
        }, {
            key: "hideLoading",
            value: function() {
                $(".loading").hide()
            }
        }, {
            key: "bindEvent",
            value: function() {
                var t = 1
                  , e = this
                  , a = {
                    render: "\u52a0\u8f7d\u4e2d...",
                    loadMore: "\u4e0a\u62c9\u52a0\u8f7d\u66f4\u591a",
                    noMore: "\u6ca1\u6709\u66f4\u591a"
                };
                this.isScroll = !1;
                var n = $(".container .load-text");
                $(document).on("scroll", function() {
                    if (!e.isScroll) {
                        var i = $(window).scrollTop()
                          , o = $(window).height();
                        $(".container").height() - i - o < 50 && (n.html(a.render),
                        e.isScroll = !0,
                        t++,
                        e.renderList(t, function(t) {
                            if (!t.length)
                                return e.isScroll = !0,
                                void n.html(a.noMore);
                            e.isScroll = !1,
                            n.html(a.loadMore)
                        }))
                    }
                })
            }
        }]),
        t
    }();
    window.pageRender = t
}();
