// Transcrypt'ed from Python, 2021-01-29 21:42:34
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {Color} from './asenzor.py.colorpicker.js';
import {Embeded} from './asenzor.py.embeded.js';
import {SimpleMenu} from './asenzor.py.simplemenu.js';
import {Video} from './asenzor.py.video.js';
import {TinyEditor} from './asenzor.py.tiny.js';
import {ImageSelect} from './asenzor.py.image_select.js';
import {VuePy} from './asenzor.py.vuepy.js';
var __name__ = 'asenzor.py.edit';
export var Editor = require ('@tinymce/tinymce-vue') ['default'];
window.VUE_COMPONENTS ['asenzor'] ['editor'] = TinyEditor ().__component__;
window.VUE_COMPONENTS ['asenzor'] ['image-select'] = ImageSelect ().__component__;
window.VUE_COMPONENTS ['asenzor'] ['video-widget'] = Video ().__component__;
window.VUE_COMPONENTS ['asenzor'] ['simple-menu'] = SimpleMenu ().__component__;
window.VUE_COMPONENTS ['asenzor'] ['embeded'] = Embeded ().__component__;
window.VUE_COMPONENTS ['asenzor'] ['color'] = Color ().__component__;
export var Vue = require ('vue') ['default'];
export var Edit =  __class__ ('Edit', [VuePy], {
	__module__: __name__,
	methods: ['publish', 'save', 'update_from_widget', 'update_content', 'get_content', 'get_by_type'],
	components: window.VUE_COMPONENTS ['asenzor'],
	content: '',
	type: null,
	template: null,
	main_image: null,
	author: null,
	order: null,
	extra_data: dict ({}),
	toogle: dict ({}),
	post_type: null,
	title: null,
	get created () {return __get__ (this, function (self) {
		window.edit = self.vue;
	});},
	get data () {return __get__ (this, function (self) {
		var models = dict ({});
		for (var [py_name, widget] of self.get_by_type ('Color').py_items ()) {
			if (__in__ ('v-model', dict (widget ['options']).py_keys ())) {
				models [widget ['options'] ['v-model'].py_split ('.') [1]] = widget ['value'];
			}
		}
		return dict ({'content': (window.DATA ['post'] ? window.DATA ['post'] ['content'] : ''), 'title': (window.DATA ['post'] ? window.DATA ['post'] ['title'] : ''), 'status': null, 'author': null, 'order': null, 'type': null, 'template': null, 'main_image': null, 'toogle': self.toogle, 'post_type': null, 'type': 'post', 'models': models});
	});},
	get mounted () {return __get__ (this, function (self) {
		self.vue ['post_type'] = self.vue ['$el'] ['attributes'] ['post_type'] ['value'];
		if (window.DATA ['post'] ['content']) {
			console.log ('wwwww', self.vue.get_by_type ('Color'));
			for (var [py_name, widget] of self.vue.get_by_type ('Color').py_items ()) {
				if (__in__ ('v-model', dict (widget ['options']).py_keys ())) {
					self.vue.models [widget ['options'] ['v-model']] = widget ['value'];
					console.log ('hhhh', self.vue.models [widget ['options'] ['v-model']], widget ['value']);
				}
			}
		}
		self.vue.template = self.vue ['$refs'] ['template'].attributes ['value'] ['value'];
		for (var elem of dict (self.vue ['$refs']).py_keys ()) {
			if (elem.startswith ('toogle-')) {
				self.vue ['$refs'] [elem];
				self.vue.toogle [elem] = true;
			}
		}
		self.vue.order = self.vue ['$refs'] ['order'].attributes ['value'] ['value'];
		self.vue ['type'] = self.vue ['$refs'] ['type'].attributes ['data-value'] ['value'];
		var sticky = function () {
			var altura = $ ('.panel2').offset ().top;
			var altura = $ ('.navbar').offset ().top;
			var py_switch = function () {
				if ($ (window).scrollTop () > altura) {
					$ ('.panel2').addClass ('panel2-fixed');
				}
				else {
					$ ('.panel2').removeClass ('panel2-fixed');
				}
			};
			$ (window).on ('scroll', py_switch);
		};
		$ (document).ready (sticky);
		console.log ('iiii');
	});},
	get update_from_widget () {return __get__ (this, function (self, evt, value, py_name) {
		if (py_name) {
			console.log (dict ([[py_name, value]]));
			self.update_content (dict ([[py_name, value]]));
		}
		else {
			console.log (dict ([[evt.target ['name'], evt.target.value]]));
			self.update_content (dict ([[evt.target ['name'], evt.target.value]]));
		}
	});},
	get publish () {return __get__ (this, async function (self) {
		var form = new FormData ();
		form.append ('title', self.vue.title);
		form.append ('type', self.vue ['type']);
		form.append ('menu_order', self.vue.order);
		form.append ('status', 'publish');
		if (window.DATA ['post']) {
			form.append ('id', window.DATA ['post'] ['id']);
		}
		console.log ('xxxxxx', self.vue.post_type);
		if (self.vue.post_type == 'custom') {
			var content = JSON.stringify (self.vue.content);
			form.append ('content', content);
		}
		else {
			form.append ('content', self.vue.content);
		}
		var req = await fetch ('/json/posts/', dict ({'body': form, 'method': 'POST'}));
		if (req.status == 200) {
			self.alert ('Creado con exito');
		}
		else {
			self.alert ('A ocurrido un error', 'warning');
		}
		var data = await req.json ();
		var post = data ['item'];
		var form = new FormData ();
		for (var elem of self.extra_data.py_keys ()) {
			form.append (elem, self.extra_data [elem]);
		}
		form.append ('post', post ['id']);
		form.append ('template', self.vue.template);
		var req = await fetch ('/json/postmeta/', {'body': form, 'method': (window.DATA ['post'] ['id'] != undefined ? 'PATCH' : 'POST')});
	});},
	get save () {return __get__ (this, async function (self) {
		var form = new FormData ();
		form.append ('title', self.vue.title);
		form.append ('type', self.vue ['type']);
		form.append ('menu_order', self.vue.order);
		form.append ('status', 'trash');
		if (window.DATA ['post']) {
			form.append ('id', window.DATA ['post'] ['id']);
		}
		console.log ('xxxxxx', self.vue.post_type);
		if (self.vue.post_type == 'custom') {
			var content = JSON.stringify (self.vue.content);
			form.append ('content', content);
		}
		else {
			form.append ('content', self.vue.content);
		}
		var req = await fetch ('/json/posts/', dict ({'body': form, 'method': (window.DATA ['post'] ['id'] != undefined ? 'PATCH' : 'POST')}));
		console.log (req.status);
		if (req.status == 200) {
			self.alert ('Actualizado con exito');
		}
		else {
			self.alert ('A ocurrido un error', 'warning');
		}
		var data = await req.json ();
		var post = data ['item'];
		var form = new FormData ();
		for (var elem of self.extra_data.py_keys ()) {
			form.append (elem, self.extra_data [elem]);
		}
		form.append ('post', post ['id']);
		form.append ('template', self.vue.template);
		var req = await fetch ('/json/postmeta/', {'body': form, 'method': (window.DATA ['post'] ['id'] != undefined ? 'PATCH' : 'POST')});
	});},
	get alert () {return __get__ (this, function (self, text, status) {
		if (typeof status == 'undefined' || (status != null && status.hasOwnProperty ("__kwargtrans__"))) {;
			var status = 'success';
		};
		var node = $ ('<div id="alert" class="alert alert-dismissible fade show" style="position: fixed;top:20px;right: 20px" role="alert">\n          {}\n          <button type="button" class="close" data-dismiss="alert" aria-label="Close">\n            <span aria-hidden="true">&times;</span>\n          </button>\n        </div>'.format (text));
		node.addClass ('alert-' + status);
		$ (document.body).append (node);
	});},
	get update_content () {return __get__ (this, function (self, data) {
		for (var [elem, value] of dict (data).py_items ()) {
			var py_name = elem.py_split ('.');
			if (len (py_name) == 2) {
				self.vue.content [py_name [0]] [py_name [1]] ['value'] = value;
			}
			else if (len (py_name) == 3) {
				self.vue.content [py_name [0]] [py_name [1]] ['value'] [py_name [2]] = value;
			}
		}
	});},
	get get_content () {return __get__ (this, function (self, py_name) {
		if (DATA ['post'] && DATA ['post'] ['content']) {
			var py_name = py_name.py_split ('.');
			if (len (py_name) == 2) {
				return DATA ['post'] ['content'] [py_name [0]] [py_name [1]] ['value'];
			}
			else if (len (py_name) == 3) {
				return DATA ['post'] ['content'] [py_name [0]] [py_name [1]] ['value'] [py_name [2]];
			}
		}
		else {
			return null;
		}
	});},
	get get_by_type () {return __get__ (this, function (self, py_metatype) {
		var components = dict ({});
		if (DATA ['post'] && DATA ['post'] ['content']) {
			for (var elem of dict (DATA ['post'] ['content']).py_keys ()) {
				for (var elem2 of dict (DATA ['post'] ['content'] [elem]).py_keys ()) {
					if (py_metatype == DATA ['post'] ['content'] [elem] [elem2] ['type']) {
						components [(elem + '.') + elem2] = DATA ['post'] ['content'] [elem] [elem2];
					}
				}
			}
		}
		return components;
	});}
});
export var app = Edit ();

//# sourceMappingURL=asenzor.py.edit.map