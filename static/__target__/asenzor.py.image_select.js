<<<<<<< HEAD
// Transcrypt'ed from Python, 2021-02-01 05:05:04
=======
// Transcrypt'ed from Python, 2021-01-31 03:26:14
>>>>>>> 560cc5b517483a47493f7afa38b895a8b4adf0ac
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {VuePy} from './asenzor.py.vuepy.js';
var __name__ = 'asenzor.py.image_select';
export var ImageSelect =  __class__ ('ImageSelect', [VuePy], {
	__module__: __name__,
	template: '#image-select',
	image: null,
	py_name: null,
	methods: ['open_modal', 'remove_img'],
	get data () {return __get__ (this, function (self) {
		return dict ({'image': dict ({'src': ''}), 'name': self.vue ['$attrs'] ['name']});
	});},
	get preview () {return __get__ (this, async function (self, result) {
		self.vue.image = result [0];
		await self.vue ['$root'].update_content (dict ([[self.vue ['$attrs'] ['name'], self.vue.image.src]]));
	});},
	get remove_img () {return __get__ (this, async function (self) {
		self.vue.image = null;
		await self.vue ['$root'].update_content (dict ([[self.vue ['$attrs'] ['name'], null]]));
	});},
	get mounted () {return __get__ (this, async function (self) {
		var vue = self.vue;
		var value = await vue ['$root'].get_content (vue ['$attrs'] ['name']);
		if (value) {
			if (value) {
				var image = dict ({'src': value});
			}
		}
		else {
			var image = vue.image;
		}
		vue ['image'] = image;
	});},
	get open_modal () {return __get__ (this, async function (self) {
		window.media.single = true;
		var lib = await media;
		console.log (lib);
		lib.vue ['$on'] ('accept', await self.preview);
		$ ('#media_modal').modal ('show');
	});}
});

//# sourceMappingURL=asenzor.py.image_select.map