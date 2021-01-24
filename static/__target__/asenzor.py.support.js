// Transcrypt'ed from Python, 2021-01-24 19:43:40
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {VuePy} from './asenzor.py.vuepy.js';
var __name__ = 'asenzor.py.support';
export var Support =  __class__ ('Support', [VuePy], {
	__module__: __name__,
	methods: ['change', 'update_token'],
	get data () {return __get__ (this, function (self) {
		return dict ({'parner': DATA ['parner']});
	});},
	get change () {return __get__ (this, function (self) {
		self.vue ['$refs'] ['parner_token'].disabled = false;
	});},
	get update_token () {return __get__ (this, async function (self) {
		var form = new FormData ();
		form.append ('parner_token', self.vue ['$refs'] ['parner_token'].value);
		var req = await fetch (ASENZOR_URL + 'json/support/change-parner', dict ({'body': form, 'method': 'PATCH'}));
		var data = req.json ();
		self.vue ['parner'] = data ['item'];
		self.vue ['$refs'] ['parner_token'].disabled = true;
	});}
});

//# sourceMappingURL=asenzor.py.support.map