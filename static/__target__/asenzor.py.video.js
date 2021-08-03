// Transcrypt'ed from Python, 2021-08-02 10:03:38
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {VuePy} from './asenzor.py.vuepy.js';
var __name__ = 'asenzor.py.video';
export var Video =  __class__ ('Video', [VuePy], {
	__module__: __name__,
	methods: ['update_video'],
	template: '<div>\n\t<iframe :src="video" style="max-width:100%"/>\n\t<input :ref="\'video\'" @change="update_video"/>\n\t</div>\n\t',
	get data () {return __get__ (this, function (self) {
		var py_name = self.vue ['$attrs'] ['name'];
		var video = null;
		return dict ({'video': video, 'name': py_name});
	});},
	get update_video () {return __get__ (this, function (self) {
		self.vue.video = self.vue ['$refs'] ['video'].value;
		self.vue ['$root'].update_content (dict ([[self.vue ['name'], self.vue.video]]));
	});}
});

//# sourceMappingURL=asenzor.py.video.map