// Transcrypt'ed from Python, 2021-01-31 02:32:54
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {VuePy} from './asenzor.py.vuepy.js';
var __name__ = 'asenzor.py.simplemenu';
export var SimpleMenu =  __class__ ('SimpleMenu', [VuePy], {
	__module__: __name__,
	template: '#simple-menu',
	methods: ['add', 'remove', 'change', 'forceRerender'],
	get data () {return __get__ (this, function (self) {
		var menu = self.vue ['$root'].get_content (self.vue ['$attrs'] ['name']);
		if (!(menu)) {
			var menu = [];
		}
		var c = 0;
		for (var elem of menu) {
			if (elem.id > c) {
				var c = elem.id + 1;
			}
		}
		return dict ({'menu': menu, 'name': self.vue ['$attrs'] ['name'], 'c': c, 'renderComponent': true});
	});},
	get forceRerender () {return __get__ (this, function (self) {
		self.vue.renderComponent = false;
		var tick = function () {
			self.vue.renderComponent = true;
		};
		self.vue ['$nextTick'] (tick);
	});},
	get add () {return __get__ (this, function (self) {
		self.vue ['menu'].append (dict ({'name': '', 'link': '#', 'id': self.vue ['c'], 'checked': false}));
		self.vue ['c']++;
		self.vue.forceRerender ();
	});},
	get remove () {return __get__ (this, function (self, py_name) {
		var l = [];
		for (var elem of self.vue ['menu']) {
			if (!(elem.checked)) {
				l.append (elem);
			}
		}
		self.vue ['menu'] = l;
		self.vue ['$root'].update_content (dict ([[self.vue ['$attrs'] ['name'], self.vue ['menu']]]));
	});},
	get change () {return __get__ (this, function (self) {
		console.log ('&&&&&&&&&', self.vue ['$root']);
		self.vue ['$root'].update_content (dict ([[self.vue ['$attrs'] ['name'], self.vue ['menu']]]));
	});}
});

//# sourceMappingURL=asenzor.py.simplemenu.map