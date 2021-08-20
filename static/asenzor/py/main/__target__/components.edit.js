<<<<<<< HEAD
// Transcrypt'ed from Python, 2021-08-11 03:02:16
=======
// Transcrypt'ed from Python, 2021-08-11 02:19:42
>>>>>>> 5ced66f386b580f2b5e0b9fa975a5a1f62ad9de6
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {Color} from './components.colorpicker.js';
import {Embeded} from './components.embeded.js';
import {SimpleMenu} from './components.simplemenu.js';
import {Video} from './components.video.js';
import {TinyEditor} from './components.tiny.js';
import {ImageSelect} from './components.image_select.js';
import {VuePy} from './components.vuepy.js';
var __name__ = 'components.edit';
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
	methods: ['publish', 'save', 'update_from_widget', 'update_content', 'get_content', 'get_by_type', 'edit_guid_method', 'main_image_method', 'open_modal'],
	components: window.VUE_COMPONENTS ['asenzor'],
	content: '',
	type: null,
	template: null,
	main_image: null,
	author: null,
	order: null,
	extra_data: dict ({}),
	toogle: dict ({}),
	title: null,
	get created () {return __get__ (this, function (self) {
		window.edit = self.vue;
	});},
	get data () {return __get__ (this, function (self) {
		var models = dict ({});
		return dict ({'content': '', 'title': '', 'edit_guid': false, 'author': null, 'order': null, 'password': null, 'type': null, 'template': null, 'main_image': null, 'toogle': self.toogle, 'type': 'post', 'guid': null, 'status': 'public', 'models': models});
	});},
	get edit_guid_method () {return __get__ (this, async function (self) {
		var vue = self.vue;
		vue.edit_guid = false;
		console.log (vue.guid);
		var form = new FormData ();
		form.append ('guid', vue.guid);
		form.append ('id', POST_ID);
		var req = await fetch ('/json/posts/', dict ({'body': form, 'method': 'PATCH'}));
		var data = await req.json ();
		vue.guid = data ['item'] ['guid'];
	});},
	get mounted () {return __get__ (this, async function (self) {
		var vue = self.vue;
		vue.order = POST_ORDER;
		if (POST_ID) {
			var DATA = await self.get_data ();
			console.log ('qqqqq', DATA);
			var content = (DATA ['content'] ? DATA ['content'] : '');
			if (!(content)) {
				var content = dict ({});
			}
			vue.content = content;
			vue.guid = DATA ['guid'];
			vue.status = DATA ['status'];
			console.log ('FFFFFFFFFFF', vue.status);
			if (POST_MAIN_IMAGE) {
				vue.main_image = POST_MAIN_IMAGE;
			}
			vue.title = (DATA ['title'] ? DATA ['title'] : '');
			var color = await vue.get_by_type ('Color');
			console.log ('XXXXXXXX', color);
			for (var [py_name, widget] of color.py_items ()) {
				if (__in__ ('v-model', dict (widget ['options']).py_keys ())) {
					console.log ('*************');
					if (widget ['options'] ['v-model'].py_split ('.') [0] == 'models') {
						console.log ('++++++++++');
						vue.models [widget ['options'] ['v-model'].py_split ('.') [1]] = widget ['value'];
					}
					else {
						console.log ('MMMMMMM');
						console.error ('v-model solo se permite bajo el formato models.[name-model]');
					}
				}
			}
			vue.template = TEMPLATE;
			for (var elem of dict (vue ['$refs']).py_keys ()) {
				if (elem.startswith ('toogle-')) {
					vue ['$refs'] [elem];
					vue.toogle [elem] = true;
				}
			}
			vue ['type'] = DATA ['type'];
		}
	});},
	get update_from_widget () {return __get__ (this, async function (self, evt, value, py_name) {
		if (await self.get_type (py_name) == 'Color') {
			var node = document.querySelector ("[name='{}'] .el-color-picker__color-inner".format (py_name));
			var callback = function (mutations) {
				node.style.backgroundColor = value;
				observer.disconnect ();
			};
			var observer = new MutationObserver (callback);
			var options = dict ({'childList': true, 'attributes': true});
			observer.observe (node, options);
			node.style.backgroundColor = value;
			self.vue.models [py_name.py_split ('.') [1]] = value;
		}
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
		var vue = self.vue;
		var form = new FormData ();
		form.append ('title', vue.title);
		form.append ('type', POST_TYPE);
		form.append ('menu_order', vue.order);
		if (vue.status == 'private') {
			form.append ('password', vue.password);
		}
		form.append ('status', vue.status);
		if (POST_BUILDER == 'custom') {
			var content = JSON.stringify (vue.content);
			form.append ('content', content);
		}
		else {
			form.append ('content', vue.content);
		}
		var req = await fetch ('/json/posts/', {'body': form, 'method': 'POST'});
		if (req.status == 200) {
			self.alert ('Creado con exito');
		}
		else {
			self.alert ('A ocurrido un error', 'warning');
		}
		var data = await req.json ();
		var post = data ['item'];
		vue.guid = data ['item'] ['guid'];
		var form = new FormData ();
		for (var elem of self.extra_data.py_keys ()) {
			form.append (elem, self.extra_data [elem]);
		}
		form.append ('post', post ['id']);
		form.append ('template', vue.template);
		form.append ('main_image', vue.main_image);
		var req = await fetch ('/json/postmeta/', {'body': form, 'method': 'POST'});
	});},
	get save () {return __get__ (this, async function (self) {
		var vue = self.vue;
		var form = new FormData ();
		form.append ('title', vue.title);
		form.append ('type', POST_TYPE);
		form.append ('menu_order', vue.order);
		if (vue.status == 'private') {
			form.append ('password', vue.password);
		}
		form.append ('status', vue.status);
		var DATA = await self.get_data ();
		form.append ('id', POST_ID);
		if (POST_BUILDER == 'custom') {
			var content = JSON.stringify (vue.content);
			form.append ('content', content);
		}
		else {
			form.append ('content', vue.content);
		}
		var req = await fetch ('/json/posts/', {'body': form, 'method': 'PATCH'});
		if (req.status == 200) {
			await self.alert ('Actualizado con exito');
		}
		else {
			await self.alert ('A ocurrido un error', 'warning');
		}
		var data = await req.json ();
		window.POST_ID = data ['item'] ['id'];
		var post = data ['item'];
		vue.guid = data ['item'] ['guid'];
		var form = new FormData ();
		for (var elem of self.extra_data.py_keys ()) {
			form.append (elem, self.extra_data [elem]);
		}
		form.append ('post', post ['id']);
		form.append ('template', vue.template);
		form.append ('main_image', vue.main_image);
		var req = await fetch ('/json/postmeta/', {'body': form, 'method': 'PATCH'});
	});},
	get set_image_method () {return __get__ (this, async function (self, value) {
		var vue = self.vue;
		console.log (value [0]);
		vue.main_image = value [0].src;
	});},
	get main_image_method () {return __get__ (this, async function (self) {
		var lib = await window.media;
		await lib.py_clear ();
		await lib.vue ['$on'] ('accept', await self.set_image_method);
		var modal = M.Modal.getInstance (document.querySelector ('#media_modal'));
		modal.open ();
	});},
	get insertContent () {return __get__ (this, function (self, id, value) {
<<<<<<< HEAD
=======
		console.log ('zzzzzzz', value);
>>>>>>> 5ced66f386b580f2b5e0b9fa975a5a1f62ad9de6
		for (var elem of value) {
			tinyMCE.get (id).execCommand ('mceInsertContent', false, "<img src='/media/{}'>".format (elem.src));
		}
		// pass;
	});},
	get open_modal () {return __get__ (this, async function (self, event) {
		var lib = await window.media;
		var py_metatype = await self.get_type (event.target.dataset.target);
		if (py_metatype == 'TinyMCE') {
			var id = event.target.nextSibling.children [0].id;
			await lib.vue ['$on'] ('accept', (function __lambda__ (value) {
				return self.insertContent (id, value);
			}));
		}
		await lib.py_clear ();
		var modal = M.Modal.getInstance (document.querySelector ('#media_modal'));
		modal.open ();
		// pass;
	});},
	get alert () {return __get__ (this, async function (self, text, status) {
		if (typeof status == 'undefined' || (status != null && status.hasOwnProperty ("__kwargtrans__"))) {;
			var status = '';
		};
		M.toast (dict ({'html': text, 'class': status}));
	});},
	get update_content () {return __get__ (this, async function (self, data) {
		var vue = self.vue;
		for (var [elem, value] of dict (data).py_items ()) {
			var py_name = elem.py_split ('.');
			if (len (py_name) == 2) {
				vue.content [py_name [0]] [py_name [1]] ['value'] = value;
			}
			else if (len (py_name) == 3) {
				vue.content [py_name [0]] [py_name [1]] ['value'] [py_name [2]] = value;
			}
		}
	});},
	get get_content () {return __get__ (this, async function (self, py_name) {
		var DATA = await self.get_data ();
		if (DATA ['content']) {
			var py_name = py_name.py_split ('.');
			if (len (py_name) == 2) {
				return DATA ['content'] [py_name [0]] [py_name [1]] ['value'];
			}
			else if (len (py_name) == 3) {
				return DATA ['content'] [py_name [0]] [py_name [1]] ['value'] [py_name [2]];
			}
		}
		else {
			return null;
		}
	});},
	get get_type () {return __get__ (this, async function (self, py_name) {
		var DATA = await self.get_data ();
		if (DATA ['content']) {
			var py_name = py_name.py_split ('.');
			if (len (py_name) == 2) {
				return DATA ['content'] [py_name [0]] [py_name [1]] ['type'];
			}
			else if (len (py_name) == 3) {
				return DATA ['content'] [py_name [0]] [py_name [1]] ['value'] [py_name [2]] ['type'];
			}
		}
		else {
			return null;
		}
	});},
	get get_by_type () {return __get__ (this, async function (self, py_metatype) {
		var components = dict ({});
		var DATA = await self.get_data ();
		if (typeof (DATA ['content']) == 'object') {
			for (var elem of dict (DATA ['content']).py_keys ()) {
				for (var elem2 of dict (DATA ['content'] [elem]).py_keys ()) {
					if (py_metatype == DATA ['content'] [elem] [elem2] ['type']) {
						components [(elem + '.') + elem2] = DATA ['content'] [elem] [elem2];
					}
				}
			}
		}
		return components;
	});},
	get get_data () {return __get__ (this, async function (self) {
		if (__in__ ('POST_ID', dir (window))) {
			if (!__in__ ('DATA', dir (window))) {
				var req = await fetch ('/json/posts/{}/'.format (POST_ID));
				if (req.status == 200) {
					var data = await req.json ();
					var item = data ['item'];
					window.DATA = item;
					if (POST_BUILDER == 'custom') {
						try {
							item ['content'] = JSON.parse (item ['content']);
						}
						catch (__except0__) {
							item ['content'] = dict ({});
						}
					}
				}
				else {
					console.error ('Error al obtener los datos:', req);
				}
				return item;
			}
			else {
				return DATA;
			}
		}
	});}
});
export var app = Edit ();

//# sourceMappingURL=components.edit.map