// Transcrypt'ed from Python, 2021-08-20 04:44:54
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var Vue = require ('vue') ['default'];

function clone(obj) {
    var copy;

    // Handle the 3 simple types, and null or undefined
    if (null == obj || "object" != typeof obj) return obj;

    // Handle Date
    if (obj instanceof Date) {
        copy = new Date();
        copy.setTime(obj.getTime());
        return copy;
    }

    // Handle Array
    if (obj instanceof Array) {
        copy = [];
        for (var i = 0, len = obj.length; i < len; i++) {
            copy[i] = clone(obj[i]);
        }
        return copy;
    }

    // Handle Object
    if (obj instanceof Object) {
        copy = {};
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) copy[attr] = clone(obj[attr]);
        }
        return copy;
    }

    throw new Error("Unable to copy obj! Its type isn't supported.");
}

export var draggable = require ('vuedraggable');
Vue.component ('draggable', draggable);
export var VuePy =  __class__ ('VuePy', [object], {
	__module__: __name__,
	methods: [],
	computed: [],
	watch: [],
	delimiters: ['[[', ']]'],
	__deployed__: false,
	__link__: false,
	get __init__ () {return __get__ (this, async function (self, settings) {
		if (typeof settings == 'undefined' || (settings != null && settings.hasOwnProperty ("__kwargtrans__"))) {;
			var settings = dict ({});
		};
		var data = dict ({'methods': dict ({}), 'watch': dict ({}), 'compute': dict ({})});
		data.py_update (settings);
		for (var elem of dir (self)) {
			if (!__in__ (elem, ['__bases__', '__class__', '__init__', '__metaclass__', '__module__', '__name__', '__new__', 'methods', 'computed', 'watch', 'mount', 'deploy', '__deployed__', '__link__', 'data'])) {
				if (typeof (getattr (self, elem)) == 'function') {
					getattr (self, elem).__name__ = elem;
				}
				if (__in__ (elem, self.methods)) {
					var wrapper = function (self, elem) {
						var fn = async function () {
							var args = tuple ([].slice.apply (arguments).slice (0));
							var that = this;
							self.vue = that;
							var d = await self [elem] (...args);
							self.vue = that;
							return d;
						};
						return fn;
					};
					data ['methods'] [elem] = wrapper (self, elem);
				}
				else if (__in__ (elem, self.computed)) {
					var wrapper = function (self, elem) {
						var fn = async function () {
							var args = tuple ([].slice.apply (arguments).slice (0));
							var that = this;
							self.vue = that;
							var d = await self [elem] (...args);
							self.vue = that;
							return d;
						};
						return fn;
					};
					data ['computed'] [elem] = wrapper (self, elem);
				}
				else if (__in__ (elem, self.watch)) {
					var wrapper = function (self, elem) {
						var fn = async function () {
							var args = tuple ([].slice.apply (arguments).slice (0));
							var that = this;
							self.vue = that;
							var d = await self [elem] (...args);
							self.vue = that;
							return d;
						};
						return fn;
					};
					data ['watch'] [elem] = wrapper (self, elem);
				}
				else if (typeof (getattr (self, elem)) == 'function') {
					var wrapper = function (self, elem) {
						var fn = async function () {
							var args = tuple ([].slice.apply (arguments).slice (0));
							var that = this;
							self.vue = that;
							var result = await self [elem] (that, ...args);
							self.vue = that;
							return result;
						};
						return fn;
					};
					data [elem] = wrapper (self, elem);
				}
				else if (!(self.__link__)) {
					data [elem] = clone (getattr (self, elem));
				}
				else {
					data [elem] = getattr (self, elem);
				}
			}
		}
		if (__in__ ('data', dir (self))) {
			var wrapper = function (self, elem) {
				var fn = function () {
					var args = tuple ([].slice.apply (arguments).slice (0));
					var that = this;
					self.vue = that;
					return clone (self ['data'] (...args));
				};
				return fn;
			};
			if (!(self.__link__)) {
				data ['data'] = wrapper (self, 'data');
			}
			else {
				data ['data'] = getattr (self, 'data');
			}
		}
		self.__component__ = data;
	});},
	get beforeCreate () {return __get__ (this, function (self, vue) {
		self.vue = vue;
	});},
	get off () {return __get__ (this, function (self, fn) {
		if (fn) {
			for (var event of dict (self.vue._events).py_keys ()) {
				for (var [k, elem] of enumerate (self.vue._events [event])) {
					if (elem == fn) {
						self.vue._events [event] [k].splice (k, 1);
					}
				}
			}
		}
		else {
			self.vue._events = [];
		}
	});},
	get deploy () {return __get__ (this, async function (self) {
		if (!(self.__deployed__)) {
			self.vue = new Vue (self.__component__);
			self.__deployed__ = true;
		}
		return self;
	});},
	get mount () {return __get__ (this, async function (self, el) {
		await self.deploy ();
		self.vue ['$mount'] (el);
		return self;
	});},
	get updated () {return __get__ (this, function (self) {
		// pass;
	});}
});

//# sourceMappingURL=vuepy.map