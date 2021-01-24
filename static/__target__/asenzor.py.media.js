// Transcrypt'ed from Python, 2021-01-24 19:43:41
var re = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_re__ from './re.js';
__nest__ (re, '', __module_re__);
import {VuePy} from './asenzor.py.vuepy.js';
var __name__ = 'asenzor.py.media';
export var Media =  __class__ ('Media', [VuePy], {
	__module__: __name__,
	methods: ['select', 'drag', 'drop', 'upload', 'accept', 'edit', 'remove'],
	images: [],
	single: false,
	mediatabs: 0,
	active: null,
	get data () {return __get__ (this, function (self) {
		return dict ({'images': [], 'dragAndDropCapable': false, 'files': [], 'uploadPercentage': 0, 'selected': [], 'desmark': [], 'mediatabs': self.mediatabs, 'active': null, 'search': ''});
	});},
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
			console.log ('@@@@@', e.dataTransfer.files.length);
			while (i < e.dataTransfer.files.length) {
				self.vue.files.push (e.dataTransfer.files [i]);
				i++;
			}
			self.submitFiles ();
		};
		capture_files.bind (this);
		self.vue ['$refs'].fileform.addEventListener ('drop', capture_files);
		fetch ('/json/media/', {'method': 'GET'}).then ((function __lambda__ (res) {
			return res.json ();
		})).then (self.drawImages).catch ((function __lambda__ (e) {
			return self.vue ['$root'].alert (e, 'danger');
		}));
	});},
	get drawImages () {return __get__ (this, function (self, data) {
		var files = [];
		for (var elem of data ['items']) {
			files.append (dict ({'src': elem ['guid'], 'id': elem ['id'], 'alternative': '', 'title': (elem ['title'] ? elem ['title'] : ''), 'name': elem ['name'], 'author': elem ['author'] ['username'], 'description': elem ['content'], 'sizes': elem ['sizes']}));
		}
		self.vue.images = files;
	});},
	get getImagePreviews () {return __get__ (this, function (self) {
		var i = 0;
	});},
	get removeFile () {return __get__ (this, function (self, clave) {
		self.vue.files.splice (clave, 1);
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
		fetch ('/json/media/', {'method': 'POST', 'body': formData}).then ((function __lambda__ (res) {
			return res.json ();
		})).then (self.uploaded).catch ((function __lambda__ (e) {
			return console.log ('FAILURE!!', e);
		}));
		self.vue.files = [];
	});},
	get onUploadProgress () {return __get__ (this, function (self, progressEvent) {
		self.uploadPercentage = parseInt (Math.round ((progressEvent.loaded * 100) / progressEvent.total));
		self.uploadPercentage.bind (self.vue);
	});},
	get uploaded () {return __get__ (this, function (self, data) {
		var item = data ['item'];
		var src = item ['guid'];
		delete item ['guid'];
		item ['src'] = src;
		self.vue.images.push (item);
		if ($ (self.vue ['$refs'] ['tab1']).hasClass ('active')) {
			$ (self.vue ['$refs'] ['tab1']).removeClass ('active show');
		}
		$ (self.vue ['$refs'] ['tab2']).addClass ('active show');
		$ (self.vue ['$refs'] ['tab2']).addClass ('active show');
		$ ('#subir-archivo-tab').removeClass ('active');
		$ ('#biblioteca-medios-tab').addClass ('active');
	});},
	get upload () {return __get__ (this, function (self) {
		// pass;
	});},
	get drag () {return __get__ (this, function (self) {
		// pass;
	});},
	get drop () {return __get__ (this, function (self) {
		// pass;
	});},
	get py_clear () {return __get__ (this, function (self) {
		self.vue.selected = [];
		self.vue.desmark = [];
		for (var elem of dict (self.vue ['$refs']).py_keys ()) {
			if (elem.startswith ('slide_')) {
				self.vue ['$refs'] [elem] [0].style.border = 'inherit';
			}
		}
	});},
	get remove () {return __get__ (this, function (self) {
		// pass;
		fetch ('/json/media/', {'method': 'DELETE', 'body': formData}).then ((function __lambda__ (res) {
			return res.json ();
		})).then (self.deleted).catch ((function __lambda__ (e) {
			return console.log ('FAILURE!!', e);
		}));
	});},
	get edit () {return __get__ (this, function (self) {
		fetch ('/json/media/', {'method': 'PUT', 'body': formData}).then ((function __lambda__ (res) {
			return res.json ();
		})).then (self.edited).catch ((function __lambda__ (e) {
			return console.log ('FAILURE!!', e);
		}));
	});},
	get deleted () {return __get__ (this, function (self, data) {
		var l = [];
		for (var elem of self.vue.images) {
			if (elem.id != data ['item']) {
				l.append (elem);
			}
		}
		self.vue.images = l;
	});},
	get edited () {return __get__ (this, function (self, data) {
		// pass;
	});},
	get select () {return __get__ (this, function (self, py_name) {
		if (!(self.single)) {
			if (self.vue.selected.includes (py_name)) {
				self.vue ['$refs'] [py_name] [0].style.border = 'solid 2px gray';
				var i = self.vue.selected.indexOf (py_name);
				self.vue.selected.splice (i, 1);
				if (!(self.vue.desmark.includes (py_name))) {
					self.vue.desmark.push (py_name);
				}
			}
			else if (self.vue.desmark.includes (py_name)) {
				self.vue ['$refs'] [py_name] [0].style.border = 'inherit';
				var i = self.vue.desmark.indexOf (py_name);
				self.vue.desmark.splice (i, 1);
			}
			else {
				self.vue ['$refs'] [py_name] [0].style.border = 'solid 2px blue';
				self.vue.selected.push (py_name);
				self.vue.active = self.activate (self.getdata (self.vue ['$refs'] [py_name] [0].id));
			}
		}
		else if (self.single) {
			if (len (list (self.vue.selected)) == 0) {
				self.vue.selected.push (py_name);
				self.vue ['$refs'] [py_name] [0].style.border = 'solid 2px blue';
				self.vue.active = self.activate (self.getdata (self.vue ['$refs'] [py_name] [0].id));
			}
			else if (self.vue.selected.includes (py_name)) {
				var i = self.vue.selected.indexOf (py_name);
				self.vue.selected.splice (i, 1);
				self.vue ['$refs'] [py_name] [0].style.border = 'inherit';
			}
			else {
				self.vue.selected [0] = py_name;
				for (var elem of dict (self.vue ['$refs']).py_keys ()) {
					if (elem != py_name) {
						self.vue ['$refs'] [py_name] [0].style.border = 'inherit';
					}
				}
				self.vue ['$refs'] [py_name] [0].style.border = 'solid 2px blue';
				self.vue.active = self.activate (self.getdata (self.vue ['$refs'] [py_name] [0].id));
			}
		}
	});},
	get getdata () {return __get__ (this, function (self, id) {
		for (var img of self.vue.images) {
			if (img.id == int (id)) {
				return img;
			}
		}
	});},
	get activate () {return __get__ (this, function (self, data) {
		return data;
	});},
	get accept () {return __get__ (this, function (self) {
		var selected = [];
		for (var elem of self.vue.selected) {
			for (var img of self.vue.images) {
				if (img.id == int (self.vue ['$refs'] [elem] [0].id)) {
					selected.push (img);
				}
			}
		}
		self.vue ['$emit'] ('accept', selected);
		$ ('#media_modal').modal ('hide');
		self.off ();
	});}
});

//# sourceMappingURL=asenzor.py.media.map