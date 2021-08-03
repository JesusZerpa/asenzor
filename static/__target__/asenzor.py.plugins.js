// Transcrypt'ed from Python, 2021-08-02 10:03:37
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {VuePy} from './asenzor.py.vuepy.js';
var __name__ = 'asenzor.py.plugins';
export var Plugins =  __class__ ('Plugins', [VuePy], {
	__module__: __name__,
	methods: ['search', 'install'],
	plugins: [],
	showUpload: false,
	get determineDragAndDropCapable () {return __get__ (this, function (self) {
		var div = document.createElement ('div');
		return (__in__ ('draggable', dir (div)) || __in__ ('ondragstart', dir (div)) && __in__ ('ondrop', dir (div))) && __in__ ('FormData', window) && __in__ ('FileReader', window);
	});},
	get mounted () {return __get__ (this, function (self) {
		self.vue.dragAndDropCapable = self.determineDragAndDropCapable ();
		if (self.vue.dragAndDropCapable) {
			var for_events = function (evt) {
				var add_event = function (e) {
					e.preventDefault ();
					e.stopPropagation ();
				};
				add_event.bind (self.vue);
				self.vue ['$refs'].fileform.addEventListener (evt, add_event, false);
			};
			for_events.bind (self.vue);
			['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop'].forEach (for_events);
		}
		var capture_files = function (e) {
			var i = 0;
			while (i < e.dataTransfer.files.length) {
				self.vue.files.push (e.dataTransfer.files [i]);
				i++;
			}
			self.getImagePreviews ();
			self.submitFiles ();
		};
		capture_files.bind (this);
		self.vue ['$refs'].fileform.addEventListener ('drop', capture_files);
		fetch ('/json/media/', {'method': 'GET'}).then ((function __lambda__ (res) {
			return res.json ();
		})).then (self.drawImages).catch ((function __lambda__ (e) {
			return console.log ('FAILURE!!', e);
		}));
	});},
	get drawImages () {return __get__ (this, function (self, data) {
		var files = [];
		for (var elem of data ['items']) {
			files.append (dict ({'src': elem ['guid']}));
		}
		self.vue.images = files;
	});},
	get submitFiles () {return __get__ (this, function (self) {
		var formData = new FormData ();
		var i = 0;
		console.log (self.vue.files);
		while (i < self.vue.files.length) {
			var file = self.vue.files [i];
			formData.append (('files[' + i) + ']', file);
			i++;
		}
		formData.append ('type', 'upload');
		fetch ('/json/plugins/', {'method': 'POST', 'body': formData}).then ((function __lambda__ (res) {
			return res.json ();
		})).then (self.uploaded).catch ((function __lambda__ (e) {
			return console.log ('FAILURE!!', e);
		}));
	});},
	get onUploadProgress () {return __get__ (this, function (self, progressEvent) {
		self.uploadPercentage = parseInt (Math.round ((progressEvent.loaded * 100) / progressEvent.total));
		self.uploadPercentage.bind (self.vue);
	});},
	get data () {return __get__ (this, function (self) {
		console.log (window.DATA ['plugins']);
		return dict ({'plugins': window.DATA ['plugins'], 'dragAndDropCapable': false, 'files': [], 'uploadPercentage': 0, 'showUpload': false});
	});},
	get search () {return __get__ (this, function (self) {
		// pass;
	});},
	get install () {return __get__ (this, function (self, id) {
		var form = new FormData ();
		form.append ('id', id);
		form.append ('type', 'remote');
		fetch ('json/plugins/', dict ({'method': 'POST', 'body': form}));
	});}
});

//# sourceMappingURL=asenzor.py.plugins.map